#!/usr/bin/env python3
import pandas as pd
import numpy as np
from pathlib import Path

print("=== Testing Data Loading ===")

# Check if data files exist
data_dir = Path('data')
inventory_file = data_dir / '2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx'
validation_file = data_dir / '2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx'

print(f"Data directory exists: {data_dir.exists()}")
print(f"Inventory file exists: {inventory_file.exists()}")
print(f"Validation file exists: {validation_file.exists()}")

if inventory_file.exists():
    print("\nLoading inventory file...")
    try:
        # Get sheet names first
        xl_file = pd.ExcelFile(inventory_file)
        print(f"Sheet names: {xl_file.sheet_names}")
        
        # Load first sheet
        sku_data = pd.read_excel(inventory_file, sheet_name=0)
        print(f"SKU data shape: {sku_data.shape}")
        print(f"Columns: {list(sku_data.columns)}")
        
    except Exception as e:
        print(f"Error loading inventory file: {e}")

if validation_file.exists():
    print("\nLoading validation file...")
    try:
        validation_data = pd.read_excel(validation_file)
        print(f"Validation data shape: {validation_data.shape}")
        print(f"Columns: {list(validation_data.columns)}")
    except Exception as e:
        print(f"Error loading validation file: {e}")

print("\n=== Test Complete ===")
