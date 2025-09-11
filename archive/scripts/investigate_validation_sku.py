import pandas as pd

print("Investigating validation SKU 30847...")
print("=" * 40)

# Load data
sku_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='01_SKU_Inventory_Clean')
validation_df = pd.read_excel('CedarSim_Simulation_Ready_Data.xlsx', sheet_name='03_Validation_Sample')

# Find the specific validation SKU
sku_30847 = sku_df[sku_df['Oracle Item Number'] == 30847]
print(f"Found SKU 30847: {len(sku_30847)} records")

if len(sku_30847) > 0:
    print(f"Description: {sku_30847['Item Description'].iloc[0]}")
    print(f"Department: {sku_30847['Department Name'].iloc[0]}")
    print(f"Supplier: {sku_30847['Supplier Name'].iloc[0]}")
    
    # Check all PAR columns for this SKU
    par_columns = [col for col in sku_df.columns if 'Level' in col or 'Perpetual' in col or 'Respiratory' in col]
    print(f"\nPAR column values for SKU 30847:")
    for col in par_columns:
        value = sku_30847[col].iloc[0]
        print(f"  {col}: {value} (type: {type(value)})")
        
        # Check if it's 'X' or has any value
        if pd.isna(value):
            print(f"    -> NaN (no mapping)")
        elif str(value).strip().upper() == 'X':
            print(f"    -> 'X' (has mapping)")
        else:
            print(f"    -> Other value: {value}")

# Check if this SKU is in validation set
val_30847 = validation_df[validation_df['Oracle Item Number'] == 30847]
print(f"\nIn validation set: {len(val_30847)} records")
if len(val_30847) > 0:
    print(f"Validation description: {val_30847['Item Description'].iloc[0]}")
    print(f"Validation department: {val_30847['Department Name'].iloc[0]}")

# Check the mapping logic again
print(f"\nTesting mapping logic:")
has_any_mapping = False
for col in par_columns:
    value = sku_30847[col].iloc[0]
    if pd.notna(value) and str(value).strip().upper() == 'X':
        print(f"  {col}: HAS MAPPING")
        has_any_mapping = True
    else:
        print(f"  {col}: no mapping")

print(f"\nOverall mapping status: {'HAS MAPPING' if has_any_mapping else 'NO MAPPING'}")
