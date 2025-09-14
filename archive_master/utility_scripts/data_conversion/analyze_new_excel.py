#!/usr/bin/env python3
"""
Quick Analysis of New Excel File - 2025-09-12_MDRH_Item_List.xlsx
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyze_new_excel():
    """Analyze the new Excel file and compare with existing data"""
    
    # Set up paths
    data_dir = Path('data')
    new_file = data_dir / 'archive/original/2025-09-12_MDRH_Item_List.xlsx'
    existing_sku = data_dir / 'final/csv_complete/01_SKU_Inventory_Final_Complete.csv'
    existing_demand = data_dir / 'final/csv_complete/02_Demand_Data_Clean_Complete.csv'
    
    print("=" * 60)
    print("NEW EXCEL FILE ANALYSIS")
    print("=" * 60)
    
    print(f"New file exists: {new_file.exists()}")
    print(f"Existing SKU data exists: {existing_sku.exists()}")
    print(f"Existing demand data exists: {existing_demand.exists()}")
    
    # Load the new Excel file
    print("\n" + "=" * 40)
    print("LOADING NEW EXCEL FILE")
    print("=" * 40)
    
    try:
        excel_file = pd.ExcelFile(new_file)
        print(f"Available sheets: {excel_file.sheet_names}")
        
        new_data = {}
        for sheet_name in excel_file.sheet_names:
            print(f"\n--- Sheet: {sheet_name} ---")
            df = pd.read_excel(new_file, sheet_name=sheet_name)
            new_data[sheet_name] = df
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"First few rows:")
            print(df.head())
            
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        try:
            df = pd.read_excel(new_file, engine='openpyxl')
            print(f"Successfully loaded with openpyxl engine")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            new_data = {'Sheet1': df}
        except Exception as e2:
            print(f"Failed with openpyxl: {e2}")
            new_data = {}
    
    # Load existing data for comparison
    print("\n" + "=" * 40)
    print("LOADING EXISTING DATA")
    print("=" * 40)
    
    if existing_sku.exists():
        existing_sku_data = pd.read_csv(existing_sku)
        print(f"Existing SKU data shape: {existing_sku_data.shape}")
        print(f"Existing SKU columns: {list(existing_sku_data.columns)}")
    else:
        existing_sku_data = None
        print("Existing SKU data not found")
    
    if existing_demand.exists():
        existing_demand_data = pd.read_csv(existing_demand)
        print(f"Existing demand data shape: {existing_demand_data.shape}")
        print(f"Existing demand columns: {list(existing_demand_data.columns)}")
    else:
        existing_demand_data = None
        print("Existing demand data not found")
    
    # Analyze compatibility
    print("\n" + "=" * 40)
    print("COMPATIBILITY ANALYSIS")
    print("=" * 40)
    
    if new_data and existing_sku_data is not None:
        for sheet_name, df in new_data.items():
            print(f"\n--- Sheet: {sheet_name} ---")
            
            # Check for common columns
            common_cols = set(df.columns) & set(existing_sku_data.columns)
            print(f"Common columns with existing SKU data: {len(common_cols)}/{len(existing_sku_data.columns)}")
            print(f"Common columns: {list(common_cols)}")
            
            # Check for key identifier columns
            key_cols = ['Oracle Item Number', 'Item Description', 'Department Name', 'Department Number']
            found_key_cols = [col for col in key_cols if col in df.columns]
            print(f"Key identifier columns found: {found_key_cols}")
            
            # Check Oracle Item Number overlap
            if 'Oracle Item Number' in df.columns and 'Oracle Item Number' in existing_sku_data.columns:
                new_items = set(df['Oracle Item Number'].dropna())
                existing_items = set(existing_sku_data['Oracle Item Number'].dropna())
                
                overlap = new_items & existing_items
                new_only = new_items - existing_items
                existing_only = existing_items - new_items
                
                print(f"\nOracle Item Numbers:")
                print(f"  New data: {len(new_items)} unique items")
                print(f"  Existing data: {len(existing_items)} unique items")
                print(f"  Overlap: {len(overlap)} items ({len(overlap)/len(new_items)*100:.1f}% of new data)")
                print(f"  New only: {len(new_only)} items")
                print(f"  Existing only: {len(existing_only)} items")
                
                if len(overlap) > 0:
                    print(f"  Sample overlapping items: {list(overlap)[:5]}")
                if len(new_only) > 0:
                    print(f"  Sample new items: {list(new_only)[:5]}")
    
    # Pipeline compatibility check
    print("\n" + "=" * 40)
    print("PIPELINE COMPATIBILITY CHECK")
    print("=" * 40)
    
    required_sku_cols = [
        'Department Name', 'Department Number', 'Oracle Item Number', 
        'Item Description', 'UOM', 'Avg Daily Burn Rate', 'Supplier Name', 
        'Avg_Lead Time', 'Medline item? Y/N', 'On-PAR or Special Request'
    ]
    
    if new_data:
        for sheet_name, df in new_data.items():
            print(f"\n--- Sheet: {sheet_name} ---")
            
            # Check SKU requirements
            sku_missing = [col for col in required_sku_cols if col not in df.columns]
            sku_present = [col for col in required_sku_cols if col in df.columns]
            
            print(f"SKU Requirements:")
            print(f"  Present: {len(sku_present)}/{len(required_sku_cols)} columns")
            print(f"  Missing: {sku_missing}")
            print(f"  Present columns: {sku_present}")
            
            # Check data types for critical columns
            if 'Avg Daily Burn Rate' in df.columns:
                burn_rate_numeric = pd.to_numeric(df['Avg Daily Burn Rate'], errors='coerce').notna().sum()
                print(f"\nAvg Daily Burn Rate: {burn_rate_numeric}/{len(df)} numeric values ({burn_rate_numeric/len(df)*100:.1f}%)")
            
            if 'Avg_Lead Time' in df.columns:
                lead_time_numeric = pd.to_numeric(df['Avg_Lead Time'], errors='coerce').notna().sum()
                print(f"Avg_Lead Time: {lead_time_numeric}/{len(df)} numeric values ({lead_time_numeric/len(df)*100:.1f}%)")
    
    # Final assessment
    print("\n" + "=" * 40)
    print("FINAL ASSESSMENT")
    print("=" * 40)
    
    if not new_data:
        print("❌ CRITICAL: Unable to load new Excel file")
        print("   - Check file format and accessibility")
        print("   - Verify file is not corrupted")
        return
    
    print("✅ New Excel file loaded successfully")
    
    # Overall assessment
    is_good_input = True
    issues = []
    
    if isinstance(new_data, dict):
        for sheet_name, df in new_data.items():
            print(f"\n--- Assessment for Sheet: {sheet_name} ---")
            
            # Check data size
            if len(df) < 100:
                issues.append(f"Sheet {sheet_name} has very few rows ({len(df)})")
                is_good_input = False
            
            # Check for required columns
            required_cols = ['Oracle Item Number', 'Item Description', 'Department Name']
            missing_required = [col for col in required_cols if col not in df.columns]
            if missing_required:
                issues.append(f"Sheet {sheet_name} missing required columns: {missing_required}")
                is_good_input = False
            
            # Check data completeness
            if 'Oracle Item Number' in df.columns:
                missing_items = df['Oracle Item Number'].isnull().sum()
                if missing_items > 0:
                    issues.append(f"Sheet {sheet_name} has {missing_items} missing Oracle Item Numbers")
                    is_good_input = False
    
    # Overall assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if is_good_input:
        print(f"✅ GOOD INPUT: The new Excel file appears to be suitable for integration")
    else:
        print(f"❌ ISSUES FOUND: The new Excel file has problems that need to be addressed")
        print(f"\nIssues to fix:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Integration recommendations
    print(f"\n🔧 INTEGRATION RECOMMENDATIONS:")
    print(f"1. Review the detailed analysis above")
    print(f"2. Address any identified issues")
    print(f"3. Determine integration strategy (replace, merge, or supplement)")
    print(f"4. Update the CedarSim pipeline if needed")
    print(f"5. Run the complete pipeline with new data")
    print(f"6. Validate results against existing data")

if __name__ == "__main__":
    analyze_new_excel()
