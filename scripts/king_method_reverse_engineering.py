#!/usr/bin/env python3
"""
King's Method Reverse Engineering Script
========================================

This script analyzes the validation data to reverse engineer exactly how
the safety stock values were calculated using King's method.

King's Method Formula: Safety Stock = Z × √(Lead Time) × σD
Where:
- Z = Z-score (service level)
- Lead Time = Performance Cycle (PC)
- σD = Standard deviation of demand
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def load_validation_data():
    """Load all validation data files"""
    print("Loading validation data...")
    
    # Load test data (contains safety stock values)
    test_data = pd.read_csv('data/final/validation_subset/validation_test_data.csv')
    print(f"Loaded test data: {len(test_data)} rows")
    
    # Load demand data (contains historical demand patterns)
    demand_data = pd.read_csv('data/final/validation_subset/validation_demand_subset.csv')
    print(f"Loaded demand data: {len(demand_data)} rows")
    
    # Load SKU data (contains SKU information)
    sku_data = pd.read_csv('data/final/validation_subset/validation_sku_subset.csv')
    print(f"Loaded SKU data: {len(sku_data)} rows")
    
    return test_data, demand_data, sku_data

def extract_sku_department_combinations(test_data):
    """Extract unique SKU-department combinations with safety stock values"""
    print("\nExtracting SKU-department combinations...")
    
    # Get unique combinations
    combinations = test_data[['Oracle Item Number', 'Department Name', 'Department Number', 
                            'Safety stock_units', 'Z-score', 'Avg Daily Burn Rate']].copy()
    
    # Remove duplicates and clean data
    combinations = combinations.drop_duplicates()
    combinations = combinations.dropna(subset=['Safety stock_units'])
    
    print(f"Found {len(combinations)} unique SKU-department combinations")
    
    # Show sample data
    print("\nSample combinations:")
    print(combinations.head(10))
    
    return combinations

def analyze_demand_patterns(demand_data, combinations):
    """Analyze demand patterns for each SKU-department combination"""
    print("\nAnalyzing demand patterns...")
    
    # Convert date column
    demand_data['PO Week Ending Date'] = pd.to_datetime(demand_data['PO Week Ending Date'])
    
    # Get date range
    min_date = demand_data['PO Week Ending Date'].min()
    max_date = demand_data['PO Week Ending Date'].max()
    print(f"Demand data range: {min_date} to {max_date}")
    
    results = []
    
    for _, combo in combinations.iterrows():
        sku = combo['Oracle Item Number']
        dept = combo['Department Name']
        dept_num = combo['Department Number']
        
        # Filter demand data for this SKU-department combination
        dept_demand = demand_data[
            (demand_data['Oracle Item Number'] == sku) & 
            (demand_data['Department Number'] == dept_num)
        ].copy()
        
        if len(dept_demand) == 0:
            continue
            
        # Calculate demand statistics
        total_qty_issues = dept_demand['Total Qty Issues'].sum()
        avg_daily_burn = dept_demand['Avg Daily Burn Rate'].iloc[0] if len(dept_demand) > 0 else 0
        lead_time = dept_demand['Avg_Lead Time'].iloc[0] if len(dept_demand) > 0 else 0
        
        # Calculate demand variance using different methods
        daily_demands = []
        for _, row in dept_demand.iterrows():
            # Convert weekly demand to daily (approximate)
            weekly_demand = row['Total Qty Issues']
            daily_demand = weekly_demand / 7  # Approximate daily demand
            daily_demands.append(daily_demand)
        
        if len(daily_demands) > 1:
            demand_std = np.std(daily_demands)
            demand_var = np.var(daily_demands)
        else:
            demand_std = 0
            demand_var = 0
        
        # Test different time periods
        time_periods = {
            'all_data': dept_demand,
            '2024_only': dept_demand[dept_demand['PO Week Ending Date'].dt.year == 2024],
            '2023_2025': dept_demand[dept_demand['PO Week Ending Date'].dt.year.isin([2023, 2024, 2025])],
            'last_12_months': dept_demand[dept_demand['PO Week Ending Date'] >= (max_date - timedelta(days=365))]
        }
        
        period_stats = {}
        for period_name, period_data in time_periods.items():
            if len(period_data) > 1:
                period_demands = [row['Total Qty Issues'] / 7 for _, row in period_data.iterrows()]
                period_stats[period_name] = {
                    'std': np.std(period_demands),
                    'var': np.var(period_demands),
                    'count': len(period_data)
                }
            else:
                period_stats[period_name] = {'std': 0, 'var': 0, 'count': 0}
        
        result = {
            'sku': sku,
            'department': dept,
            'department_number': dept_num,
            'actual_safety_stock': combo['Safety stock_units'],
            'z_score': combo['Z-score'],
            'avg_daily_burn': avg_daily_burn,
            'lead_time': lead_time,
            'total_issues': total_qty_issues,
            'demand_std': demand_std,
            'demand_var': demand_var,
            'period_stats': period_stats,
            'data_points': len(dept_demand)
        }
        
        results.append(result)
    
    return results

def test_kings_formula_variations(analysis_results):
    """Test different variations of King's formula"""
    print("\nTesting King's formula variations...")
    
    formula_results = []
    
    for result in analysis_results:
        sku = result['sku']
        dept = result['department']
        actual_ss = result['actual_safety_stock']
        z_score = result['z_score']
        lead_time = result['lead_time']
        
        # Test different formula variations
        formulas = {}
        
        # Basic King's: Z × √(Lead Time) × σD
        for period_name, period_stats in result['period_stats'].items():
            if period_stats['count'] > 1 and period_stats['std'] > 0:
                basic_kings = z_score * np.sqrt(lead_time) * period_stats['std']
                formulas[f"basic_kings_{period_name}"] = basic_kings
        
        # Modified King's: Z × √(Lead Time/T1) × σD (where T1 is time period)
        for period_name, period_stats in result['period_stats'].items():
            if period_stats['count'] > 1 and period_stats['std'] > 0:
                # T1 could be 1 (daily), 7 (weekly), 30 (monthly)
                for t1 in [1, 7, 30]:
                    modified_kings = z_score * np.sqrt(lead_time / t1) * period_stats['std']
                    formulas[f"modified_kings_{period_name}_t1_{t1}"] = modified_kings
        
        # King's with lead time variance: Z × √(Lead Time × σD² + σLT² × D²)
        # Assuming σLT = 0 for now (no lead time variance data)
        for period_name, period_stats in result['period_stats'].items():
            if period_stats['count'] > 1 and period_stats['std'] > 0:
                daily_demand = result['avg_daily_burn']
                kings_with_lt_var = z_score * np.sqrt(lead_time * period_stats['var'] + 0 * daily_demand**2)
                formulas[f"kings_with_lt_var_{period_name}"] = kings_with_lt_var
        
        # Calculate accuracy for each formula
        for formula_name, predicted_ss in formulas.items():
            if predicted_ss > 0:
                error = abs(predicted_ss - actual_ss)
                error_pct = (error / actual_ss) * 100 if actual_ss > 0 else 100
                
                formula_results.append({
                    'sku': sku,
                    'department': dept,
                    'formula': formula_name,
                    'predicted_ss': predicted_ss,
                    'actual_ss': actual_ss,
                    'error': error,
                    'error_pct': error_pct,
                    'lead_time': lead_time,
                    'z_score': z_score
                })
    
    return formula_results

