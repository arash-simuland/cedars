import pandas as pd

print("Quick unmapped SKUs analysis...")

# Load data
sku_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='01_SKU_Inventory_Clean')
print(f"Loaded {len(sku_df)} SKUs")

# Find PAR columns
par_columns = [col for col in sku_df.columns if 'Level' in col or 'Perpetual' in col or 'Respiratory' in col]
print(f"Found {len(par_columns)} PAR columns")

# Quick check: count SKUs with any PAR mapping
has_mapping = sku_df[par_columns].notna().any(axis=1) | (sku_df[par_columns] == 'X').any(axis=1)
unmapped_count = (~has_mapping).sum()
mapped_count = has_mapping.sum()

print(f"Mapped SKUs: {mapped_count}")
print(f"Unmapped SKUs: {unmapped_count}")

# Check validation SKUs
validation_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='03_Validation_Sample')
print(f"Validation SKUs: {len(validation_df)}")

# Quick summary
print(f"\n✅ Analysis complete!")
print(f"📊 Remove {unmapped_count} unmapped SKUs")
print(f"📊 Keep {mapped_count} mapped SKUs")
print(f"📊 Validation SKUs: {len(validation_df)}")
