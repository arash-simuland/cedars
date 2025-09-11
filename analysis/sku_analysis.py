import pandas as pd

# Load the data
dept_rollup = pd.read_excel('2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx', sheet_name='01. Data (Department Rollup)')
full_data = pd.read_excel('2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx', sheet_name='02. Full Data')
safety_stock = pd.read_excel('2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx', sheet_name=0)

print('=== SKU ANALYSIS ===')
print(f'Department Rollup SKUs: {dept_rollup["Oracle Item Number"].nunique()}')
print(f'Full Data SKUs: {full_data["Oracle Item Number"].nunique()}')
print(f'Safety Stock SKUs: {safety_stock["Oracle Item Number"].nunique()}')

print(f'\n=== SKU OVERLAP ANALYSIS ===')
dept_skus = set(dept_rollup['Oracle Item Number'].unique())
full_skus = set(full_data['Oracle Item Number'].unique())
safety_skus = set(safety_stock['Oracle Item Number'].unique())

print(f'Department Rollup ∩ Full Data: {len(dept_skus.intersection(full_skus))}')
print(f'Department Rollup ∩ Safety Stock: {len(dept_skus.intersection(safety_skus))}')
print(f'Full Data ∩ Safety Stock: {len(full_skus.intersection(safety_skus))}')
print(f'All three datasets: {len(dept_skus.intersection(full_skus).intersection(safety_skus))}')

print(f'\n=== DEPARTMENT ANALYSIS ===')
print(f'Unique departments in Department Rollup: {dept_rollup["Department Name"].nunique()}')
print(f'Department names: {sorted(dept_rollup["Department Name"].unique())}')

print(f'\n=== PAR LOCATION ANALYSIS ===')
par_cols = [col for col in dept_rollup.columns if 'Level' in col or 'Perpetual' in col]
print(f'PAR locations: {len(par_cols)}')
print(f'PAR location names: {par_cols}')

print(f'\n=== SKU DISTRIBUTION BY PAR ===')
for col in par_cols[:5]:  # First 5 PAR locations
    non_null_count = dept_rollup[col].notna().sum()
    print(f'{col}: {non_null_count} SKUs')

print(f'\n=== SKU TYPE ANALYSIS ===')
print(f'On-PAR SKUs: {dept_rollup["On-PAR or Special Request"].value_counts()}')
print(f'Medline items: {dept_rollup["Medline item? Y/N"].value_counts()}')

print(f'\n=== SAMPLE SKU ANALYSIS ===')
print(f'First 10 SKUs in Department Rollup:')
print(dept_rollup[['Oracle Item Number', 'Item Description', 'Department Name', 'On-PAR or Special Request']].head(10))

print(f'\n=== SAFETY STOCK SAMPLE ANALYSIS ===')
print(f'First 10 SKUs in Safety Stock:')
print(safety_stock[['Oracle Item Number', 'Item Description', 'Department Name', 'Safety stock_units']].head(10))
