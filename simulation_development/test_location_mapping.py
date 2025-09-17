#!/usr/bin/env python3
"""
Test script for CedarSim Location Mapping

This script tests the location mapping functionality to ensure it works correctly
with the actual data.
"""

import sys
import os
from pathlib import Path

# Add the simulation_development directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from data.input_data.location_mapper import LocationMapper
from data.input_data.data_integration import DataIntegrator

def test_location_mapper():
    """Test the location mapper with sample data."""
    print("=" * 60)
    print("TESTING CEDARSIM LOCATION MAPPER")
    print("=" * 60)
    
    # Create location mapper
    mapper = LocationMapper()
    
    # Test individual mappings
    print("\n🧪 Testing Individual Mappings:")
    test_cases = [
        ("Level 1 ED", "MDRER"),
        ("Level 2 ICU", "MDRICUPRO"),
        ("Level 6 Surgical", "MDRSURGERY"),
        ("Perpetual", "MDRCS"),
        ("Level 3 Medical", "MDR7010ME"),
        ("Unknown Location", None)
    ]
    
    for sku_loc, expected_demand_loc in test_cases:
        actual_demand_loc = mapper.map_sku_to_demand_location(sku_loc)
        status = "✅" if actual_demand_loc == expected_demand_loc else "❌"
        print(f"   {status} {sku_loc:<30} → {actual_demand_loc}")
    
    # Test reverse mappings
    print("\n🔄 Testing Reverse Mappings:")
    test_demand_locations = ["MDRER", "MDRSURGERY", "MDRCS", "UnknownDemand"]
    
    for demand_loc in test_demand_locations:
        sku_locs = mapper.map_demand_to_sku_locations(demand_loc)
        print(f"   {demand_loc:<15} ← {sku_locs}")
    
    # Print mapping summary
    mapper.print_mapping_summary()

def test_data_integration():
    """Test the data integration with location mapping."""
    print("\n" + "=" * 60)
    print("TESTING DATA INTEGRATION WITH LOCATION MAPPING")
    print("=" * 60)
    
    try:
        # Create data integrator
        integrator = DataIntegrator()
        
        # Load production data (this will trigger location mapping validation)
        print("\n📊 Loading production data...")
        data = integrator.load_production_data()
        
        print(f"\n✅ Data loaded successfully:")
        print(f"   SKU Records: {len(data['sku_data']):,}")
        print(f"   Demand Records: {len(data['demand_data']):,}")
        print(f"   Validation Records: {len(data['validation_data']):,}")
        
        # Test creating antology structure
        print("\n🏗️  Creating antology structure...")
        antology = integrator.create_antology_structure(use_validation_subset=True)
        
        print(f"\n✅ Antology created successfully:")
        print(f"   Locations: {len(antology.locations)}")
        print(f"   SKU Instances: {sum(len(sku_list) for sku_list in antology.sku_registry.values())}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during data integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Starting CedarSim Location Mapping Tests")
    
    # Test location mapper
    test_location_mapper()
    
    # Test data integration
    success = test_data_integration()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    else:
        print("❌ SOME TESTS FAILED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
