import pandas as pd

# Load data
sku_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='01_SKU_Inventory_Clean')
validation_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='03_Validation_Sample')

# Find unmapped SKUs
par_columns = [col for col in sku_df.columns if 'Level' in col or 'Perpetual' in col or 'Respiratory' in col]
sku_df['has_par_mapping'] = sku_df[par_columns].notna().any(axis=1)
unmapped_skus = sku_df[~sku_df['has_par_mapping']]

# Check validation SKUs
validation_skus = set(validation_df['Oracle Item Number'].astype(str))
unmapped_skus_list = set(unmapped_skus['Oracle Item Number'].astype(str))
validation_unmapped = validation_skus.intersection(unmapped_skus_list)

print(f"Total validation SKUs: {len(validation_skus)}")
print(f"Total unmapped SKUs: {len(unmapped_skus_list)}")
print(f"Validation SKUs that are unmapped: {len(validation_unmapped)}")

if len(validation_unmapped) > 0:
    print("\nValidation SKU that is unmapped:")
    for sku in validation_unmapped:
        print(f"SKU: {sku}")
        val_info = validation_df[validation_df['Oracle Item Number'].astype(str) == sku]
        print(f"Description: {val_info['Item Description'].iloc[0]}")
        print(f"Department: {val_info['Department Name'].iloc[0]}")
        
        # Check if this SKU has any PAR mapping
        sku_info = sku_df[sku_df['Oracle Item Number'].astype(str) == sku]
        print(f"Has PAR mapping: {sku_info['has_par_mapping'].iloc[0]}")
        print(f"PAR columns with values:")
        for col in par_columns:
            if sku_info[col].notna().any():
                print(f"  {col}: {sku_info[col].iloc[0]}")
