#!/usr/bin/env python3
"""
Filter Final List to Demand Coverage

This script:
1. Removes SKUs from the final list that don't have historical demand data
2. Keeps only SKUs that have both final list data AND historical demand data
3. Records which SKUs were removed due to lack of historical data
4. Creates filtered datasets for simulation use
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime

def filter_final_list_to_demand_coverage():
    """Filter final list to only include SKUs with historical demand data."""
    
    print("=" * 80)
    print("FILTERING FINAL LIST TO DEMAND COVERAGE")
    print("=" * 80)
    
    # Load data
    print("\n1. Loading data...")
    source_skus = pd.read_excel('simulation_development/data/prod-input-data/2025-09-12-final-list-with-results.xlsx')
    demand_data = pd.read_csv('simulation_development/data/archive-input_data/historical_demand_data.csv')
    
    print(f"   ✅ Source SKUs: {len(source_skus):,} records")
    print(f"   ✅ Demand data: {len(demand_data):,} records")
    
    # Get unique SKUs
    source_str = set(str(x) for x in source_skus['Oracle Item Number'].unique())
    demand_str = set(str(x) for x in demand_data['Oracle Item Number'].unique())
    
    print(f"\n2. Analyzing SKU coverage...")
    print(f"   Source unique SKUs: {len(source_str):,}")
    print(f"   Demand unique SKUs: {len(demand_str):,}")
    
    # Normalize SKUs (remove leading zeros for comparison)
    source_normalized = set(x.lstrip('0') or '0' for x in source_str)
    demand_normalized = set(x.lstrip('0') or '0' for x in demand_str)
    
    # Find overlap
    overlap_normalized = source_normalized.intersection(demand_normalized)
    missing_from_demand = source_normalized - demand_normalized
    
    print(f"   Overlap (normalized): {len(overlap_normalized):,}")
    print(f"   Missing from demand: {len(missing_from_demand):,}")
    print(f"   Coverage: {len(overlap_normalized)/len(source_str)*100:.1f}%")
    
    # Create mapping from normalized back to original SKUs
    source_to_normalized = {x: x.lstrip('0') or '0' for x in source_str}
    normalized_to_source = {}
    for orig, norm in source_to_normalized.items():
        if norm not in normalized_to_source:
            normalized_to_source[norm] = []
        normalized_to_source[norm].append(orig)
    
    # Find SKUs to keep (have demand data)
    skus_to_keep = set()
    for norm_sku in overlap_normalized:
        if norm_sku in normalized_to_source:
            skus_to_keep.update(normalized_to_source[norm_sku])
    
    # Find SKUs to remove (no demand data)
    skus_to_remove = set()
    for norm_sku in missing_from_demand:
        if norm_sku in normalized_to_source:
            skus_to_remove.update(normalized_to_source[norm_sku])
    
    print(f"\n3. Filtering data...")
    print(f"   SKUs to keep: {len(skus_to_keep):,}")
    print(f"   SKUs to remove: {len(skus_to_remove):,}")
    
    # Filter source data
    filtered_source = source_skus[source_skus['Oracle Item Number'].isin(skus_to_keep)].copy()
    removed_source = source_skus[source_skus['Oracle Item Number'].isin(skus_to_remove)].copy()
    
    # Filter demand data to only include kept SKUs
    # Need to normalize demand SKUs for matching
    demand_data['Oracle Item Number Normalized'] = demand_data['Oracle Item Number'].astype(str).apply(lambda x: x.lstrip('0') or '0')
    kept_normalized = set(x.lstrip('0') or '0' for x in skus_to_keep)
    filtered_demand = demand_data[demand_data['Oracle Item Number Normalized'].isin(kept_normalized)].copy()
    filtered_demand = filtered_demand.drop('Oracle Item Number Normalized', axis=1)
    
    print(f"   Filtered source: {len(filtered_source):,} records")
    print(f"   Removed source: {len(removed_source):,} records")
    print(f"   Filtered demand: {len(filtered_demand):,} records")
    
    # Create output directory
    output_dir = Path('simulation_development/data/prod-input-data/filtered')
    output_dir.mkdir(exist_ok=True)
    
    # Save filtered data
    print(f"\n4. Saving filtered data...")
    
    # Save filtered final list
    filtered_source_file = output_dir / '2025-09-12-final-list-filtered.xlsx'
    filtered_source.to_excel(filtered_source_file, index=False)
    print(f"   ✅ Filtered final list: {filtered_source_file}")
    
    # Save filtered demand data
    filtered_demand_file = output_dir / 'historical_demand_filtered.csv'
    filtered_demand.to_csv(filtered_demand_file, index=False)
    print(f"   ✅ Filtered demand data: {filtered_demand_file}")
    
    # Save removed SKUs record
    removed_file = output_dir / 'removed_skus_no_demand_data.csv'
    removed_source.to_csv(removed_file, index=False)
    print(f"   ✅ Removed SKUs record: {removed_file}")
    
    # Create summary report
    summary_file = output_dir / 'filtering_summary.txt'
    with open(summary_file, 'w') as f:
        f.write("FINAL LIST FILTERING SUMMARY\n")
        f.write("=" * 50 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Original final list SKUs: {len(source_str):,}\n")
        f.write(f"SKUs with demand data: {len(skus_to_keep):,}\n")
        f.write(f"SKUs removed (no demand): {len(skus_to_remove):,}\n")
        f.write(f"Coverage: {len(skus_to_keep)/len(source_str)*100:.1f}%\n")
        f.write(f"\nFiltered final list records: {len(filtered_source):,}\n")
        f.write(f"Filtered demand records: {len(filtered_demand):,}\n")
        f.write(f"Removed SKUs records: {len(removed_source):,}\n")
        f.write(f"\nFiles created:\n")
        f.write(f"- {filtered_source_file.name}\n")
        f.write(f"- {filtered_demand_file.name}\n")
        f.write(f"- {removed_file.name}\n")
    
    print(f"   ✅ Summary report: {summary_file}")
    
    # Show sample of removed SKUs
    print(f"\n5. Sample of removed SKUs (no demand data):")
    removed_skus_sample = removed_source['Oracle Item Number'].unique()[:20]
    for sku in removed_skus_sample:
        print(f"   - {sku}")
    
    print(f"\n" + "=" * 80)
    print("✅ FILTERING COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    return {
        'filtered_source': filtered_source,
        'filtered_demand': filtered_demand,
        'removed_source': removed_source,
        'coverage_percentage': len(skus_to_keep)/len(source_str)*100
    }

if __name__ == "__main__":
    result = filter_final_list_to_demand_coverage()
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Coverage: {result['coverage_percentage']:.1f}%")
    print(f"   SKUs kept: {len(result['filtered_source']['Oracle Item Number'].unique()):,}")
    print(f"   SKUs removed: {len(result['removed_source']['Oracle Item Number'].unique()):,}")
    print(f"   Demand records: {len(result['filtered_demand']):,}")
