#!/usr/bin/env python3
"""
Focused King's Method Reverse Engineering Script
===============================================

This script focuses on the specific examples mentioned in the plan to
reverse engineer exactly how the safety stock values were calculated.

Based on the plan, we know:
- SKU 136 - Surgery Supplies: Safety Stock = 229, Lead Time = 0.5, σD = 158
- SKU 508 - Balance Sheet CC: Safety Stock = 40, Lead Time = 0.66, σD = 24

King's Method Formula: Safety Stock = Z × √(Lead Time) × σD
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
    
    return test_data, demand_data

def analyze_specific_examples(test_data, demand_data):
    """Analyze the specific examples mentioned in the plan"""
    print("\nAnalyzing specific examples from the plan...")
    
    # Convert date column
    demand_data['PO Week Ending Date'] = pd.to_datetime(demand_data['PO Week Ending Date'])
    
    # Get date range
    min_date = demand_data['PO Week Ending Date'].min()
    max_date = demand_data['PO Week Ending Date'].max()
    print(f"Demand data range: {min_date} to {max_date}")
    
    # Focus on specific examples from the plan
    examples = [
        {'sku': 136, 'dept': 'Surgery Supplies', 'dept_num': 7470009, 'expected_ss': 229, 'expected_lt': 0.5},
        {'sku': 508, 'dept': 'Balance Sheet CC', 'dept_num': 0, 'expected_ss': 40, 'expected_lt': 0.66}
    ]
    
    results = []
    
    for example in examples:
        sku = example['sku']
        dept = example['dept']
        dept_num = example['dept_num']
        expected_ss = example['expected_ss']
        expected_lt = example['expected_lt']
        
        print(f"\nAnalyzing SKU {sku} in {dept}...")
        
        # Get test data for this combination
        test_row = test_data[
            (test_data['Oracle Item Number'] == sku) & 
            (test_data['Department Name'] == dept)
        ]
        
        if len(test_row) == 0:
            print(f"  No test data found for SKU {sku} in {dept}")
            continue
        
        actual_ss = test_row['Safety stock_units'].iloc[0]
        z_score = test_row['Z-score'].iloc[0]
        avg_daily_burn = test_row['Avg Daily Burn Rate'].iloc[0]
        
        print(f"  Test data: SS={actual_ss}, Z={z_score}, Burn Rate={avg_daily_burn}")
        
        # Get demand data for this combination
        dept_demand = demand_data[
            (demand_data['Oracle Item Number'] == sku) & 
            (demand_data['Department Number'] == dept_num)
        ].copy()
        
        if len(dept_demand) == 0:
            print(f"  No demand data found for SKU {sku} in department {dept_num}")
            continue
        
        print(f"  Found {len(dept_demand)} demand records")
        
        # Calculate demand statistics for different time periods
        time_periods = {
            'all_data': dept_demand,
            '2024_only': dept_demand[dept_demand['PO Week Ending Date'].dt.year == 2024],
            '2023_2025': dept_demand[dept_demand['PO Week Ending Date'].dt.year.isin([2023, 2024, 2025])],
            'last_12_months': dept_demand[dept_demand['PO Week Ending Date'] >= (max_date - timedelta(days=365))],
            '2024_2025': dept_demand[dept_demand['PO Week Ending Date'].dt.year.isin([2024, 2025])]
        }
        
        period_analysis = {}
        
        for period_name, period_data in time_periods.items():
            if len(period_data) > 1:
                # Calculate daily demands (weekly data converted to daily)
                daily_demands = []
                for _, row in period_data.iterrows():
                    weekly_demand = row['Total Qty Issues']
                    daily_demand = weekly_demand / 7
                    daily_demands.append(daily_demand)
                
                demand_std = np.std(daily_demands)
                demand_var = np.var(daily_demands)
                demand_mean = np.mean(daily_demands)
                
                # Test King's formula: Z × √(Lead Time) × σD
                predicted_ss = z_score * np.sqrt(expected_lt) * demand_std
                error = abs(predicted_ss - actual_ss)
                error_pct = (error / actual_ss) * 100 if actual_ss > 0 else 100
                
                period_analysis[period_name] = {
                    'count': len(period_data),
                    'demand_std': demand_std,
                    'demand_var': demand_var,
                    'demand_mean': demand_mean,
                    'predicted_ss': predicted_ss,
                    'actual_ss': actual_ss,
                    'error': error,
                    'error_pct': error_pct,
                    'lead_time': expected_lt,
                    'z_score': z_score
                }
                
                print(f"    {period_name}: σD={demand_std:.2f}, predicted={predicted_ss:.2f}, actual={actual_ss}, error={error_pct:.1f}%")
        
        # Find the best period match
        if period_analysis:
            best_period = min(period_analysis.keys(), key=lambda x: period_analysis[x]['error_pct'])
            best_result = period_analysis[best_period]
            
            print(f"  Best match: {best_period} with {best_result['error_pct']:.1f}% error")
            
            results.append({
                'sku': sku,
                'department': dept,
                'best_period': best_period,
                'demand_std': best_result['demand_std'],
                'predicted_ss': best_result['predicted_ss'],
                'actual_ss': best_result['actual_ss'],
                'error_pct': best_result['error_pct'],
                'lead_time': best_result['lead_time'],
                'z_score': best_result['z_score'],
                'data_points': best_result['count']
            })
    
    return results

def test_formula_variations(test_data, demand_data):
    """Test different formula variations on all available data"""
    print("\nTesting formula variations on all available data...")
    
    # Convert date column
    demand_data['PO Week Ending Date'] = pd.to_datetime(demand_data['PO Week Ending Date'])
    
    # Get all SKU-department combinations with safety stock values
    combinations = test_data[['Oracle Item Number', 'Department Name', 'Department Number', 
                            'Safety stock_units', 'Z-score', 'Avg Daily Burn Rate']].copy()
    combinations = combinations.drop_duplicates()
    combinations = combinations.dropna(subset=['Safety stock_units'])
    
    print(f"Testing {len(combinations)} combinations...")
    
    formula_results = []
    
    for idx, combo in combinations.iterrows():
        sku = combo['Oracle Item Number']
        dept = combo['Department Name']
        dept_num = combo['Department Number']
        actual_ss = combo['Safety stock_units']
        z_score = combo['Z-score']
        avg_daily_burn = combo['Avg Daily Burn Rate']
        
        # Get demand data
        dept_demand = demand_data[
            (demand_data['Oracle Item Number'] == sku) & 
            (demand_data['Department Number'] == dept_num)
        ].copy()
        
        if len(dept_demand) < 2:
            continue
        
        # Get lead time from demand data
        lead_time = dept_demand['Avg_Lead Time'].iloc[0] if len(dept_demand) > 0 else 0
        
        # Test different time periods
        time_periods = {
            'all_data': dept_demand,
            '2024_only': dept_demand[dept_demand['PO Week Ending Date'].dt.year == 2024],
            '2023_2025': dept_demand[dept_demand['PO Week Ending Date'].dt.year.isin([2023, 2024, 2025])],
            '2024_2025': dept_demand[dept_demand['PO Week Ending Date'].dt.year.isin([2024, 2025])]
        }
        
        for period_name, period_data in time_periods.items():
            if len(period_data) > 1:
                # Calculate daily demands
                daily_demands = [row['Total Qty Issues'] / 7 for _, row in period_data.iterrows()]
                demand_std = np.std(daily_demands)
                
                if demand_std > 0:
                    # Test basic King's formula
                    predicted_ss = z_score * np.sqrt(lead_time) * demand_std
                    error = abs(predicted_ss - actual_ss)
                    error_pct = (error / actual_ss) * 100 if actual_ss > 0 else 100
                    
                    formula_results.append({
                        'sku': sku,
                        'department': dept,
                        'formula': f"basic_kings_{period_name}",
                        'predicted_ss': predicted_ss,
                        'actual_ss': actual_ss,
                        'error': error,
                        'error_pct': error_pct,
                        'lead_time': lead_time,
                        'z_score': z_score,
                        'demand_std': demand_std,
                        'data_points': len(period_data)
                    })
    
    return formula_results

def analyze_results(formula_results):
    """Analyze the results to find the best formula"""
    print("\nAnalyzing results...")
    
    if not formula_results:
        print("No results to analyze!")
        return
    
    df = pd.DataFrame(formula_results)
    
    # Group by formula and calculate accuracy metrics
    accuracy_metrics = df.groupby('formula').agg({
        'error': ['mean', 'std'],
        'error_pct': ['mean', 'std'],
        'predicted_ss': 'count'
    }).round(2)
    
    accuracy_metrics.columns = ['MAE', 'MAE_std', 'MAPE', 'MAPE_std', 'count']
    accuracy_metrics = accuracy_metrics.sort_values('MAPE')
    
    print("\nFormula Accuracy Ranking:")
    print(accuracy_metrics)
    
    # Find best performing formula
    best_formula = accuracy_metrics.index[0]
    best_metrics = accuracy_metrics.loc[best_formula]
    
    print(f"\nBest performing formula: {best_formula}")
    print(f"MAPE: {best_metrics['MAPE']:.2f}%")
    print(f"MAE: {best_metrics['MAE']:.2f}")
    print(f"Count: {best_metrics['count']}")
    
    # Show detailed results for best formula
    best_results = df[df['formula'] == best_formula]
    print(f"\nDetailed results for {best_formula}:")
    print(best_results[['sku', 'department', 'predicted_ss', 'actual_ss', 'error_pct']].head(10))
    
    # Calculate accuracy statistics
    within_10_pct = (best_results['error_pct'] <= 10).sum()
    within_20_pct = (best_results['error_pct'] <= 20).sum()
    total_results = len(best_results)
    
    print(f"\nAccuracy Statistics:")
    print(f"  Within 10%: {within_10_pct}/{total_results} ({within_10_pct/total_results*100:.1f}%)")
    print(f"  Within 20%: {within_20_pct}/{total_results} ({within_20_pct/total_results*100:.1f}%)")
    
    return best_formula, best_results, accuracy_metrics

def main():
    """Main execution function"""
    print("🔍 Focused King's Method Reverse Engineering Analysis")
    print("=" * 60)
    
    # Load data
    test_data, demand_data = load_validation_data()
    
    # Analyze specific examples
    example_results = analyze_specific_examples(test_data, demand_data)
    
    # Test formula variations
    formula_results = test_formula_variations(test_data, demand_data)
    
    # Analyze results
    if formula_results:
        best_formula, best_results, accuracy_metrics = analyze_results(formula_results)
        
        print(f"\n🎯 CONCLUSION:")
        print(f"The most likely formula they used is: {best_formula}")
        print(f"This formula achieves {accuracy_metrics.loc[best_formula, 'MAPE']:.2f}% average error")
        
        # Save results
        df = pd.DataFrame(formula_results)
        df.to_csv('scripts/focused_king_analysis_results.csv', index=False)
        accuracy_metrics.to_csv('scripts/focused_king_accuracy_metrics.csv')
        
        print(f"\nResults saved to:")
        print(f"  - scripts/focused_king_analysis_results.csv")
        print(f"  - scripts/focused_king_accuracy_metrics.csv")
    else:
        print("\n❌ No valid results generated.")

if __name__ == "__main__":
    main()
