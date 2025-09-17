#!/usr/bin/env python3
"""
Align Validation Data Script
============================

This script uses the test data as the main reference (24 SKUs) and ensures
the SKU and demand data files contain the same SKUs.

Test data contains 24 SKUs with safety stock values - this is our master list.
We need to extract the missing SKUs from the main datasets.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_validation_data():
    """Load current validation data files"""
    print("Loading current validation data...")
    
    test_data = pd.read_csv('data/final/validation_subset/validation_test_data.csv')
    sku_data = pd.read_csv('data/final/validation_subset/validation_sku_subset.csv')
    demand_data = pd.read_csv('data/final/validation_subset/validation_demand_subset.csv')
    
    print(f"Test data: {len(test_data)} rows, {test_data['Oracle Item Number'].nunique()} unique SKUs")
    print(f"SKU data: {len(sku_data)} rows, {sku_data['Oracle Item Number'].nunique()} unique SKUs")
    print(f"Demand data: {len(demand_data)} rows, {demand_data['Oracle Item Number'].nunique()} unique SKUs")
    
    return test_data, sku_data, demand_data

def load_main_datasets():
    """Load main datasets to extract missing data"""
    print("\nLoading main datasets...")
    
    # Load main SKU data
    sku_main = pd.read_excel('data/final/CedarSim_Simulation_Ready_Data_Final.xlsx', 
                            sheet_name='01_SKU_Inventory_Final')
    print(f"Main SKU data: {len(sku_main)} rows, {sku_main['Oracle Item Number'].nunique()} unique SKUs")
    
    # Load main demand data
    demand_main = pd.read_excel('data/final/CedarSim_Simulation_Ready_Data_Final.xlsx', 
                               sheet_name='02_Demand_Data_Clean')
    print(f"Main demand data: {len(demand_main)} rows, {demand_main['Oracle Item Number'].nunique()} unique SKUs")
    
    return sku_main, demand_main

def identify_missing_skus(test_data, sku_data, demand_data):
    """Identify which SKUs are missing from each file"""
    print("\nIdentifying missing SKUs...")
    
    test_skus = set(test_data['Oracle Item Number'].unique())
    sku_skus = set(sku_data['Oracle Item Number'].unique())
    demand_skus = set(demand_data['Oracle Item Number'].unique())
    
    missing_from_sku = test_skus - sku_skus
    missing_from_demand = test_skus - demand_skus
    
    print(f"SKUs missing from SKU data: {len(missing_from_sku)}")
    print(f"Missing SKU numbers: {sorted(missing_from_sku)}")
    
    print(f"SKUs missing from demand data: {len(missing_from_demand)}")
    print(f"Missing demand numbers: {sorted(missing_from_demand)}")
    
    return missing_from_sku, missing_from_demand

def extract_missing_sku_data(sku_main, missing_skus):
    """Extract missing SKU data from main dataset"""
    print(f"\nExtracting missing SKU data for {len(missing_skus)} SKUs...")
    
    # Filter main SKU data for missing SKUs
    missing_sku_data = sku_main[sku_main['Oracle Item Number'].isin(missing_skus)].copy()
    
    print(f"Found {len(missing_sku_data)} rows for missing SKUs")
    
    if len(missing_sku_data) > 0:
        print("Sample missing SKU data:")
        print(missing_sku_data[['Oracle Item Number', 'Item Description', 'Avg Daily Burn Rate', 'Avg_Lead Time']].head())
    
    return missing_sku_data

def extract_missing_demand_data(demand_main, missing_skus):
    """Extract missing demand data from main dataset"""
    print(f"\nExtracting missing demand data for {len(missing_skus)} SKUs...")
    
    # Filter main demand data for missing SKUs
    missing_demand_data = demand_main[demand_main['Oracle Item Number'].isin(missing_skus)].copy()
    
    print(f"Found {len(missing_demand_data)} rows for missing SKUs")
    
    if len(missing_demand_data) > 0:
        print("Sample missing demand data:")
        print(missing_demand_data[['PO Week Ending Date', 'Oracle Item Number', 'Item Description', 'Total Qty PO']].head())
    
    return missing_demand_data

def create_aligned_files(test_data, sku_data, demand_data, missing_sku_data, missing_demand_data):
    """Create new aligned validation files with all 24 SKUs"""
    print("\nCreating aligned validation files...")
    
    # Create aligned SKU data
    aligned_sku_data = pd.concat([sku_data, missing_sku_data], ignore_index=True)
    print(f"Aligned SKU data: {len(aligned_sku_data)} rows, {aligned_sku_data['Oracle Item Number'].nunique()} unique SKUs")
    
    # Create aligned demand data
    aligned_demand_data = pd.concat([demand_data, missing_demand_data], ignore_index=True)
    print(f"Aligned demand data: {len(aligned_demand_data)} rows, {aligned_demand_data['Oracle Item Number'].nunique()} unique SKUs")
    
    # Verify alignment
    test_skus = set(test_data['Oracle Item Number'].unique())
    sku_skus = set(aligned_sku_data['Oracle Item Number'].unique())
    demand_skus = set(aligned_demand_data['Oracle Item Number'].unique())
    
    print(f"\nAlignment verification:")
    print(f"Test data SKUs: {len(test_skus)}")
    print(f"Aligned SKU data SKUs: {len(sku_skus)}")
    print(f"Aligned demand data SKUs: {len(demand_skus)}")
    print(f"All SKUs aligned: {test_skus == sku_skus == demand_skus}")
    
    return aligned_sku_data, aligned_demand_data

def save_aligned_files(test_data, aligned_sku_data, aligned_demand_data):
    """Save the aligned files"""
    print("\nSaving aligned files...")
    
    # Create backup of original files
    backup_dir = 'data/final/validation_subset/backup'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup original files
    test_data.to_csv(f'{backup_dir}/validation_test_data_backup_{timestamp}.csv', index=False)
    print(f"Backed up test data to {backup_dir}/validation_test_data_backup_{timestamp}.csv")
    
    # Save aligned files
    aligned_sku_data.to_csv('data/final/validation_subset/validation_sku_subset.csv', index=False)
    aligned_demand_data.to_csv('data/final/validation_subset/validation_demand_subset.csv', index=False)
    
    print("✅ Aligned files saved successfully!")
    print("✅ All three files now contain the same 24 SKUs")

def main():
    """Main execution function"""
    print("🔍 Aligning Validation Data Files")
    print("=" * 50)
    
    # Load current validation data
    test_data, sku_data, demand_data = load_validation_data()
    
    # Load main datasets
    sku_main, demand_main = load_main_datasets()
    
    # Identify missing SKUs
    missing_from_sku, missing_from_demand = identify_missing_skus(test_data, sku_data, demand_data)
    
    # Extract missing data
    missing_sku_data = extract_missing_sku_data(sku_main, missing_from_sku)
    missing_demand_data = extract_missing_demand_data(demand_main, missing_from_demand)
    
    # Create aligned files
    aligned_sku_data, aligned_demand_data = create_aligned_files(
        test_data, sku_data, demand_data, missing_sku_data, missing_demand_data
    )
    
    # Save aligned files
    save_aligned_files(test_data, aligned_sku_data, aligned_demand_data)
    
    print("\n🎯 Alignment Complete!")
    print("All three validation files now contain the same 24 SKUs from the test data.")

if __name__ == "__main__":
    main()
