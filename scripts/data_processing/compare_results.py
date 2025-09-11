#!/usr/bin/env python3
"""Compare pipeline results with existing ready data files"""

import pandas as pd
import os
from pathlib import Path

def compare_excel_files():
    """Compare our new pipeline output with existing ready data files"""
    
    # Files to compare
    files_to_check = [
        'CedarSim_Simulation_Ready_Data_Final.xlsx',  # Our new pipeline output
        'CedarSim_Simulation_Ready_Data_FIXED.xlsx',   # Previous working file (5,942 rows)
        'CedarSim_Simulation_Ready_Data_ROBUST.xlsx',  # Robust version
        'CedarSim_Simulation_Ready_Data_ROBUST_temp.xlsx'  # Temp robust version
    ]
    
    print("=" * 80)
    print("CEDARSIM DATA COMPARISON REPORT")
    print("=" * 80)
    
    results = {}
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"\n📊 Analyzing: {file_path}")
            print("-" * 60)
            
            try:
                # Get file size
                file_size = os.path.getsize(file_path)
                print(f"File size: {file_size:,} bytes")
                
                # Read Excel file
                xl = pd.ExcelFile(file_path)
                print(f"Sheets: {len(xl.sheet_names)}")
                
                for i, sheet_name in enumerate(xl.sheet_names, 1):
                    try:
                        df = pd.read_excel(file_path, sheet_name=sheet_name)
                        print(f"  {i}. {sheet_name}: {len(df):,} rows × {len(df.columns)} columns")
                        
                        # Store results for comparison
                        if file_path not in results:
                            results[file_path] = {}
                        results[file_path][sheet_name] = {
                            'rows': len(df),
                            'columns': len(df.columns),
                            'sample_columns': list(df.columns[:5])
                        }
                        
                    except Exception as e:
                        print(f"  {i}. {sheet_name}: ERROR - {e}")
                
            except Exception as e:
                print(f"ERROR reading file: {e}")
                results[file_path] = {'error': str(e)}
        else:
            print(f"\n❌ File not found: {file_path}")
    
    # Compare results
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    
    if 'CedarSim_Simulation_Ready_Data_Final.xlsx' in results:
        our_file = results['CedarSim_Simulation_Ready_Data_Final.xlsx']
        print(f"\n🔍 Our Pipeline Output (Final.xlsx):")
        
        for sheet_name, data in our_file.items():
            if isinstance(data, dict) and 'rows' in data:
                print(f"  {sheet_name}: {data['rows']:,} rows")
        
        # Compare with FIXED file
        if 'CedarSim_Simulation_Ready_Data_FIXED.xlsx' in results:
            fixed_file = results['CedarSim_Simulation_Ready_Data_FIXED.xlsx']
            print(f"\n📋 Comparison with FIXED.xlsx:")
            
            for sheet_name in our_file.keys():
                if sheet_name in fixed_file and isinstance(fixed_file[sheet_name], dict):
                    our_rows = our_file[sheet_name]['rows']
                    fixed_rows = fixed_file[sheet_name]['rows']
                    diff = our_rows - fixed_rows
                    
                    print(f"  {sheet_name}:")
                    print(f"    Our pipeline: {our_rows:,} rows")
                    print(f"    FIXED file:   {fixed_rows:,} rows")
                    print(f"    Difference:   {diff:+,} rows")
                    
                    if diff == 0:
                        print(f"    ✅ MATCH!")
                    else:
                        print(f"    ⚠️  DIFFERENCE DETECTED!")
    
    return results

if __name__ == "__main__":
    compare_excel_files()
