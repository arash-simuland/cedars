#!/usr/bin/env python3
"""
Check if we have demand data for the new items
"""

import pandas as pd
from pathlib import Path

def check_demand_for_new_items():
    """Check demand data availability for new items"""
    
    print('🔍 Checking demand data for new items...')
    
    # Load data
    new_file = Path('data/archive/original/2025-09-12_MDRH_Item_List.xlsx')
    existing_sku = Path('data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv')
    existing_demand = Path('data/final/csv_complete/02_Demand_Data_Clean_Complete.csv')
    
    # Load files
    new_data = pd.read_excel(new_file, sheet_name='Sheet1')
    existing_sku_data = pd.read_csv(existing_sku)
    existing_demand_data = pd.read_csv(existing_demand)
    
    print(f'New data shape: {new_data.shape}')
    print(f'Existing SKU data shape: {existing_sku_data.shape}')
    print(f'Existing demand data shape: {existing_demand_data.shape}')
    
    # Find new items
    new_items = set(new_data['Oracle Item Number'])
    existing_items = set(existing_sku_data['Oracle Item Number'])
    new_only_items = new_items - existing_items
    
    print(f'\n📊 Item Analysis:')
    print(f'New items: {len(new_items)}')
    print(f'Existing items: {len(existing_items)}')
    print(f'New-only items: {len(new_only_items)}')
    
    # Check demand data for new items
    demand_items = set(existing_demand_data['Oracle Item Number'])
    new_items_with_demand = new_only_items & demand_items
    new_items_without_demand = new_only_items - demand_items
    
    print(f'\n📈 Demand Analysis:')
    print(f'Total demand items: {len(demand_items)}')
    print(f'New items WITH demand: {len(new_items_with_demand)}')
    print(f'New items WITHOUT demand: {len(new_items_without_demand)}')
    
    if len(new_items_with_demand) > 0:
        print(f'\n✅ New items that have demand data:')
        sample_with_demand = list(new_items_with_demand)[:5]
        for item in sample_with_demand:
            item_demand = existing_demand_data[existing_demand_data['Oracle Item Number'] == item]
            print(f'  {item}: {len(item_demand)} demand records')
            if len(item_demand) > 0:
                print(f'    Sample demand: {item_demand["Total Quantity"].iloc[0]} units on {item_demand["PO Week Ending Date"].iloc[0]}')
    
    if len(new_items_without_demand) > 0:
        print(f'\n❌ New items that need demand data:')
        sample_without_demand = list(new_items_without_demand)[:5]
        for item in sample_without_demand:
            print(f'  {item}')
    
    print(f'\n📊 Summary:')
    print(f'New items with demand: {len(new_items_with_demand)}/{len(new_only_items)} ({len(new_items_with_demand)/len(new_only_items)*100:.1f}%)')
    print(f'New items without demand: {len(new_items_without_demand)}/{len(new_only_items)} ({len(new_items_without_demand)/len(new_only_items)*100:.1f}%)')
    
    # Check if new items have burn rates in the new data
    print(f'\n🔥 Burn Rate Analysis:')
    new_data_with_burn_rates = new_data[new_data['burn_rate'].notna() & (new_data['burn_rate'] > 0)]
    new_items_with_burn_rates = set(new_data_with_burn_rates['Oracle Item Number'])
    new_only_with_burn_rates = new_items_with_burn_rates & new_only_items
    
    print(f'New items with burn rates: {len(new_only_with_burn_rates)}/{len(new_only_items)} ({len(new_only_with_burn_rates)/len(new_only_items)*100:.1f}%)')
    
    # Show sample burn rates for new items
    if len(new_only_with_burn_rates) > 0:
        print(f'\n📋 Sample burn rates for new items:')
        sample_burn_rates = list(new_only_with_burn_rates)[:5]
        for item in sample_burn_rates:
            item_data = new_data[new_data['Oracle Item Number'] == item].iloc[0]
            print(f'  {item}: {item_data["burn_rate"]} units/day')
    
    return {
        'new_items_with_demand': len(new_items_with_demand),
        'new_items_without_demand': len(new_items_without_demand),
        'new_items_with_burn_rates': len(new_only_with_burn_rates),
        'total_new_items': len(new_only_items)
    }

if __name__ == "__main__":
    results = check_demand_for_new_items()
    
    print(f'\n🎯 CONCLUSION:')
    if results['new_items_with_demand'] > 0:
        print(f'✅ {results["new_items_with_demand"]} new items have demand data - can be simulated')
    else:
        print(f'❌ No new items have demand data - need to generate demand patterns')
    
    if results['new_items_with_burn_rates'] > 0:
        print(f'✅ {results["new_items_with_burn_rates"]} new items have burn rates - can estimate demand')
    else:
        print(f'❌ No new items have burn rates - need demand data')
