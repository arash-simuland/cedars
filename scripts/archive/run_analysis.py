#!/usr/bin/env python3
"""
Run the unmapped SKUs analysis from the Jupyter notebook
"""

import pandas as pd
import numpy as np
from datetime import datetime

def main():
    print("Starting unmapped SKUs analysis...")
    print("=" * 50)
    
    # Load the clean simulation data
    print("Loading CedarSim simulation data...")
    sku_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='01_SKU_Inventory_Clean')
    
    print(f"Total SKUs in clean dataset: {len(sku_df)}")
    print(f"Columns: {sku_df.columns.tolist()}")
    
    # Identify PAR location columns
    par_columns = [col for col in sku_df.columns if 'Level' in col or 'Perpetual' in col or 'Respiratory' in col]
    print(f"\nPAR Location columns ({len(par_columns)}):")
    for col in par_columns:
        print(f"  - {col}")
    
    # Identify unmapped SKUs
    print("\nAnalyzing unmapped SKUs...")
    sku_df['has_par_mapping'] = sku_df[par_columns].notna().any(axis=1)
    
    unmapped_count = (~sku_df['has_par_mapping']).sum()
    mapped_count = sku_df['has_par_mapping'].sum()
    
    print(f"SKUs with PAR mapping: {mapped_count}")
    print(f"SKUs without PAR mapping (unmapped): {unmapped_count}")
    
    if unmapped_count == 197:
        print("✅ Confirmed: Found exactly 197 unmapped SKUs as expected!")
    else:
        print(f"⚠️  Expected 197 unmapped SKUs, but found {unmapped_count}")
    
    # Analyze unmapped SKUs
    unmapped_skus = sku_df[~sku_df['has_par_mapping']].copy()
    
    print("\nAnalysis of Unmapped SKUs:")
    print("=" * 50)
    
    # Department analysis
    print("\n1. Department Distribution:")
    dept_counts = unmapped_skus['Department Name'].value_counts()
    print(dept_counts.head(10))
    
    # Supplier analysis
    print("\n2. Supplier Distribution:")
    supplier_counts = unmapped_skus['Supplier Name'].value_counts()
    print(supplier_counts.head(10))
    
    # Check validation SKUs
    print("\n3. Checking Validation SKUs:")
    validation_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='03_Validation_Sample')
    validation_skus = set(validation_df['Oracle Item Number'].astype(str))
    unmapped_skus_list = set(unmapped_skus['Oracle Item Number'].astype(str))
    
    validation_unmapped = validation_skus.intersection(unmapped_skus_list)
    print(f"Validation SKUs that are unmapped: {len(validation_unmapped)}")
    
    if len(validation_unmapped) > 0:
        print("⚠️  WARNING: Some validation SKUs are unmapped!")
    else:
        print("✅ All validation SKUs have PAR location mapping - safe to remove unmapped SKUs")
    
    # Create final cleaned dataset
    print("\nCreating Final Cleaned Dataset:")
    print("=" * 35)
    
    final_clean_skus = sku_df[sku_df['has_par_mapping']].copy()
    final_clean_skus = final_clean_skus.drop('has_par_mapping', axis=1)
    
    print(f"Original clean SKUs: {len(sku_df)}")
    print(f"Final clean SKUs (after removing unmapped): {len(final_clean_skus)}")
    print(f"SKUs removed: {len(sku_df) - len(final_clean_skus)}")
    
    # Save results
    print("\nSaving results...")
    
    # Create unmapped SKUs record
    unmapped_record = unmapped_skus[['Oracle Item Number', 'Item Description', 'Department Name', 'Supplier Name', 'Avg_Lead Time']].copy()
    unmapped_record['Removal_Reason'] = 'No PAR Location Mapping'
    
    # Save to Excel
    with pd.ExcelWriter('CedarSim_Simulation_Ready_Data_Final.xlsx', engine='openpyxl') as writer:
        final_clean_skus.to_excel(writer, sheet_name='01_SKU_Inventory_Final', index=False)
        
        # Load and save demand data
        demand_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='02_Demand_Data_Clean')
        demand_df.to_excel(writer, sheet_name='02_Demand_Data_Clean', index=False)
        
        # Save validation sample
        validation_df.to_excel(writer, sheet_name='03_Validation_Sample', index=False)
        
        # Save unmapped SKUs record
        unmapped_record.to_excel(writer, sheet_name='04_Phase2_Unmapped_SKUs', index=False)
    
    # Save CSV
    unmapped_record.to_csv('unmapped_skus_phase2.csv', index=False)
    
    print("✅ Analysis complete!")
    print(f"📊 Final dataset: {len(final_clean_skus):,} SKUs ready for simulation")
    print(f"📄 Files created:")
    print(f"  - CedarSim_Simulation_Ready_Data_Final.xlsx")
    print(f"  - unmapped_skus_phase2.csv")

if __name__ == "__main__":
    main()
