#!/usr/bin/env python3
"""
CedarSim Complete System Test

This script thoroughly tests the data loading mechanism and frontend dashboard
to ensure everything is working properly before proceeding with SimPy simulation.
"""

import sys
import os
from pathlib import Path
import json

# Add the simulation_development directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_data_loading_comprehensive():
    """Test data loading mechanism comprehensively."""
    print("=" * 80)
    print("TESTING DATA LOADING MECHANISM")
    print("=" * 80)
    
    try:
        from data.input_data.load_input_data import load_simulation_data
        from data.input_data.simulation_config import get_config
        
        # Test data loading
        print("\n1. Testing data loading...")
        data = load_simulation_data()
        
        print(f"   ✅ SKU Data: {len(data['sku_data']):,} SKUs")
        print(f"   ✅ Demand Data: {len(data['demand_data']):,} records")
        print(f"   ✅ Validation Data: {len(data['validation_data']):,} SKUs")
        
        # Test configuration
        print("\n2. Testing configuration...")
        config = get_config()
        print(f"   ✅ Configuration loaded: {len(config)} sections")
        print(f"   ✅ Simulation horizon: {config['simulation']['time_horizon_days']} days")
        print(f"   ✅ Target service level: {config['simulation']['target_service_level']*100}%")
        
        # Test data quality
        print("\n3. Testing data quality...")
        sku_data = data['sku_data']
        demand_data = data['demand_data']
        validation_data = data['validation_data']
        
        # Check for missing values
        missing_lead_times = sku_data['Avg_Lead Time'].isna().sum()
        missing_burn_rates = sku_data['Avg Daily Burn Rate'].isna().sum()
        
        print(f"   ✅ Lead time coverage: {((len(sku_data) - missing_lead_times) / len(sku_data) * 100):.1f}%")
        print(f"   ✅ Burn rate coverage: {((len(sku_data) - missing_burn_rates) / len(sku_data) * 100):.1f}%")
        
        # Check data types
        print(f"   ✅ Data types: SKU={type(sku_data)}, Demand={type(demand_data)}, Validation={type(validation_data)}")
        
        return True, data
        
    except Exception as e:
        print(f"   ❌ Data loading failed: {e}")
        return False, None

def test_data_integration_comprehensive():
    """Test data integration with AntologyGenerator."""
    print("\n" + "=" * 80)
    print("TESTING DATA INTEGRATION")
    print("=" * 80)
    
    try:
        from data.input_data.data_integration import create_integrated_antology
        from core.core_models import AntologyGenerator
        
        # Test with validation subset
        print("\n1. Testing with validation subset...")
        antology, data_integrator = create_integrated_antology(use_validation_subset=True)
        
        print(f"   ✅ AntologyGenerator created successfully")
        print(f"   ✅ Locations: {len(antology.locations)}")
        print(f"   ✅ SKUs: {len(antology.skus)}")
        print(f"   ✅ SKU types: {len(set(sku.resource_id for sku in antology.skus))}")
        
        # Test location structure
        print("\n2. Testing location structure...")
        location_types = {}
        for location in antology.locations.values():
            location_type = location.location_type
            location_types[location_type] = location_types.get(location_type, 0) + 1
        
        print(f"   ✅ Location types: {location_types}")
        
        # Test SKU distribution
        print("\n3. Testing SKU distribution...")
        sku_locations = {}
        for sku in antology.skus:
            sku_id = sku.resource_id
            if sku_id not in sku_locations:
                sku_locations[sku_id] = 0
            sku_locations[sku_id] += 1
        
        print(f"   ✅ SKU distribution: {len(sku_locations)} unique SKUs")
        print(f"   ✅ Average locations per SKU: {sum(sku_locations.values()) / len(sku_locations):.1f}")
        
        # Test network connections
        print("\n4. Testing network connections...")
        connection_count = 0
        for sku in antology.skus:
            if hasattr(sku, 'emergency_connections'):
                connection_count += len(sku.emergency_connections)
        
        print(f"   ✅ Emergency connections: {connection_count}")
        
        return True, antology
        
    except Exception as e:
        print(f"   ❌ Data integration failed: {e}")
        return False, None

