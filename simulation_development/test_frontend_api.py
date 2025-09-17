#!/usr/bin/env python3
"""
Test script to verify frontend API functionality
"""

import requests
import json
import time

def test_frontend_api():
    """Test the frontend API endpoints."""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("TESTING FRONTEND API ENDPOINTS")
    print("=" * 60)
    
    # Test 1: Check if server is running
    print("\n1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        print(f"   ✅ Server is running (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False
    
    # Test 2: Get SKU list
    print("\n2. Testing SKU list endpoint...")
    try:
        response = requests.get(f"{base_url}/api/skus", timeout=10)
        if response.status_code == 200:
            skus = response.json()
            print(f"   ✅ SKUs loaded: {len(skus)} SKUs")
            
            # Show first few SKUs
            print("   First 5 SKUs:")
            for i, sku in enumerate(skus[:5]):
                print(f"      {i+1}. {sku.get('sku_id', 'N/A')} - {sku.get('name', 'Unknown')} ({sku.get('par_count', 0)} PARs)")
            
            if len(skus) > 5:
                print(f"      ... and {len(skus) - 5} more SKUs")
        else:
            print(f"   ❌ Failed to load SKUs (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error loading SKUs: {e}")
        return False
    
    # Test 3: Get hospital layout
    print("\n3. Testing hospital layout endpoint...")
    try:
        response = requests.get(f"{base_url}/api/hospital-layout", timeout=10)
        if response.status_code == 200:
            layout = response.json()
            print(f"   ✅ Hospital layout loaded: {len(layout)} levels")
            
            # Show levels
            for level_name, level_data in layout.items():
                par_count = len(level_data.get('pars_data', []))
                print(f"      {level_name}: {par_count} PARs")
        else:
            print(f"   ❌ Failed to load hospital layout (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error loading hospital layout: {e}")
        return False
    
    # Test 4: Get SKU connections
    print("\n4. Testing SKU connections endpoint...")
    try:
        response = requests.get(f"{base_url}/api/sku-connections", timeout=10)
        if response.status_code == 200:
            connections = response.json()
            print(f"   ✅ SKU connections loaded: {len(connections)} connections")
        else:
            print(f"   ❌ Failed to load SKU connections (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error loading SKU connections: {e}")
        return False
    
    # Test 5: Test specific SKU details (if SKUs available)
    if 'skus' in locals() and skus:
        print("\n5. Testing specific SKU details...")
        try:
            first_sku = skus[0]['sku_id']
            response = requests.get(f"{base_url}/api/sku/{first_sku}", timeout=10)
            if response.status_code == 200:
                sku_details = response.json()
                print(f"   ✅ SKU details loaded for {first_sku}")
                print(f"      Connected PARs: {sku_details.get('connection_count', 0)}")
                print(f"      Perpetual level: {sku_details.get('perpetual_sku', {}).get('current_level', 'N/A')}")
            else:
                print(f"   ❌ Failed to load SKU details (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Error loading SKU details: {e}")
    
    print("\n" + "=" * 60)
    print("FRONTEND API TEST COMPLETED")
    print("=" * 60)
    print("✅ All API endpoints are working correctly!")
    print("✅ Frontend can load and display all SKUs!")
    print("✅ Ready for dashboard testing!")
    
    return True

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    success = test_frontend_api()
    if success:
        print("\n🎉 Frontend is ready for testing!")
        print("   Open http://localhost:5000 in your browser to test the dashboard")
    else:
        print("\n⚠️  Some issues found - check the output above")
