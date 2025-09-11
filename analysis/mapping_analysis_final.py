import pandas as pd
import numpy as np

# Load the data
dept_rollup = pd.read_excel('2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx', sheet_name='01. Data (Department Rollup)')

# Get PAR location columns
par_cols = [col for col in dept_rollup.columns if 'Level' in col or 'Perpetual' in col]

print('=== SKU-TO-LOCATION MAPPING ANALYSIS ===')
print(f'Available PAR locations: {len(par_cols)}')
print(f'PAR location names: {par_cols}')

print(f'\n=== MAPPING COMPLETENESS ===')
# Analyze how many SKUs are mapped to each location
mapping_summary = []
for col in par_cols:
    mapped_skus = dept_rollup[col].notna().sum()
    total_skus = len(dept_rollup)
    percentage = (mapped_skus / total_skus) * 100
    mapping_summary.append({
        'Location': col,
        'Mapped_SKUs': mapped_skus,
        'Total_SKUs': total_skus,
        'Percentage': percentage
    })
    print(f'{col}: {mapped_skus}/{total_skus} SKUs ({percentage:.1f}%)')

print(f'\n=== MAPPING VALUE INTERPRETATION ===')
sample_col = par_cols[0]  # Use first PAR column as example
sample_values = dept_rollup[sample_col].dropna()
print(f'Sample column: {sample_col}')
print(f'Value range: {sample_values.min()} to {sample_values.max()}')
print(f'Value types: {sample_values.dtype}')
print(f'Sample values: {sample_values.head().tolist()}')

# Check if values are numeric (quantities) or categorical (presence/absence)
if pd.api.types.is_numeric_dtype(sample_values):
    print('Values appear to be QUANTITIES (numeric)')
    print('This suggests the mapping shows HOW MUCH of each SKU is stored at each location')
else:
    print('Values appear to be CATEGORICAL')
    print('This suggests the mapping shows WHETHER each SKU is stored at each location')

print(f'\n=== MAPPING EXAMPLES ===')
print('First 5 SKUs and their location mappings:')

for idx, row in dept_rollup.head().iterrows():
    print(f'\nSKU: {row["Oracle Item Number"]} - {row["Item Description"]}')
    print(f'Department: {row["Department Name"]}')
    mapped_locations = []
    for col in par_cols:
        if pd.notna(row[col]):
            mapped_locations.append(f'{col}: {row[col]}')
    if mapped_locations:
        print(f'Mapped to: {mapped_locations}')
    else:
        print('Not mapped to any PAR location')

print(f'\n=== MAPPING SUMMARY ===')
# Create a summary DataFrame
mapping_df = pd.DataFrame(mapping_summary).sort_values('Mapped_SKUs', ascending=False)
print(mapping_df)

# Calculate overall mapping statistics
total_mapped = dept_rollup[par_cols].notna().sum(axis=1)
print(f'\nMapping Statistics:')
print(f'SKUs with at least one location: {(total_mapped > 0).sum()}')
print(f'SKUs with no locations: {(total_mapped == 0).sum()}')
print(f'SKUs with multiple locations: {(total_mapped > 1).sum()}')
print(f'Average locations per SKU: {total_mapped.mean():.2f}')

print(f'\n=== CONCLUSION ===')
if (total_mapped > 0).sum() > len(dept_rollup) * 0.8:
    print('✅ YES - The Excel sheet shows a CLEAR map of where each item is in the hospital')
    print('   Most SKUs have location mappings')
elif (total_mapped > 0).sum() > len(dept_rollup) * 0.5:
    print('⚠️ PARTIAL - The Excel sheet shows a PARTIAL map of where items are located')
    print('   Some SKUs have location mappings, but many do not')
else:
    print('❌ NO - The Excel sheet does NOT show a clear map of where items are located')
    print('   Most SKUs lack location mappings')
