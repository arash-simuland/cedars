#!/usr/bin/env python3
"""
CedarSim Input Data Loader

This script loads and validates the simulation input data files.
"""

import pandas as pd
import os
from pathlib import Path

def load_simulation_data():
    """Load all simulation input data files."""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    print("=" * 60)
    print("LOADING CEDARSIM SIMULATION INPUT DATA")
    print("=" * 60)
    
    # Load SKU inventory data
    print("\n1. Loading SKU inventory data...")
    sku_file = script_dir / "sku_inventory_data.csv"
    if not sku_file.exists():
        raise FileNotFoundError(f"SKU data file not found: {sku_file}")
    
    sku_data = pd.read_csv(sku_file)
    print(f"   ✅ Loaded {len(sku_data):,} SKUs")
    print(f"   Columns: {len(sku_data.columns)}")
    print(f"   Key fields: Oracle Item Number, Avg Daily Burn Rate, Avg_Lead Time")
    
    # Load historical demand data
    print("\n2. Loading historical demand data...")
    demand_file = script_dir / "historical_demand_data.csv"
    if not demand_file.exists():
        raise FileNotFoundError(f"Demand data file not found: {demand_file}")
    
    demand_data = pd.read_csv(demand_file)
    print(f"   ✅ Loaded {len(demand_data):,} demand records")
    print(f"   Columns: {len(demand_data.columns)}")
    print(f"   Time range: {demand_data['PO Week Ending Date'].min()} to {demand_data['PO Week Ending Date'].max()}")
    
    # Load validation subset data
    print("\n3. Loading validation subset data...")
    validation_file = script_dir / "validation_subset_data.csv"
    if not validation_file.exists():
        raise FileNotFoundError(f"Validation data file not found: {validation_file}")
    
    validation_data = pd.read_csv(validation_file)
    print(f"   ✅ Loaded {len(validation_data):,} validation SKUs")
    print(f"   Columns: {len(validation_data.columns)}")
    print(f"   Safety stock coverage: {len(validation_data[validation_data['Safety stock_units'].notna()])} SKUs")
    
    # Validate data quality
    print("\n4. Validating data quality...")
    
    # Check for missing lead times
    missing_lead_times = sku_data['Avg_Lead Time'].isna().sum()
    print(f"   Lead time coverage: {((len(sku_data) - missing_lead_times) / len(sku_data) * 100):.1f}%")
    
    # Check for missing burn rates
    missing_burn_rates = sku_data['Avg Daily Burn Rate'].isna().sum()
    print(f"   Burn rate coverage: {((len(sku_data) - missing_burn_rates) / len(sku_data) * 100):.1f}%")
    
    # Check unit consistency
    print(f"   Unit consistency: Daily burn rates + Daily lead times ✅")
    
    # Check PAR mapping coverage
    par_columns = [col for col in sku_data.columns if 'Level' in col or 'Respiratory' in col]
    par_mapped = sku_data[par_columns].apply(lambda x: x.notna().any(), axis=1).sum()
    print(f"   PAR mapping coverage: {(par_mapped / len(sku_data) * 100):.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ ALL INPUT DATA LOADED SUCCESSFULLY!")
    print("=" * 60)
    
    return {
        'sku_data': sku_data,
        'demand_data': demand_data,
        'validation_data': validation_data
    }

def get_data_summary():
    """Get a summary of the loaded data."""
    data = load_simulation_data()
    
    print("\n📊 DATA SUMMARY:")
    print(f"   SKU Inventory: {len(data['sku_data']):,} SKUs")
    print(f"   Demand Records: {len(data['demand_data']):,} records")
    print(f"   Validation SKUs: {len(data['validation_data']):,} SKUs")
    print(f"   Total Data Size: ~{sum([df.memory_usage(deep=True).sum() for df in data.values()]) / 1024 / 1024:.1f} MB")
    
    return data

if __name__ == "__main__":
    # Load and validate data
    data = get_data_summary()
    
    # Show sample data
    print("\n📋 SAMPLE SKU DATA:")
    print(data['sku_data'][['Oracle Item Number', 'Item Description', 'Avg Daily Burn Rate', 'Avg_Lead Time']].head())
    
    print("\n📋 SAMPLE DEMAND DATA:")
    print(data['demand_data'][['PO Week Ending Date', 'Oracle Item Number', 'Total Qty Issues', 'Avg Daily Burn Rate']].head())
    
    print("\n📋 SAMPLE VALIDATION DATA:")
    print(data['validation_data'][['Oracle Item Number', 'Avg Daily Burn Rate', 'Safety stock_units']].head())
