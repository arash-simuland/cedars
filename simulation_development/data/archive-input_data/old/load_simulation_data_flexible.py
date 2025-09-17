#!/usr/bin/env python3
"""
CedarSim Flexible Data Loader

This script provides flexible data loading options:
1. Validation subset mode: Only validation SKUs for testing against analytical solution
2. Full dataset mode: All SKUs but same time range as validation test
3. Complete mode: All SKUs with full historical time range
"""

import pandas as pd
import os
from pathlib import Path

def load_simulation_data(mode='validation_subset'):
    """
    Load simulation data based on the specified mode.
    
    Args:
        mode (str): Data loading mode
            - 'validation_subset': Only validation SKUs (24 SKUs) for testing
            - 'full_time_range': All SKUs but same time range as validation (2022-2025)
            - 'complete': All SKUs with full historical time range (2019-2025)
    """
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    print("=" * 80)
    print(f"LOADING CEDARSIM SIMULATION DATA - {mode.upper()} MODE")
    print("=" * 80)
    
    if mode == 'validation_subset':
        return _load_validation_subset(script_dir)
    elif mode == 'full_time_range':
        return _load_full_time_range(script_dir)
    elif mode == 'complete':
        return _load_complete_dataset(script_dir)
    else:
        raise ValueError(f"Invalid mode: {mode}. Use 'validation_subset', 'full_time_range', or 'complete'")

def _load_validation_subset(script_dir):
    """Load only validation SKUs for testing against analytical solution."""
    
    print("\n🎯 VALIDATION SUBSET MODE - Testing against analytical solution")
    print("   SKUs: 24 validation SKUs only")
    print("   Time Range: 2022-01-02 to 2025-07-06")
    print("   Purpose: Compare simulation vs analytical results")
    
    # Load validation subset data
    sku_file = script_dir / "validation_sku_subset.csv"
    demand_file = script_dir / "validation_demand_subset.csv"
    validation_file = script_dir / "validation_test_data.csv"
    
    if not all([sku_file.exists(), demand_file.exists(), validation_file.exists()]):
        raise FileNotFoundError("Validation subset files not found. Run create_validation_subset.py first.")
    
    sku_data = pd.read_csv(sku_file)
    demand_data = pd.read_csv(demand_file)
    validation_data = pd.read_csv(validation_file)
    
    print(f"   ✅ SKU data: {len(sku_data):,} records")
    print(f"   ✅ Demand data: {len(demand_data):,} records")
    print(f"   ✅ Validation data: {len(validation_data):,} records")
    
    return {
        'sku_data': sku_data,
        'demand_data': demand_data,
        'validation_data': validation_data,
        'mode': 'validation_subset',
        'description': 'Validation subset for testing against analytical solution'
    }

def _load_full_time_range(script_dir):
    """Load all SKUs but filter to validation test time range."""
    
    print("\n🌍 FULL TIME RANGE MODE - All SKUs, validation time range")
    print("   SKUs: All 5,941 SKUs")
    print("   Time Range: 2022-01-02 to 2025-07-06 (same as validation)")
    print("   Purpose: Full simulation with consistent time range")
    
    # Load complete datasets
    sku_file = script_dir / "sku_inventory_data.csv"
    demand_file = script_dir / "historical_demand_data.csv"
    validation_file = script_dir / "validation_subset_data.csv"
    
    if not all([sku_file.exists(), demand_file.exists()]):
        raise FileNotFoundError("Complete dataset files not found.")
    
    sku_data = pd.read_csv(sku_file)
    demand_data = pd.read_csv(demand_file)
    
    # Filter demand data to validation time range
    demand_data['PO Week Ending Date'] = pd.to_datetime(demand_data['PO Week Ending Date'])
    validation_start = pd.to_datetime('2022-01-02')
    validation_end = pd.to_datetime('2025-07-06')
    
    demand_data = demand_data[
        (demand_data['PO Week Ending Date'] >= validation_start) & 
        (demand_data['PO Week Ending Date'] <= validation_end)
    ].copy()
    
    # Load validation data if available
    validation_data = None
    if validation_file.exists():
        validation_data = pd.read_csv(validation_file)
        print(f"   ✅ Validation data: {len(validation_data):,} records")
    else:
        print("   ⚠️  Validation data not available")
    
    print(f"   ✅ SKU data: {len(sku_data):,} records")
    print(f"   ✅ Demand data: {len(demand_data):,} records (filtered to validation time range)")
    
    return {
        'sku_data': sku_data,
        'demand_data': demand_data,
        'validation_data': validation_data,
        'mode': 'full_time_range',
        'description': 'All SKUs with validation test time range'
    }

