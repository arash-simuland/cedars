#!/usr/bin/env python3
"""
Script to examine column names in both Excel files to understand the structure.
"""

import pandas as pd

def examine_columns():
    """Examine column names in both files."""
    
    print("🔍 Examining Excel File Columns")
    print("=" * 50)
    
    try:
        # Read our pipeline output
        print("📂 Our pipeline output columns:")
        our_file = pd.read_excel('CedarSim_Simulation_Ready_Data_Final.xlsx', sheet_name='01_SKU_Inventory_Final')
        print(f"   Sheet: 01_SKU_Inventory_Final")
        print(f"   Rows: {len(our_file)}")
        print(f"   Columns: {list(our_file.columns)}")
        print()
        
        # Read the FIXED file - check all sheet names first
        print("📂 FIXED file structure:")
        fixed_file = pd.ExcelFile('CedarSim_Simulation_Ready_Data_FIXED.xlsx')
        print(f"   Sheet names: {fixed_file.sheet_names}")
        
        for sheet_name in fixed_file.sheet_names:
            print(f"\n   Sheet: {sheet_name}")
            sheet_data = pd.read_excel('CedarSim_Simulation_Ready_Data_FIXED.xlsx', sheet_name=sheet_name)
            print(f"   Rows: {len(sheet_data)}")
            print(f"   Columns: {list(sheet_data.columns)}")
            
            # Look for Oracle Item Number column
            oracle_cols = [col for col in sheet_data.columns if 'oracle' in col.lower() or 'item' in col.lower()]
            if oracle_cols:
                print(f"   Potential Oracle Item Number columns: {oracle_cols}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    examine_columns()