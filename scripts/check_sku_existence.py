#!/usr/bin/env python3
"""
Check SKU Existence Script
==========================

Check if the missing SKUs from test data exist in the main datasets.
"""

import pandas as pd

def main():
    # Load main datasets
    print("Loading main datasets...")
    sku_main = pd.read_excel('data/final/CedarSim_Simulation_Ready_Data_Final.xlsx', 
                            sheet_name='01_SKU_Inventory_Final')
    demand_main = pd.read_excel('data/final/CedarSim_Simulation_Ready_Data_Final.xlsx', 
                               sheet_name='02_Demand_Data_Clean')
    
    print(f"Main SKU data: {len(sku_main)} rows, {sku_main['Oracle Item Number'].nunique()} unique SKUs")
    print(f"Main demand data: {len(demand_main)} rows, {demand_main['Oracle Item Number'].nunique()} unique SKUs")
    
    # Test SKUs that are missing
    test_skus = [136, 235, 262, 386, 508, 523, 529, 535, 536, 549, 552, 555, 565, 838, 1077]
    
    print(f"\nSample SKUs from main SKU data:")
    print(sorted(sku_main['Oracle Item Number'].unique())[:20])
    
    print(f"\nSample SKUs from main demand data:")
    print(sorted(demand_main['Oracle Item Number'].unique())[:20])
    
    print(f"\nChecking if test SKUs exist in main data:")
    for sku in test_skus[:5]:
        sku_in_sku = sku in sku_main['Oracle Item Number'].values
        sku_in_demand = sku in demand_main['Oracle Item Number'].values
        print(f"SKU {sku} in SKU data: {sku_in_sku}")
        print(f"SKU {sku} in demand data: {sku_in_demand}")
    
    # Check if there are any SKUs that start with these numbers
    print(f"\nChecking for SKUs that start with these numbers:")
    for sku in test_skus[:5]:
        sku_str = str(sku)
        sku_matches = sku_main[sku_main['Oracle Item Number'].astype(str).str.startswith(sku_str)]
        demand_matches = demand_main[demand_main['Oracle Item Number'].astype(str).str.startswith(sku_str)]
        print(f"SKUs starting with {sku}: SKU data={len(sku_matches)}, Demand data={len(demand_matches)}")

if __name__ == "__main__":
    main()
