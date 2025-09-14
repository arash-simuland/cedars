#!/usr/bin/env python3
"""
Convert New Data to Complete CSV Format
======================================

This script takes the new Excel format data and merges it with the existing
complete data to create updated CSV files in the csv_complete format.

What it does:
1. Loads new data from 2025-09-12_MDRH_Item_List.xlsx
2. Loads existing complete data from csv_complete folder
3. Merges them, preserving all existing fields and updating burn rates/lead times
4. Outputs updated CSV files in the same csv_complete format
"""

import sys
from pathlib import Path
import pandas as pd

# Add the scripts directory to the path so we can import the converter
sys.path.append('scripts/data_processing')

from new_excel_converter import CedarSimDataConverter

def main():
    print("=" * 60)
    print("CONVERTING NEW DATA TO COMPLETE CSV FORMAT")
    print("=" * 60)
    
    # File paths
    new_data_file = "data/archive/original/2025-09-12_MDRH_Item_List.xlsx"
    existing_data_file = "data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv"
    
    # Check if files exist
    if not Path(new_data_file).exists():
        print(f"❌ ERROR: New data file not found: {new_data_file}")
        return False
    
    if not Path(existing_data_file).exists():
        print(f"❌ ERROR: Existing data file not found: {existing_data_file}")
        return False
    
    print(f"✅ Found new data file: {new_data_file}")
    print(f"✅ Found existing data file: {existing_data_file}")
    
    # Create converter
    print("\n🔄 Creating converter...")
    converter = CedarSimDataConverter(existing_data_file)
    
    # Convert the data
    print("🔄 Converting and merging data...")
    merged_data = converter.convert_new_data(
        new_data_file,
        handle_new_items=False,  # Don't add new items, just update existing ones
        exclude_new_items=True   # Exclude new items from simulation
    )
    
    # Save the updated data back to csv_complete format
    print("🔄 Saving updated data...")
    
    # Create backup of original
    backup_file = "data/final/csv_complete/01_SKU_Inventory_Final_Complete_backup.csv"
    if Path(existing_data_file).exists():
        import shutil
        shutil.copy2(existing_data_file, backup_file)
        print(f"✅ Created backup: {backup_file}")
    
    # Save updated data
    merged_data.to_csv(existing_data_file, index=False)
    print(f"✅ Updated main data file: {existing_data_file}")
    
    # Also save a copy with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_file = f"data/final/csv_complete/01_SKU_Inventory_Final_Complete_updated_{timestamp}.csv"
    merged_data.to_csv(timestamped_file, index=False)
    print(f"✅ Saved timestamped copy: {timestamped_file}")
    
    print("\n" + "=" * 60)
    print("✅ CONVERSION COMPLETE!")
    print("=" * 60)
    print(f"Updated data shape: {merged_data.shape}")
    print(f"All existing fields preserved (departments, suppliers, PAR mappings, etc.)")
    print(f"Updated fields: burn rates, lead times, UOM from new data")
    print(f"New items excluded from simulation (no demand data)")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS: New data has been merged with existing complete data!")
        print("   The csv_complete folder now contains the updated dataset.")
    else:
        print("\n❌ FAILED: Conversion failed. Check the error messages above.")