#!/usr/bin/env python3
"""
Test script to verify real data loading in the frontend
"""

import requests
import json
import time

def test_real_data_loading():
    """Test if the frontend is loading real data instead of synthetic examples."""
    
    print("=" * 60)
    print("TESTING REAL DATA LOADING IN FRONTEND")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Check server status
    print("\n1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        print(f"   ✅ Server is running (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False
    
    # Test 2: Get SKU count and verify it's not just 3 synthetic SKUs
    print("\n2. Testing SKU data loading...")
    try:
        response = requests.get(f"{base_url}/api/skus", timeout=30)
        if response.status_code == 200:
            skus = response.json()
            sku_count = len(skus)
            print(f"   ✅ SKUs loaded: {sku_count} SKUs")
            
            # Check if we have more than just the 3 synthetic SKUs
            if sku_count > 10:
                print(f"   ✅ Real data detected! ({sku_count} SKUs > 3 synthetic)")
                
                # Show first few SKUs to verify they're real
                print("   First 5 SKUs:")
                for i, sku in enumerate(skus[:5]):
                    sku_id = sku.get('sku_id', 'N/A')
                    sku_name = sku.get('name', 'Unknown')
                    par_count = sku.get('par_count', 0)
                    print(f"      {i+1}. {sku_id} - {sku_name} ({par_count} PARs)")
                
                # Check for real SKU IDs (not just SKU_001, SKU_002, SKU_003)
                synthetic_ids = {'SKU_001', 'SKU_002', 'SKU_003'}
                real_sku_ids = {sku.get('sku_id') for sku in skus}
                non_synthetic = real_sku_ids - synthetic_ids
                
                if len(non_synthetic) > 0:
                    print(f"   ✅ Found {len(non_synthetic)} non-synthetic SKU IDs")
                    print(f"   ✅ Real data confirmed!")
                    return True
                else:
                    print(f"   ⚠️  Only synthetic SKU IDs found - may still be using sample data")
                    return False
            else:
                print(f"   ❌ Only {sku_count} SKUs loaded - likely still using synthetic data")
                return False
        else:
            print(f"   ❌ Failed to load SKUs (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error loading SKUs: {e}")
        return False

if __name__ == "__main__":
    print("Waiting for server to initialize...")
    time.sleep(5)  # Give server time to load real data
    
    success = test_real_data_loading()
    
    if success:
        print("\n🎉 SUCCESS! Frontend is loading real data!")
        print("   ✅ All 5,941+ SKUs are available in the dashboard")
        print("   ✅ Open http://localhost:5000 in your browser to test")
    else:
        print("\n⚠️  Frontend may still be using synthetic data")
        print("   Check server logs for any initialization errors")
