#!/usr/bin/env python3
"""
Safety Stock Calculator
=======================

Based on the flowchart: Safety Stock = Z-score × Historical Demand Standard Deviation

This script calculates safety stock for all 24 SKUs using the exact formula shown.
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

def calculate_safety_stock(test_data, demand_data):
    """Calculate safety stock using: Z-score × Historical Demand Standard Deviation"""
    print("\nCalculating safety stock for all SKU-department combinations...")
    
    # Convert date column
    demand_data['PO Week Ending Date'] = pd.to_datetime(demand_data['PO Week Ending Date'])
    
    # Get all unique SKU-department combinations from test data
    combinations = test_data[['Oracle Item Number', 'Department Name', 'Department Number', 
                            'Safety stock_units', 'Z-score', 'Avg Daily Burn Rate']].copy()
    combinations = combinations.drop_duplicates()
    combinations = combinations.dropna(subset=['Safety stock_units'])
    
    print(f"Found {len(combinations)} SKU-department combinations to analyze")
    
    results = []
    
    for idx, combo in combinations.iterrows():
        sku = combo['Oracle Item Number']
        dept = combo['Department Name']
        dept_num = combo['Department Number']
        actual_ss = combo['Safety stock_units']
        z_score = combo['Z-score']
        avg_daily_burn = combo['Avg Daily Burn Rate']
        
        print(f"\nProcessing SKU {sku} in {dept}...")
        
        # Get demand data for this combination
        dept_demand = demand_data[
            (demand_data['Oracle Item Number'] == sku) & 
            (demand_data['Department Number'] == dept_num)
        ].copy()
        
        if len(dept_demand) < 2:
            print(f"  Insufficient demand data ({len(dept_demand)} records)")
            continue
        
        # Calculate historical demand standard deviation
        # Convert weekly demand to daily demand for consistency
        daily_demands = []
        for _, row in dept_demand.iterrows():
            weekly_demand = row['Total Qty Issues']
            daily_demand = weekly_demand / 7  # Convert weekly to daily
            daily_demands.append(daily_demand)
        
        demand_std = np.std(daily_demands)
        demand_mean = np.mean(daily_demands)
        
        # Get lead time from demand data
        lead_time = dept_demand['Avg_Lead Time'].iloc[0] if len(dept_demand) > 0 else 0
        
        # Calculate safety stock using the formula: Z-score × √(Lead Time) × Historical Demand Standard Deviation
        calculated_ss = z_score * np.sqrt(lead_time) * demand_std
        
        # Calculate accuracy
        error = abs(calculated_ss - actual_ss)
        error_pct = (error / actual_ss) * 100 if actual_ss > 0 else 100
        
        result = {
            'sku': sku,
            'department': dept,
            'department_number': dept_num,
            'z_score': z_score,
            'lead_time': lead_time,
            'demand_std': demand_std,
            'demand_mean': demand_mean,
            'calculated_ss': calculated_ss,
            'actual_ss': actual_ss,
            'error': error,
            'error_pct': error_pct,
            'data_points': len(dept_demand),
            'avg_daily_burn': avg_daily_burn
        }
        
        results.append(result)
        
        print(f"  Z-score: {z_score}")
        print(f"  Lead Time: {lead_time}")
        print(f"  Demand Std: {demand_std:.2f}")
        print(f"  Calculated SS: {calculated_ss:.2f}")
        print(f"  Actual SS: {actual_ss}")
        print(f"  Error: {error_pct:.1f}%")
        print(f"  Data points: {len(dept_demand)}")
    
    return results

def analyze_results(results):
    """Analyze the calculation results"""
    print("\n" + "="*60)
    print("SAFETY STOCK CALCULATION ANALYSIS")
    print("="*60)
    
    if not results:
        print("No results to analyze!")
        return
    
    df = pd.DataFrame(results)
    
    # Calculate overall accuracy metrics
    overall_mape = df['error_pct'].mean()
    overall_mae = df['error'].mean()
    within_10_pct = (df['error_pct'] <= 10).sum()
    within_20_pct = (df['error_pct'] <= 20).sum()
    within_50_pct = (df['error_pct'] <= 50).sum()
    total_results = len(df)
    
    print(f"\nOVERALL ACCURACY METRICS:")
    print(f"  Total combinations analyzed: {total_results}")
    print(f"  Mean Absolute Percentage Error (MAPE): {overall_mape:.2f}%")
    print(f"  Mean Absolute Error (MAE): {overall_mae:.2f}")
    print(f"  Within 10% error: {within_10_pct}/{total_results} ({within_10_pct/total_results*100:.1f}%)")
    print(f"  Within 20% error: {within_20_pct}/{total_results} ({within_20_pct/total_results*100:.1f}%)")
    print(f"  Within 50% error: {within_50_pct}/{total_results} ({within_50_pct/total_results*100:.1f}%)")
    
    # Show best and worst predictions
    print(f"\nBEST PREDICTIONS (lowest error %):")
    best_predictions = df.nsmallest(5, 'error_pct')
    for _, row in best_predictions.iterrows():
        print(f"  SKU {row['sku']} - {row['department']}: {row['error_pct']:.1f}% error")
        print(f"    Calculated: {row['calculated_ss']:.1f}, Actual: {row['actual_ss']}")
    
    print(f"\nWORST PREDICTIONS (highest error %):")
    worst_predictions = df.nlargest(5, 'error_pct')
    for _, row in worst_predictions.iterrows():
        print(f"  SKU {row['sku']} - {row['department']}: {row['error_pct']:.1f}% error")
        print(f"    Calculated: {row['calculated_ss']:.1f}, Actual: {row['actual_ss']}")
    
    # Show summary statistics
    print(f"\nSUMMARY STATISTICS:")
    print(f"  Z-score range: {df['z_score'].min():.2f} - {df['z_score'].max():.2f}")
    print(f"  Demand std range: {df['demand_std'].min():.2f} - {df['demand_std'].max():.2f}")
    print(f"  Calculated SS range: {df['calculated_ss'].min():.1f} - {df['calculated_ss'].max():.1f}")
    print(f"  Actual SS range: {df['actual_ss'].min():.1f} - {df['actual_ss'].max():.1f}")
    
    return df

def create_detailed_report(df):
    """Create a detailed report of all calculations"""
    print(f"\n" + "="*60)
    print("DETAILED CALCULATION REPORT")
    print("="*60)
    
    # Sort by error percentage for easy review
    df_sorted = df.sort_values('error_pct')
    
    print(f"\nAll calculations (sorted by accuracy):")
    print("-" * 100)
    print(f"{'SKU':<6} {'Department':<25} {'Z':<4} {'Std':<8} {'Calc SS':<8} {'Actual SS':<9} {'Error %':<8} {'Data Pts':<8}")
    print("-" * 100)
    
    for _, row in df_sorted.iterrows():
        print(f"{row['sku']:<6} {row['department']:<25} {row['z_score']:<4.2f} {row['demand_std']:<8.2f} "
              f"{row['calculated_ss']:<8.1f} {row['actual_ss']:<9.1f} {row['error_pct']:<8.1f} {row['data_points']:<8}")
    
    return df_sorted

def main():
    """Main execution function"""
    print("🔍 Safety Stock Calculator")
    print("Formula: Safety Stock = Z-score × Historical Demand Standard Deviation")
    print("=" * 70)
    
    # Load data
    test_data, demand_data = load_validation_data()
    
    # Calculate safety stock for all combinations
    results = calculate_safety_stock(test_data, demand_data)
    
    # Analyze results
    df = analyze_results(results)
    
    if df is not None and len(df) > 0:
        # Create detailed report
        df_sorted = create_detailed_report(df)
        
        # Save results
        df_sorted.to_csv('scripts/safety_stock_calculations.csv', index=False)
        
        print(f"\n" + "="*60)
        print("CONCLUSION")
        print("="*60)
        
        overall_mape = df['error_pct'].mean()
        within_20_pct = (df['error_pct'] <= 20).sum()
        total_results = len(df)
        
        if overall_mape < 30 and within_20_pct / total_results > 0.5:
            print("✅ SUCCESS: The formula 'Safety Stock = Z-score × Historical Demand Standard Deviation'")
            print("   provides good accuracy for most SKU-department combinations.")
        else:
            print("⚠️  PARTIAL SUCCESS: The formula works for some combinations but may need refinement.")
        
        print(f"\nResults saved to: scripts/safety_stock_calculations.csv")
    else:
        print("\n❌ No valid results generated. Check data availability.")

if __name__ == "__main__":
    main()
