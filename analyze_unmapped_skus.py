#!/usr/bin/env python3
"""
Analyze unmapped SKUs in CedarSim simulation data
Identify SKUs with no PAR location mapping
"""

import pandas as pd
import numpy as np

def analyze_unmapped_skus():
    """Analyze SKUs to identify those without PAR location mapping"""
    
    # Load the clean SKU inventory data
    print("Loading CedarSim simulation data...")
    sku_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='01_SKU_Inventory_Clean')
    
    print(f"Total SKUs in clean dataset: {len(sku_df)}")
    print(f"Columns: {sku_df.columns.tolist()}")
    
    # Display first few rows to understand structure
    print("\nFirst 5 rows:")
    print(sku_df.head())
    
    # Check for PAR location mapping columns
    par_columns = [col for col in sku_df.columns if 'par' in col.lower() or 'location' in col.lower()]
    print(f"\nPAR/Location related columns: {par_columns}")
    
    # Check for missing values in key columns
    print("\nMissing values per column:")
    missing_counts = sku_df.isnull().sum()
    print(missing_counts[missing_counts > 0])
    
    # Look for SKU identifier column
    sku_columns = [col for col in sku_df.columns if 'sku' in col.lower() or 'item' in col.lower()]
    print(f"\nSKU identifier columns: {sku_columns}")
    
    # Check data types
    print("\nData types:")
    print(sku_df.dtypes)
    
    return sku_df

if __name__ == "__main__":
    df = analyze_unmapped_skus()
