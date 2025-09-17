#!/usr/bin/env python3
"""
CedarSim Validation Subset Data Loader

This script loads the validation subset data that matches exactly the test SKUs
and time range for fair comparison between simulation and analytical results.
"""

import pandas as pd
import os
from pathlib import Path

def load_validation_subset_data():
    """Load validation subset data for fair comparison testing."""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    print("=" * 60)
    print("LOADING CEDARSIM VALIDATION SUBSET DATA")
    print("=" * 60)
    
    # Load validation subset SKU inventory data
    print("\n1. Loading validation subset SKU data...")
    sku_file = script_dir / "validation_sku_subset.csv"
    if not sku_file.exists():
        raise FileNotFoundError(f"Validation SKU data file not found: {sku_file}")
    
    sku_data = pd.read_csv(sku_file)
    print(f"   ✅ Loaded {len(sku_data):,} validation SKUs")
    print(f"   Columns: {len(sku_data.columns)}")
    print(f"   Key fields: Oracle Item Number, Avg Daily Burn Rate, Avg_Lead Time")
    
    # Load validation subset demand data
    print("\n2. Loading validation subset demand data...")
    demand_file = script_dir / "validation_demand_subset.csv"
    if not demand_file.exists():
        raise FileNotFoundError(f"Validation demand data file not found: {demand_file}")
    
    demand_data = pd.read_csv(demand_file)
    print(f"   ✅ Loaded {len(demand_data):,} validation demand records")
    print(f"   Columns: {len(demand_data.columns)}")
    print(f"   Time range: {demand_data['PO Week Ending Date'].min()} to {demand_data['PO Week Ending Date'].max()}")
    
    # Load validation test data (analytical results)
    print("\n3. Loading validation test data...")
    validation_file = script_dir / "validation_test_data.csv"
    if not validation_file.exists():
        raise FileNotFoundError(f"Validation test data file not found: {validation_file}")
    
    validation_data = pd.read_csv(validation_file)
    print(f"   ✅ Loaded {len(validation_data):,} validation test records")
    print(f"   Columns: {len(validation_data.columns)}")
    print(f"   Safety stock coverage: {len(validation_data[validation_data['Safety stock_units'].notna()])} SKUs")
    
    # Validate data quality
    print("\n4. Validating validation subset data quality...")
    
    # Check for missing lead times
    missing_lead_times = sku_data['Avg_Lead Time'].isna().sum()
    print(f"   Lead time coverage: {((len(sku_data) - missing_lead_times) / len(sku_data) * 100):.1f}%")
    
    # Check for missing burn rates
    missing_burn_rates = sku_data['Avg Daily Burn Rate'].isna().sum()
    print(f"   Burn rate coverage: {((len(sku_data) - missing_burn_rates) / len(sku_data) * 100):.1f}%")
    
    # Check SKU coverage
    sku_skus = set(sku_data['Oracle Item Number'].unique())
    demand_skus = set(demand_data['Oracle Item Number'].unique())
    validation_skus = set(validation_data['Oracle Item Number'].unique())
    
    print(f"   SKU data SKUs: {len(sku_skus)}")
    print(f"   Demand data SKUs: {len(demand_skus)}")
    print(f"   Validation test SKUs: {len(validation_skus)}")
    
    # Check overlap
    sku_demand_overlap = sku_skus.intersection(demand_skus)
    sku_validation_overlap = sku_skus.intersection(validation_skus)
    demand_validation_overlap = demand_skus.intersection(validation_skus)
    
    print(f"   SKU-Demand overlap: {len(sku_demand_overlap)} SKUs")
    print(f"   SKU-Validation overlap: {len(sku_validation_overlap)} SKUs")
    print(f"   Demand-Validation overlap: {len(demand_validation_overlap)} SKUs")
    
    # Check PAR mapping coverage
    par_columns = [col for col in sku_data.columns if 'Level' in col or 'Respiratory' in col]
    par_mapped = sku_data[par_columns].apply(lambda x: x.notna().any(), axis=1).sum()
    print(f"   PAR mapping coverage: {(par_mapped / len(sku_data) * 100):.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ VALIDATION SUBSET DATA LOADED SUCCESSFULLY!")
    print("=" * 60)
    
    return {
        'sku_data': sku_data,
        'demand_data': demand_data,
        'validation_data': validation_data
    }

def get_validation_subset_summary():
    """Get a summary of the validation subset data."""
    data = load_validation_subset_data()
    
    print("\n📊 VALIDATION SUBSET SUMMARY:")
    print(f"   SKU Inventory: {len(data['sku_data']):,} SKUs")
    print(f"   Demand Records: {len(data['demand_data']):,} records")
    print(f"   Validation Test: {len(data['validation_data']):,} records")
    print(f"   Total Data Size: ~{sum([df.memory_usage(deep=True).sum() for df in data.values()]) / 1024 / 1024:.1f} MB")
    
    # Show time range
    demand_data = data['demand_data']
    print(f"   Time Range: {demand_data['PO Week Ending Date'].min()} to {demand_data['PO Week Ending Date'].max()}")
    
    # Show SKU coverage
    sku_skus = set(data['sku_data']['Oracle Item Number'].unique())
    demand_skus = set(data['demand_data']['Oracle Item Number'].unique())
    validation_skus = set(data['validation_data']['Oracle Item Number'].unique())
    
    print(f"   SKUs with demand data: {len(sku_skus.intersection(demand_skus))}")
    print(f"   SKUs with validation data: {len(sku_skus.intersection(validation_skus))}")
    
    return data

if __name__ == "__main__":
    # Load and validate validation subset data
    data = get_validation_subset_summary()
    
    # Show sample data
    print("\n📋 SAMPLE VALIDATION SKU DATA:")
    print(data['sku_data'][['Oracle Item Number', 'Item Description', 'Avg Daily Burn Rate', 'Avg_Lead Time']].head())
    
    print("\n📋 SAMPLE VALIDATION DEMAND DATA:")
    print(data['demand_data'][['PO Week Ending Date', 'Oracle Item Number', 'Total Qty Issues', 'Avg Daily Burn Rate']].head())
    
    print("\n📋 SAMPLE VALIDATION TEST DATA:")
    print(data['validation_data'][['Oracle Item Number', 'Avg Daily Burn Rate', 'Safety stock_units']].head())
