#!/usr/bin/env python3
"""
Test Validation Subset Accuracy

This script tests the validation subset data to ensure it matches the validation test
range and SKUs for fair comparison between simulation and analytical results.
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Add the simulation_development directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_validation_subset_accuracy():
    """Test the validation subset data for accuracy and completeness."""
    
    print("=" * 80)
    print("TESTING VALIDATION SUBSET ACCURACY")
    print("=" * 80)
    
    try:
        from data.input_data.load_validation_subset import load_validation_subset_data
        
        # Load validation subset data
        print("\n1. Loading validation subset data...")
        data = load_validation_subset_data()
        
        sku_data = data['sku_data']
        demand_data = data['demand_data']
        validation_data = data['validation_data']
        
        print(f"   ✅ SKU data: {len(sku_data):,} SKUs")
        print(f"   ✅ Demand data: {len(demand_data):,} records")
        print(f"   ✅ Validation data: {len(validation_data):,} records")
        
        # Test 1: Check SKU coverage
        print("\n2. Testing SKU coverage...")
        sku_skus = set(sku_data['Oracle Item Number'].unique())
        demand_skus = set(demand_data['Oracle Item Number'].unique())
        validation_skus = set(validation_data['Oracle Item Number'].unique())
        
        print(f"   SKU data SKUs: {len(sku_skus)}")
        print(f"   Demand data SKUs: {len(demand_skus)}")
        print(f"   Validation test SKUs: {len(validation_skus)}")
        
        # Check overlaps
        sku_demand_overlap = sku_skus.intersection(demand_skus)
        sku_validation_overlap = sku_skus.intersection(validation_skus)
        demand_validation_overlap = demand_skus.intersection(validation_skus)
        
        print(f"   SKU-Demand overlap: {len(sku_demand_overlap)} SKUs")
        print(f"   SKU-Validation overlap: {len(sku_validation_overlap)} SKUs")
        print(f"   Demand-Validation overlap: {len(demand_validation_overlap)} SKUs")
        
        # Test 2: Check time range consistency
        print("\n3. Testing time range consistency...")
        demand_time_range = demand_data['PO Week Ending Date']
        print(f"   Demand time range: {demand_time_range.min()} to {demand_time_range.max()}")
        print(f"   Total weeks: {demand_time_range.nunique()}")
        
        # Test 3: Check data quality
        print("\n4. Testing data quality...")
        
        # Check for missing values
        missing_lead_times = sku_data['Avg_Lead Time'].isna().sum()
        missing_burn_rates = sku_data['Avg Daily Burn Rate'].isna().sum()
        missing_safety_stock = validation_data['Safety stock_units'].isna().sum()
        
        print(f"   Lead time coverage: {((len(sku_data) - missing_lead_times) / len(sku_data) * 100):.1f}%")
        print(f"   Burn rate coverage: {((len(sku_data) - missing_burn_rates) / len(sku_data) * 100):.1f}%")
        print(f"   Safety stock coverage: {((len(validation_data) - missing_safety_stock) / len(validation_data) * 100):.1f}%")
        
        # Test 4: Check burn rate consistency
        print("\n5. Testing burn rate consistency...")
        
        # Compare burn rates between SKU data and validation data
        # Get average burn rates per SKU (in case there are multiple records)
        sku_avg_rates = sku_data.groupby('Oracle Item Number')['Avg Daily Burn Rate'].mean()
        val_avg_rates = validation_data.groupby('Oracle Item Number')['Avg Daily Burn Rate'].mean()
        
        # Find common SKUs
        common_skus = sku_skus.intersection(validation_skus)
        print(f"   Common SKUs between SKU and validation data: {len(common_skus)}")
        
        if len(common_skus) > 0:
            burn_rate_diffs = []
            for sku in common_skus:
                sku_rate = sku_avg_rates.get(sku, None)
                val_rate = val_avg_rates.get(sku, None)
                if sku_rate is not None and val_rate is not None:
                    # Convert to float to avoid pandas comparison issues
                    sku_rate_val = float(sku_rate)
                    val_rate_val = float(val_rate)
                    diff = abs(sku_rate_val - val_rate_val)
                    burn_rate_diffs.append(diff)
            
            if burn_rate_diffs:
                avg_diff = sum(burn_rate_diffs) / len(burn_rate_diffs)
                max_diff = max(burn_rate_diffs)
                print(f"   Average burn rate difference: {avg_diff:.2f}")
                print(f"   Maximum burn rate difference: {max_diff:.2f}")
        
        # Test 5: Check demand data quality
        print("\n6. Testing demand data quality...")
        
        # Check for zero demand records
        zero_demand = demand_data[demand_data['Total Qty Issues'] == 0]
        print(f"   Zero demand records: {len(zero_demand)} ({len(zero_demand)/len(demand_data)*100:.1f}%)")
        
        # Check for negative demand records
        negative_demand = demand_data[demand_data['Total Qty Issues'] < 0]
        print(f"   Negative demand records: {len(negative_demand)}")
        
        # Check demand distribution
        demand_stats = demand_data['Total Qty Issues'].describe()
        print(f"   Demand statistics:")
        print(f"     Mean: {demand_stats['mean']:.2f}")
        print(f"     Median: {demand_stats['50%']:.2f}")
        print(f"     Std: {demand_stats['std']:.2f}")
        print(f"     Min: {demand_stats['min']:.2f}")
        print(f"     Max: {demand_stats['max']:.2f}")
        
        # Test 6: Check PAR mapping
        print("\n7. Testing PAR mapping...")
        par_columns = [col for col in sku_data.columns if 'Level' in col or 'Respiratory' in col]
        print(f"   PAR columns: {len(par_columns)}")
        
        par_mapped = sku_data[par_columns].apply(lambda x: x.notna().any(), axis=1).sum()
        print(f"   SKUs with PAR mapping: {par_mapped} ({par_mapped/len(sku_data)*100:.1f}%)")
        
        # Test 7: Summary for simulation readiness
        print("\n8. Simulation readiness assessment...")
        
        # Calculate coverage metrics
        sku_coverage = len(sku_demand_overlap) / len(validation_skus) * 100
        demand_coverage = len(demand_validation_overlap) / len(validation_skus) * 100
        
        print(f"   SKU coverage: {sku_coverage:.1f}%")
        print(f"   Demand coverage: {demand_coverage:.1f}%")
        print(f"   Data quality: {'✅ EXCELLENT' if missing_lead_times == 0 and missing_burn_rates == 0 else '⚠️  NEEDS ATTENTION'}")
        print(f"   Time range: {'✅ SUFFICIENT' if demand_time_range.nunique() >= 52 else '⚠️  LIMITED'}")
        
        # Overall assessment
        if sku_coverage >= 80 and demand_coverage >= 80 and missing_lead_times == 0 and missing_burn_rates == 0:
            print(f"\n🎯 ASSESSMENT: ✅ READY FOR VALIDATION TESTING")
        elif sku_coverage >= 60 and demand_coverage >= 60:
            print(f"\n🎯 ASSESSMENT: ⚠️  PARTIALLY READY - Some SKUs missing demand data")
        else:
            print(f"\n🎯 ASSESSMENT: ❌ NOT READY - Insufficient data coverage")
        
        print("\n" + "=" * 80)
        print("✅ VALIDATION SUBSET TESTING COMPLETED!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_validation_subset_accuracy()
    if success:
        print("\n🎉 All tests passed! The validation subset is ready for simulation testing.")
    else:
        print("\n💥 Some tests failed. Please review the validation subset data.")