def _load_complete_dataset(script_dir):
    """Load complete dataset with full historical time range."""
    
    print("\n🚀 COMPLETE MODE - All SKUs, full historical time range")
    print("   SKUs: All 5,941 SKUs")
    print("   Time Range: 2019-12-15 to 2025-07-06 (full historical)")
    print("   Purpose: Full-scale simulation with complete historical data")
    
    # Load complete datasets
    sku_file = script_dir / "sku_inventory_data.csv"
    demand_file = script_dir / "historical_demand_data.csv"
    validation_file = script_dir / "validation_subset_data.csv"
    
    if not all([sku_file.exists(), demand_file.exists()]):
        raise FileNotFoundError("Complete dataset files not found.")
    
    sku_data = pd.read_csv(sku_file)
    demand_data = pd.read_csv(demand_file)
    
    # Load validation data if available
    validation_data = None
    if validation_file.exists():
        validation_data = pd.read_csv(validation_file)
        print(f"   ✅ Validation data: {len(validation_data):,} records")
    else:
        print("   ⚠️  Validation data not available")
    
    print(f"   ✅ SKU data: {len(sku_data):,} records")
    print(f"   ✅ Demand data: {len(demand_data):,} records (full historical range)")
    
    return {
        'sku_data': sku_data,
        'demand_data': demand_data,
        'validation_data': validation_data,
        'mode': 'complete',
        'description': 'Complete dataset with full historical time range'
    }

def get_data_summary(mode='validation_subset'):
    """Get a summary of the loaded data for the specified mode."""
    data = load_simulation_data(mode)
    
    print(f"\n📊 DATA SUMMARY - {mode.upper()} MODE:")
    print(f"   SKU Inventory: {len(data['sku_data']):,} SKUs")
    print(f"   Demand Records: {len(data['demand_data']):,} records")
    if data['validation_data'] is not None:
        print(f"   Validation Test: {len(data['validation_data']):,} records")
    print(f"   Mode: {data['mode']}")
    print(f"   Description: {data['description']}")
    
    # Show time range
    demand_data = data['demand_data']
    if 'PO Week Ending Date' in demand_data.columns:
        time_range = demand_data['PO Week Ending Date']
        print(f"   Time Range: {time_range.min()} to {time_range.max()}")
    
    # Show SKU coverage
    sku_skus = set(data['sku_data']['Oracle Item Number'].unique())
    demand_skus = set(data['demand_data']['Oracle Item Number'].unique())
    print(f"   SKUs with demand data: {len(sku_skus.intersection(demand_skus))}")
    
    return data

def create_time_range_subset():
    """Create a subset of all SKUs with validation test time range."""
    
    print("=" * 80)
    print("CREATING FULL TIME RANGE SUBSET")
    print("=" * 80)
    
    # Load complete datasets
    sku_data = pd.read_csv('data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv')
    demand_data = pd.read_csv('data/final/csv_complete/02_Demand_Data_Clean_Complete.csv')
    
    print(f"   Original SKU data: {len(sku_data):,} SKUs")
    print(f"   Original demand data: {len(demand_data):,} records")
    
    # Filter demand data to validation time range
    demand_data['PO Week Ending Date'] = pd.to_datetime(demand_data['PO Week Ending Date'])
    validation_start = pd.to_datetime('2022-01-02')
    validation_end = pd.to_datetime('2025-07-06')
    
    filtered_demand = demand_data[
        (demand_data['PO Week Ending Date'] >= validation_start) & 
        (demand_data['PO Week Ending Date'] <= validation_end)
    ].copy()
    
    print(f"   Filtered demand data: {len(filtered_demand):,} records")
    print(f"   Time range: {filtered_demand['PO Week Ending Date'].min()} to {filtered_demand['PO Week Ending Date'].max()}")
    
    # Create output directory
    output_dir = Path('data/final/full_time_range_subset')
    output_dir.mkdir(exist_ok=True)
    
    # Save subset files
    sku_output = output_dir / 'full_sku_data.csv'
    demand_output = output_dir / 'full_demand_data.csv'
    
    sku_data.to_csv(sku_output, index=False)
    filtered_demand.to_csv(demand_output, index=False)
    
    print(f"   ✅ Saved: {sku_output}")
    print(f"   ✅ Saved: {demand_output}")
    
    # Copy to simulation development directory
    import shutil
    shutil.copy2(sku_output, 'simulation_development/data/input_data/full_sku_data.csv')
    shutil.copy2(demand_output, 'simulation_development/data/input_data/full_demand_data.csv')
    
    print(f"   ✅ Copied to simulation development directory")
    
    print("\n" + "=" * 80)
    print("✅ FULL TIME RANGE SUBSET CREATED!")
    print("=" * 80)
    
    return {
        'sku_data': sku_data,
        'demand_data': filtered_demand,
        'time_range': f"{filtered_demand['PO Week Ending Date'].min()} to {filtered_demand['PO Week Ending Date'].max()}"
    }

if __name__ == "__main__":
    # Test all modes
    print("Testing all data loading modes...\n")
    
    # Test validation subset mode
    print("1. Testing validation subset mode:")
    try:
        data = get_data_summary('validation_subset')
        print("   ✅ Validation subset mode working\n")
    except Exception as e:
        print(f"   ❌ Validation subset mode failed: {e}\n")
    
    # Test full time range mode
    print("2. Testing full time range mode:")
    try:
        data = get_data_summary('full_time_range')
        print("   ✅ Full time range mode working\n")
    except Exception as e:
        print(f"   ❌ Full time range mode failed: {e}\n")
    
    # Test complete mode
    print("3. Testing complete mode:")
    try:
        data = get_data_summary('complete')
        print("   ✅ Complete mode working\n")
    except Exception as e:
        print(f"   ❌ Complete mode failed: {e}\n")
