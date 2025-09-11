#!/usr/bin/env python3
"""
Check what's in the ROBUST files and understand their purpose.
"""

import pandas as pd
import os

def check_robust_files():
    """Check the content and purpose of ROBUST files."""
    
    print("🔍 ROBUST Files Analysis")
    print("=" * 50)
    
    robust_files = [
        'CedarSim_Simulation_Ready_Data_ROBUST.xlsx',
        'CedarSim_Simulation_Ready_Data_ROBUST_temp.xlsx'
    ]
    
    for file_path in robust_files:
        if os.path.exists(file_path):
            print(f"\n📂 Analyzing: {file_path}")
            print(f"   File size: {os.path.getsize(file_path):,} bytes")
            
            try:
                # Get sheet names
                excel_file = pd.ExcelFile(file_path)
                print(f"   Sheets: {excel_file.sheet_names}")
                
                # Check each sheet
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    print(f"     {sheet_name}: {len(df)} rows × {len(df.columns)} columns")
                    
                    # Show first few rows if it's a small dataset
                    if len(df) <= 10:
                        print(f"       Sample data:")
                        print(df.head(3).to_string())
                    else:
                        print(f"       Columns: {list(df.columns)[:5]}...")
                        
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        else:
            print(f"❌ File not found: {file_path}")
    
    # Compare with other files
    print(f"\n📊 File Size Comparison:")
    files_to_compare = [
        'CedarSim_Simulation_Ready_Data_Final.xlsx',
        'CedarSim_Simulation_Ready_Data_FIXED.xlsx',
        'CedarSim_Simulation_Ready_Data_ROBUST.xlsx'
    ]
    
    for file_path in files_to_compare:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   {file_path}: {size:,} bytes ({size/1024/1024:.1f} MB)")

if __name__ == "__main__":
    check_robust_files()
