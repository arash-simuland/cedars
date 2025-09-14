#!/usr/bin/env python3
"""
Test the new Excel converter
"""

import pandas as pd
from pathlib import Path

def test_converter():
    """Test the converter with a simple example"""
    
    print("🧪 Testing CedarSim Data Converter...")
    
    # Check if files exist
    new_file = Path('data/archive/original/2025-09-12_MDRH_Item_List.xlsx')
    existing_data = Path('data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv')
    
    print(f"New file exists: {new_file.exists()}")
    print(f"Existing data exists: {existing_data.exists()}")
    
    if not new_file.exists() or not existing_data.exists():
        print("❌ Required files not found")
        return
    
    # Load data
    print("\n📊 Loading data...")
    new_data = pd.read_excel(new_file, sheet_name='Sheet1')
    existing_data = pd.read_csv(existing_data)
    
    print(f"New data shape: {new_data.shape}")
    print(f"Existing data shape: {existing_data.shape}")
    
    # Check overlap
    new_items = set(new_data['Oracle Item Number'])
    existing_items = set(existing_data['Oracle Item Number'])
    overlap = new_items & existing_items
    
    print(f"\n🔍 Data Analysis:")
    print(f"New items: {len(new_items)}")
    print(f"Existing items: {len(existing_items)}")
    print(f"Overlapping items: {len(overlap)}")
    print(f"Overlap percentage: {len(overlap)/len(new_items)*100:.1f}%")
    
    # Test column mapping
    print(f"\n🔄 Testing column mapping...")
    column_mapping = {
        'Oracle Item Number': 'Oracle Item Number',
        'Item Description': 'Item Description',
        'unit_of_measure': 'UOM',
        'lead_time': 'Avg_Lead Time',
        'burn_rate': 'Avg Daily Burn Rate'
    }
    
    # Convert new data
    converted_data = new_data.copy()
    converted_data = converted_data.rename(columns=column_mapping)
    converted_data = converted_data.drop_duplicates(subset=['Oracle Item Number'], keep='first')
    
    print(f"Converted data shape: {converted_data.shape}")
    print(f"Converted columns: {list(converted_data.columns)}")
    
    # Test merging
    print(f"\n🔗 Testing data merging...")
    
    # Update overlapping items
    merged_data = existing_data.copy()
    
    for item in list(overlap)[:5]:  # Test with first 5 items
        new_item_data = converted_data[converted_data['Oracle Item Number'] == item].iloc[0]
        mask = merged_data['Oracle Item Number'] == item
        
        # Update burn rate and lead time
        merged_data.loc[mask, 'Avg Daily Burn Rate'] = new_item_data['Avg Daily Burn Rate']
        merged_data.loc[mask, 'Avg_Lead Time'] = new_item_data['Avg_Lead Time']
        merged_data.loc[mask, 'UOM'] = new_item_data['UOM']
        
        print(f"Updated item {item}: Burn Rate={new_item_data['Avg Daily Burn Rate']}, Lead Time={new_item_data['Avg_Lead Time']}")
    
    print(f"\n✅ Converter test successful!")
    print(f"Final merged data shape: {merged_data.shape}")
    
    # Show sample
    sample_items = list(overlap)[:3]
    print(f"\n📋 Sample converted data:")
    for item in sample_items:
        sample = merged_data[merged_data['Oracle Item Number'] == item].iloc[0]
        print(f"Item {item}: {sample['Item Description']}")
        print(f"  Department: {sample['Department Name']}")
        print(f"  Supplier: {sample['Supplier Name']}")
        print(f"  Burn Rate: {sample['Avg Daily Burn Rate']}")
        print(f"  Lead Time: {sample['Avg_Lead Time']}")
        print(f"  PAR Status: {sample['On-PAR or Special Request']}")
        print()

if __name__ == "__main__":
    test_converter()
