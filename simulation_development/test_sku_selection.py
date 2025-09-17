#!/usr/bin/env python3
"""
Test script to verify SKU selection functionality
"""

import requests
import json

def test_sku_selection():
    """Test SKU selection and data retrieval."""
    
    print("=" * 60)
    print("TESTING SKU SELECTION FUNCTIONALITY")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Get SKU list
    print("\n1. Getting SKU list...")
    try:
        response = requests.get(f"{base_url}/api/skus", timeout=10)
        if response.status_code == 200:
            skus = response.json()
            print(f"   ✅ Loaded {len(skus)} SKUs")
            
            # Test first few SKUs
            test_skus = skus[:3]
            for i, sku in enumerate(test_skus):
                sku_id = sku.get('sku_id')
                sku_name = sku.get('name', 'Unknown')
                par_count = sku.get('par_count', 0)
                print(f"   {i+1}. {sku_id} - {sku_name} ({par_count} PARs)")
        else:
            print(f"   ❌ Failed to load SKUs (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error loading SKUs: {e}")
        return False
    
    # Test 2: Test specific SKU details
    print("\n2. Testing specific SKU details...")
    try:
        test_sku_id = test_skus[0]['sku_id']
        response = requests.get(f"{base_url}/api/sku/{test_sku_id}", timeout=10)
        if response.status_code == 200:
            sku_details = response.json()
            print(f"   ✅ SKU details loaded for {test_sku_id}")
            
            # Check perpetual SKU data
            perpetual_sku = sku_details.get('perpetual_sku', {})
            if perpetual_sku:
                print(f"   Perpetual: Level {perpetual_sku.get('current_level', 'N/A')}")
            
            # Check PAR SKUs
            par_skus = sku_details.get('par_skus', [])
            print(f"   PARs with this SKU: {len(par_skus)}")
            for par_sku in par_skus[:3]:  # Show first 3
                location = par_sku.get('location_id', 'Unknown')
                level = par_sku.get('current_level', 'N/A')
                print(f"      {location}: Level {level}")
            
            if len(par_skus) > 3:
                print(f"      ... and {len(par_skus) - 3} more PARs")
        else:
            print(f"   ❌ Failed to load SKU details (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error loading SKU details: {e}")
        return False
    
    # Test 3: Test different SKU
    print("\n3. Testing different SKU...")
    try:
        if len(test_skus) > 1:
            test_sku_id_2 = test_skus[1]['sku_id']
            response = requests.get(f"{base_url}/api/sku/{test_sku_id_2}", timeout=10)
            if response.status_code == 200:
                sku_details_2 = response.json()
                print(f"   ✅ SKU details loaded for {test_sku_id_2}")
                
                # Compare with first SKU
                perpetual_sku_2 = sku_details_2.get('perpetual_sku', {})
                if perpetual_sku_2:
                    level_2 = perpetual_sku_2.get('current_level', 'N/A')
                    print(f"   Perpetual: Level {level_2}")
                
                par_skus_2 = sku_details_2.get('par_skus', [])
                print(f"   PARs with this SKU: {len(par_skus_2)}")
                
                # Check if different from first SKU
                if len(par_skus) != len(par_skus_2):
                    print(f"   ✅ Different SKU has different PAR distribution")
                else:
                    print(f"   ℹ️  Same number of PARs as first SKU")
            else:
                print(f"   ❌ Failed to load second SKU details (Status: {response.status_code})")
                return False
        else:
            print(f"   ℹ️  Only one SKU available for testing")
    except Exception as e:
        print(f"   ❌ Error loading second SKU details: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("SKU SELECTION TEST COMPLETED")
    print("=" * 60)
    print("✅ SKU selection and data retrieval is working!")
    print("✅ Frontend should now update PAR levels when selecting different SKUs")
    print("✅ Open http://localhost:5000 and test the dropdown selection")
    
    return True

if __name__ == "__main__":
    success = test_sku_selection()
    if success:
        print("\n🎉 Ready for frontend testing!")
    else:
        print("\n⚠️  Some issues found - check the output above")
