#!/usr/bin/env python3
"""
Fix SKU Alignment Script
========================

The issue is that the main datasets use zero-padded SKU numbers (e.g., '00136')
while the test data uses unpadded numbers (e.g., 136).

This script fixes the alignment by converting SKU numbers to the correct format.
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
    """Load main datasets"""
    print("\nLoading main datasets...")
    
    sku_main = pd.read_excel('data/final/CedarSim_Simulation_Ready_Data_Final.xlsx', 
                            sheet_name='01_SKU_Inventory_Final')
    demand_main = pd.read_excel('data/final/CedarSim_Simulation_Ready_Data_Final.xlsx', 
                               sheet_name='02_Demand_Data_Clean')
    
    print(f"Main SKU data: {len(sku_main)} rows, {sku_main['Oracle Item Number'].nunique()} unique SKUs")
    print(f"Main demand data: {len(demand_main)} rows, {demand_main['Oracle Item Number'].nunique()} unique SKUs")
    
    return sku_main, demand_main

def convert_sku_format(df, sku_column='Oracle Item Number'):
    """Convert SKU numbers to consistent format"""
    print(f"Converting SKU format in {sku_column}...")
    
    # Convert to string and zero-pad to 5 digits
    df[sku_column] = df[sku_column].astype(str).str.zfill(5)
    
    return df

def find_matching_skus(test_data, sku_main, demand_main):
    """Find matching SKUs in main datasets"""
    print("\nFinding matching SKUs...")
    
    # Get test SKUs and convert to zero-padded format
    test_skus = set(test_data['Oracle Item Number'].astype(str).str.zfill(5).unique())
    print(f"Test SKUs (zero-padded): {sorted(test_skus)}")
    
    # Get main dataset SKUs
    sku_main_skus = set(sku_main['Oracle Item Number'].astype(str).unique())
    demand_main_skus = set(demand_main['Oracle Item Number'].astype(str).unique())
    
    # Find matches
    sku_matches = test_skus.intersection(sku_main_skus)
    demand_matches = test_skus.intersection(demand_main_skus)
    
    print(f"SKUs found in main SKU data: {len(sku_matches)}")
    print(f"SKUs found in main demand data: {len(demand_matches)}")
    
    return sku_matches, demand_matches

def extract_matching_data(sku_main, demand_main, sku_matches, demand_matches):
    """Extract matching data from main datasets"""
    print("\nExtracting matching data...")
    
    # Convert main datasets to zero-padded format
    sku_main = sku_main.copy()
    demand_main = demand_main.copy()
    sku_main['Oracle Item Number'] = sku_main['Oracle Item Number'].astype(str).str.zfill(5)
    demand_main['Oracle Item Number'] = demand_main['Oracle Item Number'].astype(str).str.zfill(5)
    
    # Extract matching SKU data
    matching_sku_data = sku_main[sku_main['Oracle Item Number'].isin(sku_matches)].copy()
    print(f"Extracted {len(matching_sku_data)} rows of SKU data")
    
    # Extract matching demand data
    matching_demand_data = demand_main[demand_main['Oracle Item Number'].isin(demand_matches)].copy()
    print(f"Extracted {len(matching_demand_data)} rows of demand data")
    
    return matching_sku_data, matching_demand_data

def create_aligned_files(test_data, sku_data, demand_data, matching_sku_data, matching_demand_data):
    """Create aligned files with consistent SKU format"""
    print("\nCreating aligned files...")
    
    # Convert test data SKUs to zero-padded format
    test_data_aligned = test_data.copy()
    test_data_aligned['Oracle Item Number'] = test_data_aligned['Oracle Item Number'].astype(str).str.zfill(5)
    
    # Convert existing SKU data to zero-padded format
    sku_data_aligned = sku_data.copy()
    sku_data_aligned['Oracle Item Number'] = sku_data_aligned['Oracle Item Number'].astype(str).str.zfill(5)
    
    # Convert existing demand data to zero-padded format
    demand_data_aligned = demand_data.copy()
    demand_data_aligned['Oracle Item Number'] = demand_data_aligned['Oracle Item Number'].astype(str).str.zfill(5)
    
    # Combine with matching data
    final_sku_data = pd.concat([sku_data_aligned, matching_sku_data], ignore_index=True)
    final_demand_data = pd.concat([demand_data_aligned, matching_demand_data], ignore_index=True)
    
    # Remove duplicates
    final_sku_data = final_sku_data.drop_duplicates(subset=['Oracle Item Number'])
    final_demand_data = final_demand_data.drop_duplicates()
    
    print(f"Final SKU data: {len(final_sku_data)} rows, {final_sku_data['Oracle Item Number'].nunique()} unique SKUs")
    print(f"Final demand data: {len(final_demand_data)} rows, {final_demand_data['Oracle Item Number'].nunique()} unique SKUs")
    
    return test_data_aligned, final_sku_data, final_demand_data

def verify_alignment(test_data, sku_data, demand_data):
    """Verify that all files have the same SKUs"""
    print("\nVerifying alignment...")
    
    test_skus = set(test_data['Oracle Item Number'].unique())
    sku_skus = set(sku_data['Oracle Item Number'].unique())
    demand_skus = set(demand_data['Oracle Item Number'].unique())
    
    print(f"Test data SKUs: {len(test_skus)}")
    print(f"SKU data SKUs: {len(sku_skus)}")
    print(f"Demand data SKUs: {len(demand_skus)}")
    
    all_aligned = test_skus == sku_skus == demand_skus
    print(f"All SKUs aligned: {all_aligned}")
    
    if not all_aligned:
        print("Missing SKUs in SKU data:", test_skus - sku_skus)
        print("Missing SKUs in demand data:", test_skus - demand_skus)
    
    return all_aligned

def save_aligned_files(test_data, sku_data, demand_data):
    """Save the aligned files"""
    print("\nSaving aligned files...")
    
    # Create backup
    backup_dir = 'data/final/validation_subset/backup'
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save aligned files
    test_data.to_csv('data/final/validation_subset/validation_test_data.csv', index=False)
    sku_data.to_csv('data/final/validation_subset/validation_sku_subset.csv', index=False)
    demand_data.to_csv('data/final/validation_subset/validation_demand_subset.csv', index=False)
    
    print("✅ Aligned files saved successfully!")

def main():
    """Main execution function"""
    print("🔧 Fixing SKU Alignment")
    print("=" * 50)
    
    # Load data
    test_data, sku_data, demand_data = load_validation_data()
    sku_main, demand_main = load_main_datasets()
    
    # Find matching SKUs
    sku_matches, demand_matches = find_matching_skus(test_data, sku_main, demand_main)
    
    # Extract matching data
    matching_sku_data, matching_demand_data = extract_matching_data(sku_main, demand_main, sku_matches, demand_matches)
    
    # Create aligned files
    test_data_aligned, final_sku_data, final_demand_data = create_aligned_files(
        test_data, sku_data, demand_data, matching_sku_data, matching_demand_data
    )
    
    # Verify alignment
    all_aligned = verify_alignment(test_data_aligned, final_sku_data, final_demand_data)
    
    if all_aligned:
        # Save aligned files
        save_aligned_files(test_data_aligned, final_sku_data, final_demand_data)
        print("\n🎯 SKU Alignment Complete!")
        print("All three validation files now contain the same SKUs with consistent formatting.")
    else:
        print("\n❌ Alignment failed. Some SKUs are still missing from the main datasets.")

if __name__ == "__main__":
    main()
