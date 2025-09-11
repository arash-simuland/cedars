#!/usr/bin/env python3
"""
Detailed analysis of SKU counts and data structure in both files.
"""

import pandas as pd

def detailed_analysis():
    """Perform detailed analysis of both files."""
    
    print("🔍 Detailed SKU Analysis")
    print("=" * 60)
    
    try:
        # Read our pipeline output
        print("📂 Our pipeline output analysis:")
        our_file = pd.read_excel('CedarSim_Simulation_Ready_Data_Final.xlsx', sheet_name='01_SKU_Inventory_Final')
        print(f"   Total rows: {len(our_file)}")
        print(f"   Unique Oracle Item Numbers: {our_file['Oracle Item Number'].nunique()}")
        print(f"   Duplicate Oracle Item Numbers: {len(our_file) - our_file['Oracle Item Number'].nunique()}")
        
        # Check for duplicates
        duplicates = our_file[our_file.duplicated(subset=['Oracle Item Number'], keep=False)]
        if len(duplicates) > 0:
            print(f"   Duplicate SKUs found:")
            for sku in duplicates['Oracle Item Number'].unique()[:5]:  # Show first 5
                print(f"     - {sku}")
        
        print()
        
        # Read the FIXED file
        print("📂 FIXED file analysis:")
        fixed_file = pd.read_excel('CedarSim_Simulation_Ready_Data_FIXED.xlsx', sheet_name='Data')
        print(f"   Total rows: {len(fixed_file)}")
        
        # Check if first row is header
        print(f"   First few values in column C:")
        print(f"     Row 0: {fixed_file.iloc[0, 2]}")
        print(f"     Row 1: {fixed_file.iloc[1, 2]}")
        print(f"     Row 2: {fixed_file.iloc[2, 2]}")
        
        # Try different approaches to get SKUs
        print(f"\n   Trying different approaches:")
        
        # Approach 1: Skip first row
        skus_skip_first = fixed_file.iloc[1:, 2].astype(str)
        print(f"   Skip first row: {len(skus_skip_first)} rows, {skus_skip_first.nunique()} unique")
        
        # Approach 2: Use all rows
        skus_all = fixed_file.iloc[:, 2].astype(str)
        print(f"   All rows: {len(skus_all)} rows, {skus_all.nunique()} unique")
        
        # Approach 3: Check if there are empty values
        skus_clean = skus_skip_first[skus_skip_first != 'nan'].dropna()
        print(f"   Clean (no NaN): {len(skus_clean)} rows, {skus_clean.nunique()} unique")
        
        # Show some sample values
        print(f"\n   Sample SKU values (first 10):")
        for i, sku in enumerate(skus_clean.head(10)):
            print(f"     {i+1}: {sku}")
        
        # Compare with our data
        our_skus = set(our_file['Oracle Item Number'].astype(str))
        fixed_skus = set(skus_clean)
        
        print(f"\n🔍 Comparison:")
        print(f"   Our pipeline unique SKUs: {len(our_skus)}")
        print(f"   FIXED file unique SKUs: {len(fixed_skus)}")
        print(f"   Difference: {len(fixed_skus) - len(our_skus)}")
        
        missing_from_ours = fixed_skus - our_skus
        extra_in_ours = our_skus - fixed_skus
        
        if missing_from_ours:
            print(f"\n❌ Missing from our pipeline ({len(missing_from_ours)}):")
            for sku in sorted(list(missing_from_ours)[:10]):  # Show first 10
                print(f"   - {sku}")
        
        if extra_in_ours:
            print(f"\n➕ Extra in our pipeline ({len(extra_in_ours)}):")
            for sku in sorted(list(extra_in_ours)[:10]):  # Show first 10
                print(f"   + {sku}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    detailed_analysis()
