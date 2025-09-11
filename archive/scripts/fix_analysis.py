import pandas as pd
import numpy as np

print("Fixing unmapped SKUs analysis with correct logic...")
print("=" * 60)

# Load data
sku_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='01_SKU_Inventory_Clean')
validation_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='03_Validation_Sample')

# Identify PAR columns
par_columns = [col for col in sku_df.columns if 'Level' in col or 'Perpetual' in col or 'Respiratory' in col]
print(f"Found {len(par_columns)} PAR location columns")

# Fix the logic - look for 'X' values or non-null values
print("\nChecking PAR mapping logic...")
print("Sample of PAR column values:")
for col in par_columns[:3]:  # Show first 3 columns
    unique_vals = sku_df[col].value_counts(dropna=False).head()
    print(f"  {col}: {dict(unique_vals)}")

# Correct logic: SKU has PAR mapping if ANY PAR column has 'X' or non-null value
sku_df['has_par_mapping'] = False
for col in par_columns:
    # Check for 'X' values or non-null values
    has_mapping = (sku_df[col] == 'X') | (sku_df[col].notna())
    sku_df['has_par_mapping'] = sku_df['has_par_mapping'] | has_mapping

unmapped_skus = sku_df[~sku_df['has_par_mapping']].copy()

print(f"\nCorrected Analysis:")
print(f"Total SKUs: {len(sku_df)}")
print(f"Unmapped SKUs: {len(unmapped_skus)}")
print(f"Mapped SKUs: {len(sku_df) - len(unmapped_skus)}")

# Check validation SKUs with corrected logic
validation_skus = set(validation_df['Oracle Item Number'].astype(str))
unmapped_skus_list = set(unmapped_skus['Oracle Item Number'].astype(str))
validation_unmapped = validation_skus.intersection(unmapped_skus_list)

print(f"\nValidation SKUs: {len(validation_skus)}")
print(f"Validation SKUs that are unmapped: {len(validation_unmapped)}")

if len(validation_unmapped) > 0:
    print("\n⚠️  Validation SKUs that are unmapped:")
    for sku in validation_unmapped:
        val_info = validation_df[validation_df['Oracle Item Number'].astype(str) == sku]
        print(f"  SKU: {sku}")
        print(f"  Description: {val_info['Item Description'].iloc[0]}")
        print(f"  Department: {val_info['Department Name'].iloc[0]}")
else:
    print("✅ All validation SKUs have PAR location mapping!")

# Analyze unmapped SKUs
if len(unmapped_skus) > 0:
    print(f"\nUnmapped SKUs Analysis:")
    print(f"Top Departments:")
    dept_counts = unmapped_skus['Department Name'].value_counts()
    print(dept_counts.head())
    
    print(f"\nTop Suppliers:")
    supplier_counts = unmapped_skus['Supplier Name'].value_counts()
    print(supplier_counts.head())

print(f"\n✅ Corrected analysis complete!")
print(f"📊 Final dataset will have: {len(sku_df) - len(unmapped_skus):,} SKUs")
print(f"📊 Unmapped SKUs to remove: {len(unmapped_skus):,} SKUs")