def analyze_formula_accuracy(formula_results):
    """Analyze which formulas are most accurate"""
    print("\nAnalyzing formula accuracy...")
    
    df = pd.DataFrame(formula_results)
    
    # Group by formula and calculate accuracy metrics
    accuracy_metrics = df.groupby('formula').agg({
        'error': ['mean', 'std'],
        'error_pct': ['mean', 'std'],
        'predicted_ss': 'count'
    }).round(2)
    
    accuracy_metrics.columns = ['MAE', 'MAE_std', 'MAPE', 'MAPE_std', 'count']
    accuracy_metrics = accuracy_metrics.sort_values('MAPE')
    
    print("\nFormula Accuracy Ranking (by Mean Absolute Percentage Error):")
    print(accuracy_metrics.head(20))
    
    # Find best performing formulas
    best_formulas = accuracy_metrics.head(5)
    
    print(f"\nTop 5 performing formulas:")
    for formula, metrics in best_formulas.iterrows():
        print(f"{formula}: MAPE={metrics['MAPE']:.2f}%, MAE={metrics['MAE']:.2f}, Count={metrics['count']}")
    
    return accuracy_metrics, df

def find_exact_formula(df, accuracy_metrics):
    """Find the exact formula they used"""
    print("\nFinding exact formula...")
    
    # Look for formulas with very high accuracy
    high_accuracy = accuracy_metrics[accuracy_metrics['MAPE'] < 5]  # Less than 5% error
    
    if len(high_accuracy) > 0:
        print(f"Found {len(high_accuracy)} formulas with <5% error:")
        for formula, metrics in high_accuracy.iterrows():
            print(f"  {formula}: MAPE={metrics['MAPE']:.2f}%")
        
        # Get detailed results for the best formula
        best_formula = high_accuracy.index[0]
        best_results = df[df['formula'] == best_formula]
        
        print(f"\nDetailed results for best formula: {best_formula}")
        print(best_results[['sku', 'department', 'predicted_ss', 'actual_ss', 'error_pct']].head(10))
        
        # Calculate overall accuracy
        overall_mape = best_results['error_pct'].mean()
        overall_mae = best_results['error'].mean()
        
        print(f"\nOverall accuracy for {best_formula}:")
        print(f"  Mean Absolute Percentage Error: {overall_mape:.2f}%")
        print(f"  Mean Absolute Error: {overall_mae:.2f}")
        print(f"  Predictions within 10%: {(best_results['error_pct'] <= 10).sum()}/{len(best_results)}")
        print(f"  Predictions within 20%: {(best_results['error_pct'] <= 20).sum()}/{len(best_results)}")
        
        return best_formula, best_results
    else:
        print("No formulas found with <5% error. Looking at top performers...")
        top_formula = accuracy_metrics.index[0]
        top_results = df[df['formula'] == top_formula]
        
        print(f"Best performing formula: {top_formula}")
        print(f"MAPE: {accuracy_metrics.loc[top_formula, 'MAPE']:.2f}%")
        
        return top_formula, top_results