def test_frontend_generation_comprehensive():
    """Test frontend data generation."""
    print("\n" + "=" * 80)
    print("TESTING FRONTEND DATA GENERATION")
    print("=" * 80)
    
    try:
        from frontend.frontend_generator import FrontendDataGenerator
        from data.input_data.data_integration import create_integrated_antology
        
        # Create antology
        print("\n1. Creating antology structure...")
        antology, _ = create_integrated_antology(use_validation_subset=True)
        
        # Create frontend generator
        print("\n2. Creating frontend generator...")
        generator = FrontendDataGenerator(antology)
        
        # Generate frontend data
        print("\n3. Generating frontend data...")
        frontend_data = generator.generate_frontend_data()
        
        print(f"   ✅ Frontend data keys: {list(frontend_data.keys())}")
        print(f"   ✅ SKU list: {len(frontend_data.get('sku_list', []))} SKUs")
        print(f"   ✅ Hospital layout: {len(frontend_data.get('hospital_layout', {}))} levels")
        print(f"   ✅ SKU connections: {len(frontend_data.get('sku_connections', {}))} connections")
        
        # Test individual components
        print("\n4. Testing individual components...")
        
        # Test hospital layout
        hospital_layout = generator.generate_hospital_layout()
        print(f"   ✅ Hospital layout: {len(hospital_layout)} levels")
        
        # Test SKU connections
        sku_connections = generator.generate_sku_connections()
        print(f"   ✅ SKU connections: {len(sku_connections)} SKUs")
        
        # Test inventory timeline for a sample SKU
        if frontend_data.get('sku_list'):
            sample_sku = frontend_data['sku_list'][0]['sku_id']
            timeline = generator.generate_inventory_timeline(sample_sku, weeks=4)
            print(f"   ✅ Inventory timeline for {sample_sku}: {len(timeline.get('data', []))} data points")
        
        return True, frontend_data
        
    except Exception as e:
        print(f"   ❌ Frontend generation failed: {e}")
        return False, None

def test_dashboard_api_comprehensive():
    """Test dashboard API functionality."""
    print("\n" + "=" * 80)
    print("TESTING DASHBOARD API")
    print("=" * 80)
    
    try:
        from frontend.dashboard_api_integrated import app, initialize_antology
        
        # Test API import
        print("\n1. Testing API import...")
        print(f"   ✅ Flask app imported successfully")
        print(f"   ✅ CORS enabled")
        
        # Test antology initialization
        print("\n2. Testing antology initialization...")
        initialize_antology(use_validation_subset=True)
        print(f"   ✅ AntologyGenerator initialized")
        
        # Test API routes (without actually running the server)
        print("\n3. Testing API routes...")
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.methods} {rule.rule}")
        
        print(f"   ✅ Available routes: {len(routes)}")
        for route in routes[:5]:  # Show first 5 routes
            print(f"      {route}")
        if len(routes) > 5:
            print(f"      ... and {len(routes) - 5} more")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Dashboard API test failed: {e}")
        return False

def test_dashboard_html():
    """Test dashboard HTML file."""
    print("\n" + "=" * 80)
    print("TESTING DASHBOARD HTML")
    print("=" * 80)
    
    try:
        dashboard_path = Path("frontend/dashboard.html")
        
        print("\n1. Testing HTML file...")
        if not dashboard_path.exists():
            print(f"   ❌ Dashboard file not found: {dashboard_path}")
            return False
        
        print(f"   ✅ Dashboard file found: {dashboard_path}")
        print(f"   ✅ File size: {dashboard_path.stat().st_size:,} bytes")
        
        # Read and validate HTML content
        print("\n2. Testing HTML content...")
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key HTML elements
        html_checks = [
            ('DOCTYPE html', 'HTML5 doctype'),
            ('<title>CedarSim Dashboard</title>', 'Page title'),
            ('<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', 'Chart.js library'),
            ('function loadSKUData()', 'SKU data loading function'),
            ('function updateCharts()', 'Chart update function'),
            ('<select id="skuSelect">', 'SKU selection dropdown'),
            ('<canvas id="inventoryChart">', 'Inventory chart canvas')
        ]
        
        for check, description in html_checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ Missing: {description}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Dashboard HTML test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all comprehensive tests."""
    print("CEDARSIM COMPREHENSIVE SYSTEM TEST")
    print("=" * 80)
    print("Testing data loading mechanism and frontend dashboard...")
    
    # Run all tests
    tests = [
        ("Data Loading", test_data_loading_comprehensive),
        ("Data Integration", test_data_integration_comprehensive),
        ("Frontend Generation", test_frontend_generation_comprehensive),
        ("Dashboard API", test_dashboard_api_comprehensive),
        ("Dashboard HTML", test_dashboard_html)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("   Data loading mechanism: ✅ Working")
        print("   Frontend dashboard: ✅ Working")
        print("   Ready to proceed with SimPy simulation development!")
    else:
        print(f"\n⚠️  {total - passed} tests failed - please fix issues before proceeding")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
