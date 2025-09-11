#!/usr/bin/env python3
"""
Script to find the missing SKU between our pipeline output and the FIXED file.
This will help validate the 1 SKU difference (5,941 vs 5,942 rows).
"""

import pandas as pd
import sys

def find_missing_sku():
    """Find the specific SKU that's missing from our pipeline output."""
    
    print("🔍 Finding Missing SKU Analysis")
    print("=" * 50)
    
    try:
        # Read our pipeline output
        print("📂 Reading our pipeline output...")
        our_file = pd.read_excel('CedarSim_Simulation_Ready_Data_Final.xlsx', sheet_name='01_SKU_Inventory_Final')
        our_skus = set(our_file['Oracle Item Number'].astype(str))
        print(f"   ✅ Our pipeline: {len(our_skus)} SKUs")
        
        # Read the FIXED file - column C should be Oracle Item Number
        print("📂 Reading FIXED file...")
        fixed_file = pd.read_excel('CedarSim_Simulation_Ready_Data_FIXED.xlsx', sheet_name='Data')
        # Skip the first row if it's a header, and use column C (index 2)
        fixed_skus = set(fixed_file.iloc[1:, 2].astype(str))  # Column C, skip header row
        print(f"   ✅ FIXED file: {len(fixed_skus)} SKUs")
        
        # Find the difference
        print("\n🔍 Analyzing differences...")
        missing_from_ours = fixed_skus - our_skus
        extra_in_ours = our_skus - fixed_skus
        
        print(f"   📊 SKUs in FIXED but missing from our pipeline: {len(missing_from_ours)}")
        print(f"   📊 SKUs in our pipeline but missing from FIXED: {len(extra_in_ours)}")
        
        if missing_from_ours:
            print(f"\n❌ MISSING SKUs from our pipeline:")
            for sku in sorted(missing_from_ours):
                print(f"   - {sku}")
                
            # Check if any of these were removed in Phase 1 or Phase 2
            print(f"\n🔍 Checking removal records...")
            
            # Read Phase 1 removal records
            try:
                phase1_removed = pd.read_csv('phase1_missing_lead_times_removal.csv')
                phase1_skus = set(phase1_removed['Oracle Item Number'].astype(str))
                print(f"   📋 Phase 1 removed: {len(phase1_skus)} SKUs")
                
                # Check if missing SKUs were in Phase 1 removal
                phase1_matches = missing_from_ours.intersection(phase1_skus)
                if phase1_matches:
                    print(f"   ⚠️  Missing SKUs that were removed in Phase 1: {phase1_matches}")
                    for sku in phase1_matches:
                        sku_info = phase1_removed[phase1_removed['Oracle Item Number'].astype(str) == sku]
                        if not sku_info.empty:
                            print(f"      - {sku}: {sku_info.iloc[0]['Item Description']} (Missing Lead Time)")
                
            except Exception as e:
                print(f"   ❌ Error reading Phase 1 file: {e}")
            
            # Read Phase 2 removal records
            try:
                phase2_removed = pd.read_csv('phase2_unmapped_skus_removal.csv')
                phase2_skus = set(phase2_removed['Oracle Item Number'].astype(str))
                print(f"   📋 Phase 2 removed: {len(phase2_skus)} SKUs")
                
                # Check if missing SKUs were in Phase 2 removal
                phase2_matches = missing_from_ours.intersection(phase2_skus)
                if phase2_matches:
                    print(f"   ⚠️  Missing SKUs that were removed in Phase 2: {phase2_matches}")
                    for sku in phase2_matches:
                        sku_info = phase2_removed[phase2_removed['Oracle Item Number'].astype(str) == sku]
                        if not sku_info.empty:
                            print(f"      - {sku}: {sku_info.iloc[0]['Item Description']} (No PAR Mapping)")
                
            except Exception as e:
                print(f"   ❌ Error reading Phase 2 file: {e}")
        
        if extra_in_ours:
            print(f"\n➕ EXTRA SKUs in our pipeline:")
            for sku in sorted(extra_in_ours):
                print(f"   + {sku}")
        
        # Summary
        print(f"\n📊 SUMMARY:")
        print(f"   Our pipeline: {len(our_skus)} SKUs")
        print(f"   FIXED file:   {len(fixed_skus)} SKUs")
        print(f"   Difference:   {len(fixed_skus) - len(our_skus)} SKUs")
        
        if len(missing_from_ours) == 1 and len(extra_in_ours) == 0:
            print(f"\n✅ CONFIRMED: Exactly 1 SKU missing from our pipeline")
            missing_sku = list(missing_from_ours)[0]
            print(f"   Missing SKU: {missing_sku}")
            
            # Check if this SKU was correctly removed
            was_removed_phase1 = missing_sku in phase1_skus if 'phase1_skus' in locals() else False
            was_removed_phase2 = missing_sku in phase2_skus if 'phase2_skus' in locals() else False
            
            if was_removed_phase1:
                print(f"   ✅ VALIDATION: SKU {missing_sku} was correctly removed in Phase 1 (Missing Lead Time)")
            elif was_removed_phase2:
                print(f"   ✅ VALIDATION: SKU {missing_sku} was correctly removed in Phase 2 (No PAR Mapping)")
            else:
                print(f"   ❌ WARNING: SKU {missing_sku} was NOT found in removal records - needs investigation!")
        
        return missing_from_ours, extra_in_ours
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return set(), set()

if __name__ == "__main__":
    missing, extra = find_missing_sku()