#!/usr/bin/env python3
"""Check the structure of the FIXED file"""

import pandas as pd

def check_fixed_file():
    try:
        print("Loading FIXED file...")
        df = pd.read_excel('CedarSim_Simulation_Ready_Data_FIXED.xlsx', sheet_name='Data')
        print(f"Shape: {df.shape}")
        print("Columns:")
        for i, col in enumerate(df.columns):
            print(f"  {i:2d}: '{col}'")
        
        print(f"\nFirst few rows:")
        print(df.head())
        
        print(f"\nRow 0 (should be headers):")
        print(df.iloc[0])
        
        # Try to find Oracle Item Number column
        print(f"\nLooking for Oracle Item Number...")
        for i, col in enumerate(df.columns):
            if 'Oracle' in str(df.iloc[0, i]) or 'Item' in str(df.iloc[0, i]):
                print(f"  Column {i} ({col}): {df.iloc[0, i]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_fixed_file()