def main():
    """Main execution function"""
    print("🔍 King's Method Reverse Engineering Analysis")
    print("=" * 50)
    
    # Load data
    test_data, demand_data, sku_data = load_validation_data()
    
    # Extract SKU-department combinations
    combinations = extract_sku_department_combinations(test_data)
    
    # Analyze demand patterns
    analysis_results = analyze_demand_patterns(demand_data, combinations)
    print(f"\nAnalyzed {len(analysis_results)} SKU-department combinations")
    
    # Test King's formula variations
    formula_results = test_kings_formula_variations(analysis_results)
    print(f"\nTested {len(formula_results)} formula combinations")
    
    # Analyze accuracy
    accuracy_metrics, df = analyze_formula_accuracy(formula_results)
    
    # Find exact formula
    best_formula, best_results = find_exact_formula(df, accuracy_metrics)
    
    print(f"\n🎯 CONCLUSION:")
    print(f"The most likely formula they used is: {best_formula}")
    print(f"This formula achieves {accuracy_metrics.loc[best_formula, 'MAPE']:.2f}% average error")
    
    # Save results
    df.to_csv('scripts/king_formula_analysis_results.csv', index=False)
    accuracy_metrics.to_csv('scripts/king_formula_accuracy_metrics.csv')
    
    print(f"\nResults saved to:")
    print(f"  - scripts/king_formula_analysis_results.csv")
    print(f"  - scripts/king_formula_accuracy_metrics.csv")

if __name__ == "__main__":
    main()
