#!/usr/bin/env python3
"""
Analyze CedarSim Simulation Ready Data to identify unmapped SKUs
"""

import pandas as pd
import sys

def analyze_simulation_data():
    """Analyze the simulation data file to understand structure and find unmapped SKUs"""
    
    try:
        # Load the Excel file
        xl = pd.ExcelFile('CedarSim_Simulation_Ready_Data.xlsx')
        print("Sheet names:", xl.sheet_names)
        print("\nSheet sizes:")
        
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet)
            print(f"{sheet}: {len(df)} rows, {len(df.columns)} columns")
            print(f"  Columns: {list(df.columns)}")
            print()
        
        # Focus on the main SKU data sheet (likely the first one)
        main_sheet = xl.sheet_names[0]
        sku_data = pd.read_excel(xl, sheet_name=main_sheet)
        
        print(f"\nAnalyzing main sheet: {main_sheet}")
        print(f"Total SKUs: {len(sku_data)}")
        
        # Look for PAR location mapping columns
        par_columns = [col for col in sku_data.columns if 'par' in col.lower() or 'location' in col.lower()]
        print(f"PAR/Location columns: {par_columns}")
        
        # Check for missing PAR mappings
        if par_columns:
            for col in par_columns:
                missing_count = sku_data[col].isna().sum()
                print(f"Missing values in {col}: {missing_count}")
                
                if missing_count > 0:
                    print(f"SKUs with missing {col}:")
                    missing_skus = sku_data[sku_data[col].isna()]
                    print(missing_skus[['SKU', col] if 'SKU' in sku_data.columns else missing_skus.columns[:2]].head(10))
        
        # Look for any other potential mapping issues
        print(f"\nData types:")
        print(sku_data.dtypes)
        
        print(f"\nFirst few rows:")
        print(sku_data.head())
        
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    analyze_simulation_data()
