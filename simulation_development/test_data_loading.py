#!/usr/bin/env python3
"""
Test script to verify data loading and model structure creation
"""

import sys
import os
from pathlib import Path

# Add the simulation_development directory to the path
sys.path.append(os.path.dirname(__file__))

from data.input_data.data_integration import create_integrated_antology
from core.core_models import AntologyGenerator

def test_data_loading():
    """Test the data loading and model structure creation."""
    
    print("=" * 60)
    print("TESTING CEDARSIM DATA LOADING AND MODEL STRUCTURE")
    print("=" * 60)
    
    try:
        # Test with validation subset first
        print("\n1. Testing with validation subset...")
        antology, integrator = create_integrated_antology(use_validation_subset=True)
        
        print(f"   ✅ Successfully loaded validation subset")
        print(f"   📊 Locations: {len(antology.locations)}")
        print(f"   📊 SKUs: {len(antology.sku_registry)}")
        
        # Test network status
        status = antology.get_network_status()
        print(f"   📊 Total SKU instances: {status['total_skus']}")
        print(f"   📊 Total locations: {status['total_locations']}")
        
        # Test with full dataset
        print("\n2. Testing with full dataset...")
        antology_full, integrator_full = create_integrated_antology(use_validation_subset=False)
        
        print(f"   ✅ Successfully loaded full dataset")
        print(f"   📊 Locations: {len(antology_full.locations)}")
        print(f"   📊 SKUs: {len(antology_full.sku_registry)}")
        
        # Test network status
        status_full = antology_full.get_network_status()
        print(f"   📊 Total SKU instances: {status_full['total_skus']}")
        print(f"   📊 Total locations: {status_full['total_locations']}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - DATA LOADING IS WORKING!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_loading()
    sys.exit(0 if success else 1)
