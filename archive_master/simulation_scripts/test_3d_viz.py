#!/usr/bin/env python3
"""
Test script for CedarSim 3D Visualization Pipeline
==================================================

This script tests the 3D visualization pipeline with a small sample of data
to ensure everything works correctly before running on the full dataset.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

import importlib.util
spec = importlib.util.spec_from_file_location("viz_pipeline", "cedarsim_3d_viz.py")
viz_pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(viz_pipeline)
CedarSim3DVisualizer = viz_pipeline.CedarSim3DVisualizer

def create_test_data():
    """Create a small test dataset for visualization testing"""
    print("Creating test data...")
    
    # Create test SKU data
    test_skus = []
    for i in range(50):  # Small sample for testing
        sku_data = {
            'Oracle Item Number': f'TEST_SKU_{i:03d}',
            'Item Description': f'Test Item {i}',
            'Avg_Lead Time': np.random.uniform(0.5, 5.0),
            'Avg Daily Burn Rate': np.random.uniform(0.1, 10.0),
            'Perpetual': np.random.choice([1, np.nan], p=[0.3, 0.7]),
            'Level 1 ED': np.random.choice([1, np.nan], p=[0.4, 0.6]),
            'Level 1 Imaging': np.random.choice([1, np.nan], p=[0.2, 0.8]),
            'Level 2 Surgery/Procedures/PACU': np.random.choice([1, np.nan], p=[0.5, 0.5]),
            'Level 3 Central Lab': np.random.choice([1, np.nan], p=[0.3, 0.7]),
            'Level 7 ICU': np.random.choice([1, np.nan], p=[0.4, 0.6]),
            'Respiratory Therapy': np.random.choice([1, np.nan], p=[0.2, 0.8])
        }
        test_skus.append(sku_data)
    
    test_sku_df = pd.DataFrame(test_skus)
    
    # Create test demand data
    test_demand = []
    for i in range(100):  # Small sample
        demand_data = {
            'Oracle Item Number': f'TEST_SKU_{np.random.randint(0, 50):03d}',
            'Date': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 365)),
            'Total Qty Issues': np.random.randint(1, 20)
        }
        test_demand.append(demand_data)
    
    test_demand_df = pd.DataFrame(test_demand)
    
    # Create test validation data
    test_validation = test_sku_df.head(10).copy()
    
    return test_sku_df, test_demand_df, test_validation

def test_visualization_pipeline():
    """Test the 3D visualization pipeline with test data"""
    print("Testing CedarSim 3D Visualization Pipeline")
    print("=" * 50)
    
    try:
        # Create test data
        test_sku_df, test_demand_df, test_validation_df = create_test_data()
        
        # Create test Excel file
        test_file = Path("test_data.xlsx")
        with pd.ExcelWriter(test_file, engine='openpyxl') as writer:
            test_sku_df.to_excel(writer, sheet_name='01_SKU_Inventory_Final', index=False)
            test_demand_df.to_excel(writer, sheet_name='02_Demand_Data_Clean', index=False)
            test_validation_df.to_excel(writer, sheet_name='03_Validation_Sample', index=False)
        
        print(f"Test data created: {test_file}")
        print(f"  - SKUs: {len(test_sku_df)}")
        print(f"  - Demand records: {len(test_demand_df)}")
        print(f"  - Validation SKUs: {len(test_validation_df)}")
        
        # Initialize visualizer with test data
        visualizer = CedarSim3DVisualizer(data_file=str(test_file))
        
        # Test data loading
        print("\nTesting data loading...")
        if visualizer.load_data():
            print("✅ Data loading successful")
        else:
            print("❌ Data loading failed")
            return False
        
        # Test location position calculation
        print("\nTesting location position calculation...")
        locations = visualizer.calculate_location_positions()
        print(f"✅ Calculated positions for {len(locations)} locations")
        
        # Test connection calculation
        print("\nTesting connection calculation...")
        connections = visualizer.calculate_connections()
        print(f"✅ Calculated {len(connections)} connections")
        
        # Test 3D visualization creation
        print("\nTesting 3D visualization creation...")
        if visualizer.create_3d_visualization("test_3d_viz.html"):
            print("✅ 3D visualization created successfully")
        else:
            print("❌ 3D visualization creation failed")
            return False
        
        # Test network visualization creation
        print("\nTesting network visualization creation...")
        if visualizer.create_network_visualization("test_network.html"):
            print("✅ Network visualization created successfully")
        else:
            print("❌ Network visualization creation failed")
            return False
        
        # Test report generation
        print("\nTesting report generation...")
        report = visualizer.generate_visualization_report()
        with open("test_report.md", 'w') as f:
            f.write(report)
        print("✅ Report generated successfully")
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("Generated test files:")
        print("  - test_3d_viz.html (3D visualization)")
        print("  - test_network.html (Network graph)")
        print("  - test_report.md (Summary report)")
        print("  - test_data.xlsx (Test data)")
        
        # Clean up test files
        test_file.unlink()
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_visualization_pipeline()
    sys.exit(0 if success else 1)
