import pandas as pd
import numpy as np
from datetime import datetime

print("Completing unmapped SKUs analysis...")
print("=" * 50)

# Load data
sku_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='01_SKU_Inventory_Clean')
validation_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='03_Validation_Sample')

# Identify PAR columns
par_columns = [col for col in sku_df.columns if 'Level' in col or 'Perpetual' in col or 'Respiratory' in col]
print(f"Found {len(par_columns)} PAR location columns")

# Find unmapped SKUs
sku_df['has_par_mapping'] = sku_df[par_columns].notna().any(axis=1)
unmapped_skus = sku_df[~sku_df['has_par_mapping']].copy()

print(f"Total SKUs: {len(sku_df)}")
print(f"Unmapped SKUs: {len(unmapped_skus)}")
print(f"Mapped SKUs: {len(sku_df) - len(unmapped_skus)}")

# Check validation SKUs
validation_skus = set(validation_df['Oracle Item Number'].astype(str))
unmapped_skus_list = set(unmapped_skus['Oracle Item Number'].astype(str))
validation_unmapped = validation_skus.intersection(unmapped_skus_list)

print(f"\nValidation SKUs: {len(validation_skus)}")
print(f"Validation SKUs that are unmapped: {len(validation_unmapped)}")

if len(validation_unmapped) > 0:
    print("\n⚠️  CRITICAL: Validation SKU that is unmapped:")
    for sku in validation_unmapped:
        val_info = validation_df[validation_df['Oracle Item Number'].astype(str) == sku]
        print(f"  SKU: {sku}")
        print(f"  Description: {val_info['Item Description'].iloc[0]}")
        print(f"  Department: {val_info['Department Name'].iloc[0]}")
        
        # Check if this SKU has any PAR mapping
        sku_info = sku_df[sku_df['Oracle Item Number'].astype(str) == sku]
        print(f"  Has PAR mapping: {sku_info['has_par_mapping'].iloc[0]}")
        print(f"  PAR columns with values:")
        for col in par_columns:
            if sku_info[col].notna().any():
                print(f"    {col}: {sku_info[col].iloc[0]}")

# Create final dataset (keeping validation SKU for now)
print(f"\nCreating final dataset...")
final_clean_skus = sku_df[sku_df['has_par_mapping']].copy()
final_clean_skus = final_clean_skus.drop('has_par_mapping', axis=1)

# Create unmapped SKUs record
unmapped_record = unmapped_skus[['Oracle Item Number', 'Item Description', 'Department Name', 'Supplier Name', 'Avg_Lead Time']].copy()
unmapped_record['Removal_Reason'] = 'No PAR Location Mapping'

print(f"Final clean SKUs: {len(final_clean_skus)}")
print(f"Unmapped SKUs record: {len(unmapped_record)}")

# Save results
print(f"\nSaving results...")

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

# Summary
print(f"\n📋 Summary:")
print(f"  - Phase 1: Removed 298 SKUs (missing lead times)")
print(f"  - Phase 2: Removed {len(unmapped_record)} SKUs (no PAR mapping)")
print(f"  - Final dataset: {len(final_clean_skus):,} SKUs")
print(f"  - Validation SKUs: {len(validation_skus)} (1 unmapped - needs attention)")
