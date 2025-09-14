#!/usr/bin/env python3
"""
Analyze Missing SKU Information - Perpetual/PAR and Levels
"""

import pandas as pd
import numpy as np
from pathlib import Path

def analyze_missing_sku_info():
    """Analyze what SKU information is missing in the new file"""
    
    # Load the new Excel file
    new_file = Path('data/archive/original/2025-09-12_MDRH_Item_List.xlsx')
    existing_sku = Path('data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv')
    
    print('=' * 60)
    print('DETAILED SKU INFORMATION ANALYSIS')
    print('=' * 60)
    
    # Load data
    new_data = pd.read_excel(new_file, sheet_name='Sheet1')
    existing_data = pd.read_csv(existing_sku)
    
    print(f'New data shape: {new_data.shape}')
    print(f'Existing data shape: {existing_data.shape}')
    
    print('\n' + '=' * 40)
    print('NEW FILE COLUMNS:')
    print('=' * 40)
    for i, col in enumerate(new_data.columns):
        print(f'{i+1:2d}. {col}')
    
    print('\n' + '=' * 40)
    print('EXISTING FILE COLUMNS:')
    print('=' * 40)
    for i, col in enumerate(existing_data.columns):
        print(f'{i+1:2d}. {col}')
    
    print('\n' + '=' * 40)
    print('PERPETUAL/PAR INFORMATION ANALYSIS')
    print('=' * 40)
    
    # Check for perpetual/PAR related columns in existing data
    perpetual_cols = [col for col in existing_data.columns if 'perpetual' in col.lower() or 'par' in col.lower()]
    print(f'Perpetual/PAR columns in existing data: {perpetual_cols}')
    
    # Check for level columns in existing data
    level_cols = [col for col in existing_data.columns if 'level' in col.lower()]
    print(f'Level columns in existing data: {level_cols}')
    
    print('\n' + '=' * 40)
    print('MISSING CRITICAL INFORMATION IN NEW FILE')
    print('=' * 40)
    
    missing_info = {
        'Department Information': ['Department Name', 'Department Number'],
        'Supplier Information': ['Supplier Name'],
        'PAR/Perpetual Status': ['On-PAR or Special Request', 'Medline item? Y/N'],
        'Level Information': level_cols,
        'Burn Rate': ['Avg Daily Burn Rate'],
        'Lead Time': ['Avg_Lead Time'],
        'UOM': ['UOM']
    }
    
    for category, columns in missing_info.items():
        print(f'\n{category}:')
        for col in columns:
            if col in existing_data.columns:
                if col in new_data.columns:
                    print(f'  ✅ {col} - Present')
                else:
                    print(f'  ❌ {col} - Missing')
            else:
                print(f'  ⚠️  {col} - Not in existing data')
    
    print('\n' + '=' * 40)
    print('SAMPLE DATA COMPARISON')
    print('=' * 40)
    
    # Show sample of overlapping items
    common_items = set(new_data['Oracle Item Number']) & set(existing_data['Oracle Item Number'])
    if common_items:
        sample_item = list(common_items)[0]
        print(f'Sample item: {sample_item}')
        
        print('\nNew file data:')
        new_sample = new_data[new_data['Oracle Item Number'] == sample_item].iloc[0]
        for col in new_data.columns:
            print(f'  {col}: {new_sample[col]}')
        
        print('\nExisting file data:')
        existing_sample = existing_data[existing_data['Oracle Item Number'] == sample_item].iloc[0]
        for col in ['Department Name', 'Department Number', 'Supplier Name', 'On-PAR or Special Request', 'Medline item? Y/N']:
            if col in existing_sample:
                print(f'  {col}: {existing_sample[col]}')
        
        # Show level information
        print('\nLevel information:')
        for col in level_cols:
            if col in existing_sample and pd.notna(existing_sample[col]):
                print(f'  {col}: {existing_sample[col]}')
    
    print('\n' + '=' * 40)
    print('PERPETUAL/PAR STATUS ANALYSIS')
    print('=' * 40)
    
    # Analyze PAR status in existing data
    if 'On-PAR or Special Request' in existing_data.columns:
        par_status = existing_data['On-PAR or Special Request'].value_counts()
        print(f'PAR Status distribution in existing data:')
        for status, count in par_status.items():
            print(f'  {status}: {count} items')
    
    # Analyze Medline status
    if 'Medline item? Y/N' in existing_data.columns:
        medline_status = existing_data['Medline item? Y/N'].value_counts()
        print(f'\nMedline Status distribution in existing data:')
        for status, count in medline_status.items():
            print(f'  {status}: {count} items')
    
    print('\n' + '=' * 40)
    print('LEVEL DISTRIBUTION ANALYSIS')
    print('=' * 40)
    
    # Analyze level distribution
    for col in level_cols:
        if col in existing_data.columns:
            level_data = existing_data[col].value_counts()
            print(f'\n{col}:')
            for level, count in level_data.items():
                if pd.notna(level):
                    print(f'  {level}: {count} items')
    
    print('\n' + '=' * 40)
    print('IMPACT ASSESSMENT')
    print('=' * 40)
    
    # Calculate impact of missing information
    total_existing = len(existing_data)
    total_new = len(new_data)
    overlap = len(common_items)
    
    print(f'Total items in existing data: {total_existing:,}')
    print(f'Total items in new data: {total_new:,}')
    print(f'Overlapping items: {overlap:,}')
    print(f'New items only: {total_new - overlap:,}')
    print(f'Existing items only: {total_existing - overlap:,}')
    
    # Check what percentage of existing items would lose critical information
    if overlap > 0:
        print(f'\nImpact on overlapping items:')
        print(f'  Items that would lose PAR status: {overlap:,} (100%)')
        print(f'  Items that would lose Medline status: {overlap:,} (100%)')
        print(f'  Items that would lose level information: {overlap:,} (100%)')
        print(f'  Items that would lose department info: {overlap:,} (100%)')
        print(f'  Items that would lose supplier info: {overlap:,} (100%)')

if __name__ == "__main__":
    analyze_missing_sku_info()
