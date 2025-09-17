#!/usr/bin/env python3
import pandas as pd

# Load demand data
demand_data = pd.read_csv('data/prod-input-data/SIMULATION_READY_DEMAND_DATA.csv')

print('=== SURGICAL DEMAND DATA ANALYSIS ===')
print()

# Look for surgical-related locations
surgical_locations = [loc for loc in demand_data['Deliver to Location'].unique() if 'SURGERY' in str(loc).upper() or 'OR' in str(loc).upper()]
print('Surgical-related locations in demand data:')
for loc in sorted(surgical_locations):
    print(f'  - {loc}')

print()
print('=== SAMPLE SURGICAL DEMAND RECORDS ===')
surgical_demand = demand_data[demand_data['Deliver to Location'].isin(surgical_locations)]
print(f'Total surgical demand records: {len(surgical_demand)}')
print()
print('Sample records:')
print(surgical_demand[['Deliver to Location', 'Department Name', 'Department Number', 'Business Unit']].head(10))

print()
print('=== DEPARTMENT ANALYSIS FOR SURGICAL LOCATIONS ===')
for loc in surgical_locations:
    loc_data = demand_data[demand_data['Deliver to Location'] == loc]
    depts = loc_data['Department Name'].unique()
    print(f'{loc}:')
    for dept in depts:
        print(f'  - {dept}')
    print()
