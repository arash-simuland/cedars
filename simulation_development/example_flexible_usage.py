#!/usr/bin/env python3
"""
CedarSim Flexible Data Loading Example

This script demonstrates how to use the flexible data loading system
for different simulation scenarios.
"""

import sys
from pathlib import Path

# Add the simulation_development directory to Python path
sys.path.append(str(Path(__file__).parent))

from data.input_data.load_simulation_data_flexible import load_simulation_data, get_data_summary

def demonstrate_validation_subset():
    """Demonstrate validation subset mode for testing."""
    
    print("=" * 80)
    print("VALIDATION SUBSET MODE - Testing against analytical solution")
    print("=" * 80)
    
    # Load validation subset data
    data = load_simulation_data('validation_subset')
    
    print(f"\n📊 Data Summary:")
    print(f"   SKU Inventory: {len(data['sku_data']):,} SKUs")
    print(f"   Demand Records: {len(data['demand_data']):,} records")
    print(f"   Validation Test: {len(data['validation_data']):,} records")
    
    # Show sample data
    print(f"\n📋 Sample SKU Data:")
    print(data['sku_data'][['Oracle Item Number', 'Item Description', 'Avg Daily Burn Rate', 'Avg_Lead Time']].head())
    
    print(f"\n📋 Sample Validation Data (Analytical Solution):")
    print(data['validation_data'][['Oracle Item Number', 'Avg Daily Burn Rate', 'Safety stock_units']].head())
    
    print(f"\n🎯 Use Case: Compare your simulation results against the analytical solution")
    print(f"   - Run your simulation with this data")
    print(f"   - Compare safety stock levels with validation_data['Safety stock_units']")
    print(f"   - Validate accuracy before scaling up")
    
    return data

def demonstrate_full_time_range():
    """Demonstrate full time range mode for production simulation."""
    
    print("\n" + "=" * 80)
    print("FULL TIME RANGE MODE - Production simulation with all SKUs")
    print("=" * 80)
    
    # Load full time range data
    data = load_simulation_data('full_time_range')
    
    print(f"\n📊 Data Summary:")
    print(f"   SKU Inventory: {len(data['sku_data']):,} SKUs")
    print(f"   Demand Records: {len(data['demand_data']):,} records")
    print(f"   Validation Test: {len(data['validation_data']):,} records")
    
    # Show time range
    time_range = data['demand_data']['PO Week Ending Date']
    print(f"   Time Range: {time_range.min()} to {time_range.max()}")
    
    # Show SKU coverage
    sku_skus = set(data['sku_data']['Oracle Item Number'].unique())
    demand_skus = set(data['demand_data']['Oracle Item Number'].unique())
    print(f"   SKUs with demand data: {len(sku_skus.intersection(demand_skus)):,}")
    
    print(f"\n🌍 Use Case: Full production simulation with consistent time range")
    print(f"   - Run simulation with all 5,941 SKUs")
    print(f"   - Same time range as validation test for consistency")
    print(f"   - Scale up from validation testing")
    
    return data

def demonstrate_complete_mode():
    """Demonstrate complete mode for maximum historical coverage."""
    
    print("\n" + "=" * 80)
    print("COMPLETE MODE - Maximum historical coverage")
    print("=" * 80)
    
    # Load complete data
    data = load_simulation_data('complete')
    
    print(f"\n📊 Data Summary:")
    print(f"   SKU Inventory: {len(data['sku_data']):,} SKUs")
    print(f"   Demand Records: {len(data['demand_data']):,} records")
    print(f"   Validation Test: {len(data['validation_data']):,} records")
    
    # Show time range
    time_range = data['demand_data']['PO Week Ending Date']
    print(f"   Time Range: {time_range.min()} to {time_range.max()}")
    
    print(f"\n🚀 Use Case: Maximum historical coverage")
    print(f"   - Full historical time range (2019-2025)")
    print(f"   - All 5,941 SKUs")
    print(f"   - Maximum data for analysis")
    
    return data

def compare_modes():
    """Compare all three modes side by side."""
    
    print("\n" + "=" * 80)
    print("MODE COMPARISON")
    print("=" * 80)
    
    modes = ['validation_subset', 'full_time_range', 'complete']
    
    for mode in modes:
        print(f"\n{mode.upper()}:")
        try:
            data = get_data_summary(mode)
            print(f"   ✅ {data['description']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Main demonstration function."""
    
    print("🎯 CEDARSIM FLEXIBLE DATA LOADING DEMONSTRATION")
    print("=" * 80)
    
    try:
        # Demonstrate validation subset mode
        validation_data = demonstrate_validation_subset()
        
        # Demonstrate full time range mode
        full_data = demonstrate_full_time_range()
        
        # Demonstrate complete mode
        complete_data = demonstrate_complete_mode()
        
        # Compare all modes
        compare_modes()
        
        print("\n" + "=" * 80)
        print("✅ DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        print(f"\n🎯 RECOMMENDED WORKFLOW:")
        print(f"   1. Start with validation_subset mode for testing")
        print(f"   2. Scale to full_time_range mode for production")
        print(f"   3. Use complete mode only if you need full historical range")
        
        print(f"\n📝 USAGE:")
        print(f"   from data.input_data.load_simulation_data_flexible import load_simulation_data")
        print(f"   data = load_simulation_data('validation_subset')  # or 'full_time_range' or 'complete'")
        
    except Exception as e:
        print(f"\n❌ DEMONSTRATION FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
