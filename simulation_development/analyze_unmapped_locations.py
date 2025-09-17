#!/usr/bin/env python3
"""
Analyze Unmapped Locations in CedarSim Data

This script analyzes the unmapped demand locations to identify potential
additional mappings based on naming patterns and context.
"""

import pandas as pd
import sys
import os
from pathlib import Path
from collections import Counter

# Add the simulation_development directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from data.input_data.location_mapper import LocationMapper
from data.input_data.data_integration import DataIntegrator

def analyze_unmapped_locations():
    """Analyze unmapped locations and suggest potential mappings."""
    print("=" * 80)
    print("CEDARSIM UNMAPPED LOCATIONS ANALYSIS")
    print("=" * 80)
    
    # Load data
    integrator = DataIntegrator()
    data = integrator.load_production_data()
    
    # Get unique locations from both datasets
    sku_locations = set(data['sku_data']['Deliver To'].dropna().astype(str).unique())
    demand_locations = set(data['demand_data']['Deliver to Location'].dropna().astype(str).unique())
    
    # Get current mappings
    mapper = LocationMapper()
    mapped_demand_locations = mapper.get_all_demand_locations()
    
    # Find unmapped demand locations
    unmapped_demand = demand_locations - mapped_demand_locations
    
    print(f"\n📊 Location Analysis Summary:")
    print(f"   Total SKU Locations: {len(sku_locations)}")
    print(f"   Total Demand Locations: {len(demand_locations)}")
    print(f"   Mapped Demand Locations: {len(mapped_demand_locations)}")
    print(f"   Unmapped Demand Locations: {len(unmapped_demand)}")
    
    if not unmapped_demand:
        print("\n✅ All demand locations are mapped!")
        return
    
    print(f"\n🔍 Unmapped Demand Locations ({len(unmapped_demand)}):")
    for loc in sorted(unmapped_demand):
        print(f"   - {loc}")
    
    # Analyze patterns in unmapped locations
    print(f"\n🔬 Pattern Analysis:")
    analyze_location_patterns(unmapped_demand, data['demand_data'])
    
    # Suggest potential mappings
    print(f"\n💡 Suggested Mappings:")
    suggest_mappings(unmapped_demand, sku_locations)

def analyze_location_patterns(unmapped_locations, demand_data):
    """Analyze patterns in unmapped locations."""
    print("   Analyzing naming patterns and usage...")
    
    # Count records per unmapped location
    location_counts = {}
    for loc in unmapped_locations:
        count = len(demand_data[demand_data['Deliver to Location'] == loc])
        location_counts[loc] = count
    
    # Sort by usage
    sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n   📈 Usage Statistics (Top 10):")
    for loc, count in sorted_locations[:10]:
        print(f"      {loc:<25} : {count:>6,} records")
    
    # Analyze naming patterns
    print(f"\n   🔤 Naming Pattern Analysis:")
    
    # Group by prefixes
    prefixes = {}
    for loc in unmapped_locations:
        if '_' in loc:
            prefix = loc.split('_')[0]
        elif loc.startswith('MDR'):
            prefix = 'MDR'
        else:
            prefix = 'OTHER'
        
        if prefix not in prefixes:
            prefixes[prefix] = []
        prefixes[prefix].append(loc)
    
    for prefix, locations in sorted(prefixes.items()):
        print(f"      {prefix:<10} : {len(locations)} locations")
        for loc in sorted(locations)[:3]:  # Show first 3
            print(f"         - {loc}")
        if len(locations) > 3:
            print(f"         ... and {len(locations) - 3} more")

def suggest_mappings(unmapped_locations, sku_locations):
    """Suggest potential mappings based on patterns."""
    print("   Analyzing potential mappings...")
    
    suggestions = []
    
    for demand_loc in unmapped_locations:
        potential_mappings = []
        
        # Pattern-based suggestions
        if 'MDR7010' in demand_loc:
            potential_mappings.append("Level 3 Medical (MDR7010ME pattern)")
            potential_mappings.append("Level 4 Medical (MDR7010ME pattern)")
            potential_mappings.append("Level 5 Observation, Medical Tele & Non-Tele (MDR7010ME pattern)")
        
        if 'MDR6' in demand_loc:
            potential_mappings.append("Level 6 Surgical (MDR6 pattern)")
            potential_mappings.append("Level 6 Telemetry, Cardiac & Stroke (MDR6 pattern)")
        
        if 'MDR7' in demand_loc:
            potential_mappings.append("Level 7 Surgical (MDR7 pattern)")
            potential_mappings.append("Level 7 ICU (MDR7 pattern)")
        
        if 'NORTH' in demand_loc.upper():
            potential_mappings.append("Level 1 ED (NORTH wing pattern)")
        
        if 'SOUTH' in demand_loc.upper():
            potential_mappings.append("Level 1 ED (SOUTH wing pattern)")
        
        if 'JIT' in demand_loc.upper():
            potential_mappings.append("Level 3 Central Lab (JIT pattern)")
        
        if 'OR' in demand_loc.upper() and 'MDR' in demand_loc:
            potential_mappings.append("Level 2 Surgery/Procedures/PACU (OR pattern)")
        
        if 'MS' in demand_loc.upper():
            potential_mappings.append("Level 6 Surgical (MS pattern)")
        
        if potential_mappings:
            suggestions.append((demand_loc, potential_mappings))
    
    if suggestions:
        for demand_loc, mappings in suggestions:
            print(f"\n   🎯 {demand_loc}:")
            for mapping in mappings:
                print(f"      - {mapping}")
    else:
        print("   No clear patterns found for automatic suggestions.")

def create_enhanced_mapping_suggestions():
    """Create enhanced mapping suggestions based on analysis."""
    print(f"\n📝 Enhanced Mapping Suggestions:")
    print("   Based on the analysis, here are suggested additions to the location mapper:")
    
    suggestions = [
        # MDR7010 variations
        ("MDR7010JI", "Level 3 Medical", "JIT/Just-In-Time pattern"),
        ("MDR7010OR", "Level 2 Surgery/Procedures/PACU", "OR/Operating Room pattern"),
        
        # MDR6 variations  
        ("MDR6170MS", "Level 6 Surgical", "MS/Medical Surgical pattern"),
        
        # Wing-based patterns
        ("MDR1NORTH", "Level 1 ED", "North wing of ED"),
        ("MDR1SOUTH", "Level 1 ED", "South wing of ED"),
        
        # Other patterns
        ("TORDC\\MDRCS", "Perpetual", "Central Supply with TORDC prefix"),
    ]
    
    print("\n   Suggested additions to location_mapper.py:")
    print("   ```python")
    print("   # Additional mappings based on pattern analysis")
    for demand_loc, sku_loc, reason in suggestions:
        print(f'   "{sku_loc}": "{demand_loc}",  # {reason}')
    print("   ```")

def main():
    """Run the unmapped locations analysis."""
    try:
        analyze_unmapped_locations()
        create_enhanced_mapping_suggestions()
        
        print(f"\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
