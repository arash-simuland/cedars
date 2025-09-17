#!/usr/bin/env python3
"""
Create Validation Subset Data

This script creates a subset of the historical demand data and SKU inventory data
that matches exactly the validation test SKUs and time range for fair comparison.
"""

import pandas as pd
import os
from pathlib import Path

def create_validation_subset():
    """Create subset data that matches validation test range and SKUs."""
    
    print("=" * 80)
    print("CREATING VALIDATION SUBSET DATA")
    print("=" * 80)
    
    # Load original data
    print("\n1. Loading original data...")
    demand_data = pd.read_csv('data/final/csv_complete/02_Demand_Data_Clean_Complete.csv')
    sku_data = pd.read_csv('data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv')
    validation_data = pd.read_csv('data/final/csv_complete/03_Validation_Sample_Complete.csv')
    
    print(f"   ✅ Demand data: {len(demand_data):,} records")
    print(f"   ✅ SKU data: {len(sku_data):,} SKUs")
    print(f"   ✅ Validation data: {len(validation_data):,} records")
    
    # Get validation SKUs and convert to strings for matching
    val_skus = validation_data['Oracle Item Number'].unique()
    val_skus_str = [str(sku) for sku in val_skus]
    print(f"\n2. Validation SKUs: {len(val_skus)} unique SKUs")
    print(f"   SKUs: {val_skus.tolist()}")
    print(f"   SKUs as strings: {val_skus_str}")
    
    # Create subset of demand data for validation SKUs
    print("\n3. Creating demand subset...")
    # Convert demand data Oracle Item Number to string for matching
    demand_data['Oracle Item Number'] = demand_data['Oracle Item Number'].astype(str)
    demand_subset = demand_data[demand_data['Oracle Item Number'].isin(val_skus_str)].copy()
    
    print(f"   ✅ Demand subset: {len(demand_subset):,} records")
    print(f"   ✅ Time range: {demand_subset['PO Week Ending Date'].min()} to {demand_subset['PO Week Ending Date'].max()}")
    print(f"   ✅ SKUs with demand data: {demand_subset['Oracle Item Number'].nunique()}")
    
    # Create subset of SKU data for validation SKUs
    print("\n4. Creating SKU subset...")
    # SKU data already has Oracle Item Number as string
    sku_subset = sku_data[sku_data['Oracle Item Number'].isin(val_skus_str)].copy()
    
    print(f"   ✅ SKU subset: {len(sku_subset):,} SKUs")
    
    # Check which validation SKUs have no demand data
    skus_with_demand = set(demand_subset['Oracle Item Number'].unique())
    skus_without_demand = set(val_skus) - skus_with_demand
    
    if len(skus_without_demand) > 0:
        print(f"\n⚠️  WARNING: {len(skus_without_demand)} validation SKUs have no historical demand data:")
        print(f"   {sorted(skus_without_demand)}")
        print("   These SKUs will be excluded from the subset.")
    
    # Check why SKU subset might be empty
    print(f"\n   Debug: SKU data Oracle Item Number type: {sku_data['Oracle Item Number'].dtype}")
    print(f"   Debug: Validation SKUs type: {type(val_skus[0])}")
    print(f"   Debug: SKU data sample: {sku_data['Oracle Item Number'].head().tolist()}")
    print(f"   Debug: Validation SKUs sample: {val_skus[:5].tolist()}")
    
    # Create output directory
    output_dir = Path('data/final/validation_subset')
    output_dir.mkdir(exist_ok=True)
    
    # Save subset files
    print("\n5. Saving subset files...")
    
    # Save demand subset
    demand_output = output_dir / 'validation_demand_subset.csv'
    demand_subset.to_csv(demand_output, index=False)
    print(f"   ✅ Saved: {demand_output}")
    
    # Save SKU subset
    sku_output = output_dir / 'validation_sku_subset.csv'
    sku_subset.to_csv(sku_output, index=False)
    print(f"   ✅ Saved: {sku_output}")
    
    # Save validation data (copy)
    val_output = output_dir / 'validation_test_data.csv'
    validation_data.to_csv(val_output, index=False)
    print(f"   ✅ Saved: {val_output}")
    
    # Create summary report
    print("\n6. Creating summary report...")
    summary = {
        'original_demand_records': len(demand_data),
        'original_sku_count': len(sku_data),
        'validation_sku_count': len(val_skus),
        'subset_demand_records': len(demand_subset),
        'subset_sku_count': len(sku_subset),
        'skus_with_demand': len(skus_with_demand),
        'skus_without_demand': len(skus_without_demand),
        'time_range_start': str(demand_subset['PO Week Ending Date'].min()),
        'time_range_end': str(demand_subset['PO Week Ending Date'].max()),
        'skus_with_demand_list': [int(x) for x in sorted(skus_with_demand)],
        'skus_without_demand_list': [int(x) for x in sorted(skus_without_demand)]
    }
    
    summary_file = output_dir / 'validation_subset_summary.json'
    import json
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"   ✅ Saved: {summary_file}")
    
    print("\n" + "=" * 80)
    print("✅ VALIDATION SUBSET CREATED SUCCESSFULLY!")
    print("=" * 80)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Validation SKUs: {len(val_skus)}")
    print(f"   SKUs with demand data: {len(skus_with_demand)}")
    print(f"   SKUs without demand data: {len(skus_without_demand)}")
    print(f"   Demand records: {len(demand_subset):,}")
    print(f"   Time range: {demand_subset['PO Week Ending Date'].min()} to {demand_subset['PO Week Ending Date'].max()}")
    
    return summary

if __name__ == "__main__":
    summary = create_validation_subset()
