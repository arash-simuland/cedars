#!/usr/bin/env python3
"""
CedarSim Data Integration Module - Production Ready

This module integrates the production-ready input data with the AntologyGenerator
to create the simulation structure for the CedarSim hospital inventory management system.

Key Features:
- Loads production-ready data from SIMULATION_READY_SKU_INVENTORY_DATA.xlsx
- Loads demand data from SIMULATION_READY_DEMAND_DATA.csv
- Creates AntologyGenerator with real data
- Handles column name mapping between old and new formats
- Supports both validation subset and full dataset modes
"""

import pandas as pd
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from core.core_models import AntologyGenerator, ResourceFactory, Location, SKU
from .location_mapper import get_location_mapper

logger = logging.getLogger(__name__)

class DataIntegrator:
    """Integrates production-ready data with AntologyGenerator for simulation structure."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize the data integrator."""
        if data_dir is None:
            # Default to the production input data directory
            self.data_dir = Path(__file__).parent.parent / "prod-input-data"
        else:
            self.data_dir = Path(data_dir)
        
        self.antology = None
        self.sku_data = None
        self.demand_data = None
        self.validation_data = None
        self.location_mapper = get_location_mapper()
        
    def load_production_data(self) -> Dict[str, pd.DataFrame]:
        """Load the production-ready dataset from Excel and CSV files."""
        
        print("=" * 60)
        print("LOADING CEDARSIM PRODUCTION INPUT DATA")
        print("=" * 60)
        
        # Load SKU inventory data from CSV
        print("\n1. Loading SKU inventory data...")
        sku_file = self.data_dir / "SIMULATION_READY_SKU_INVENTORY_DATA.csv"
        if not sku_file.exists():
            raise FileNotFoundError(f"SKU inventory data not found: {sku_file}")
        
        self.sku_data = pd.read_csv(sku_file)
        print(f"   ✅ Loaded {len(self.sku_data):,} SKU records")
        print(f"   Columns: {list(self.sku_data.columns)}")
        print(f"   Unique SKUs: {self.sku_data['oid'].nunique():,}")
        print(f"   Unique Locations: {self.sku_data['lo'].nunique()}")
        
        # Load demand data from CSV (with uniform locations)
        print("\n2. Loading demand data...")
        demand_file = self.data_dir / "SIMULATION_READY_DEMAND_DATA_WITH_UNIFORM_LOCATIONS.csv"
        if not demand_file.exists():
            raise FileNotFoundError(f"Demand data not found: {demand_file}")
        
        self.demand_data = pd.read_csv(demand_file)
        print(f"   ✅ Loaded {len(self.demand_data):,} demand records")
        print(f"   Time range: {self.demand_data['PO Week Ending Date'].min()} to {self.demand_data['PO Week Ending Date'].max()}")
        print(f"   Unique SKUs in demand: {self.demand_data['oid'].nunique():,}")
        
        # Create validation subset from SKU data
        print("\n3. Creating validation subset...")
        self.validation_data = self._create_validation_subset()
        print(f"   ✅ Created validation subset with {len(self.validation_data):,} SKUs")
        
        # Validate location mappings
        print("\n4. Validating location mappings...")
        self._validate_location_mappings()
        
        print("\n" + "=" * 60)
        print("✅ PRODUCTION DATA LOADED SUCCESSFULLY!")
        print("=" * 60)
        
        return {
            'sku_data': self.sku_data,
            'demand_data': self.demand_data,
            'validation_data': self.validation_data
        }
    
    def _create_validation_subset(self) -> pd.DataFrame:
        """Create a validation subset from the SKU data using existing analytical safety stock."""
        # Filter SKUs that have analytical safety stock data (for validation)
        validation_data = self.sku_data[
            self.sku_data['Stock Units Analytical'].notna()
        ].copy()
        
        print(f"   Found {len(validation_data):,} SKUs with analytical safety stock data")
        
        return validation_data
    
    def _validate_location_mappings(self):
        """Validate location mappings between SKU and demand data."""
        if self.sku_data is None or self.demand_data is None:
            print("   ⚠️  Cannot validate mappings - data not loaded")
            return
        
        # Get unique locations from both datasets
        sku_locations = set(self.sku_data['lo'].dropna().astype(str).unique())
        demand_locations = set(self.demand_data['uniform_location'].dropna().astype(str).unique())
        
        # Validate mappings
        validation_results = self.location_mapper.validate_mappings(sku_locations, demand_locations)
        
        print(f"   📊 SKU Location Coverage: {validation_results['coverage_percentage']:.1f}%")
        print(f"   ✅ Mapped SKU Locations: {validation_results['mapped_sku_locations']}")
        print(f"   ✅ Mapped Demand Locations: {validation_results['mapped_demand_locations']}")
        
        if validation_results['unmapped_sku_locations']:
            print(f"   ⚠️  Unmapped SKU Locations ({len(validation_results['unmapped_sku_locations'])}):")
            for loc in validation_results['unmapped_sku_locations'][:5]:  # Show first 5
                print(f"      - {loc}")
            if len(validation_results['unmapped_sku_locations']) > 5:
                print(f"      ... and {len(validation_results['unmapped_sku_locations']) - 5} more")
        
        if validation_results['unmapped_demand_locations']:
            print(f"   ⚠️  Unmapped Demand Locations ({len(validation_results['unmapped_demand_locations'])}):")
            for loc in validation_results['unmapped_demand_locations'][:5]:  # Show first 5
                print(f"      - {loc}")
            if len(validation_results['unmapped_demand_locations']) > 5:
                print(f"      ... and {len(validation_results['unmapped_demand_locations']) - 5} more")
        
        # Print mapping summary
        print("\n   🔗 Location Mapping Summary:")
        self.location_mapper.print_mapping_summary()
    
    def create_antology_structure(self, use_validation_subset: bool = False) -> AntologyGenerator:
        """Create the complete AntologyGenerator structure with production data."""
        
        print("\n" + "=" * 60)
        print("CREATING ANTOLOGY GENERATOR STRUCTURE")
        print("=" * 60)
        
        # Initialize AntologyGenerator
        self.antology = AntologyGenerator()
        
        # Create all locations
        print("\n1. Creating locations...")
        self._create_locations()
        
        # Load data if not already loaded
        if self.sku_data is None:
            self.load_production_data()
        
        # Create SKUs
        print("\n2. Creating SKUs...")
        if use_validation_subset:
            self._create_skus_from_validation()
        else:
            self._create_skus_from_production()
        
        # Generate network connections
        print("\n3. Generating network topology...")
        self.antology.generate_network_connections()
        self.antology.finalize_network()
        
        print("\n" + "=" * 60)
        print("✅ ANTOLOGY STRUCTURE CREATED SUCCESSFULLY!")
        print("=" * 60)
        
        return self.antology
    
    def _create_locations(self):
        """Create all hospital locations using location mapping."""
        # Get unique locations from the data
        unique_locations = set()
        if self.sku_data is not None:
            # Filter out any NaN values and ensure we have strings
            valid_locations = self.sku_data['lo'].dropna().astype(str).unique()
            unique_locations = set(valid_locations)
        
        # Add standard locations
        standard_locations = [
            "Level 1 ED", "Level 2 ICU", "Level 3 Medical", "Level 4 Medical",
            "Level 5 Observation, Medical Tele & Non-Tele", "Level 6 Surgical",
            "Level 7 Surgical", "Level 8 Surgical", "Level 9 Surgical",
            "Level 10 Surgical", "Perpetual"
        ]
        
        all_locations = unique_locations.union(set(standard_locations))
        
        # Validate mappings
        print("\n🔍 Validating location mappings...")
        validation_results = self.location_mapper.validate_mappings(
            all_locations, 
            set()  # We'll validate demand locations separately
        )
        
        print(f"   📊 Location Mapping Coverage: {validation_results['coverage_percentage']:.1f}%")
        print(f"   ✅ Mapped SKU Locations: {validation_results['mapped_sku_locations']}")
        if validation_results['unmapped_sku_locations']:
            print(f"   ⚠️  Unmapped SKU Locations: {len(validation_results['unmapped_sku_locations'])}")
            for loc in validation_results['unmapped_sku_locations']:
                print(f"      - {loc}")
        
        for location_name in all_locations:
            # Ensure location_name is a string
            if not isinstance(location_name, str):
                continue
                
            # Determine location type
            if "Perpetual" in location_name:
                location_type = "PERPETUAL"
            else:
                location_type = "PAR"
            
            # Map to demand location for reference
            demand_location = self.location_mapper.map_sku_to_demand_location(location_name)
            mapping_info = f" → {demand_location}" if demand_location else " (no mapping)"
            
            location = ResourceFactory.create_location(location_name, location_type)
            self.antology.add_location(location)
            print(f"   ✅ Created {location_type}: {location_name}{mapping_info}")
    
    def _create_skus_from_production(self):
        """Create SKUs from production data."""
        print(f"   Processing {len(self.sku_data):,} SKU records...")
        
        for _, row in self.sku_data.iterrows():
            sku_id = str(row['oid']).zfill(6)  # Ensure 6-digit format
            location_id = row['lo']
            item_description = row['Item Description']
            unit_of_measure = row['unit_of_measure']
            lead_time_days = float(row['lead_time'])
            burn_rate = float(row['burn_rate'])
            
            # Use analytical safety stock if available, otherwise calculate
            analytical_safety_stock = row.get('Stock Units Analytical')
            if pd.notna(analytical_safety_stock):
                target_level = float(analytical_safety_stock)
            else:
                target_level = burn_rate * lead_time_days * 2.05  # Fallback calculation
            
            # Create SKU
            sku = ResourceFactory.create_sku(
                sku_id=sku_id,
                location_id=location_id,
                target_level=target_level,
                lead_time_days=lead_time_days,
                demand_rate=burn_rate
            )
            
            # Add additional attributes
            sku.name = item_description
            sku.unit_of_measure = unit_of_measure
            sku.analytical_safety_stock = row.get('Stock Units Analytical', None)
            
            self.antology.add_sku(sku)
            
            # Add SKU to location
            location = self.antology.locations.get(location_id)
            if location:
                location.add_sku(sku)
        
        print(f"   ✅ Created {len(self.antology.sku_registry)} SKU instances")
        print(f"   ✅ Unique SKU types: {len(set(sku.resource_id for sku_list in self.antology.sku_registry.values() for sku in sku_list))}")
    
    def _create_skus_from_validation(self):
        """Create SKUs from validation subset."""
        print(f"   Processing {len(self.validation_data):,} validation SKU records...")
        
        for _, row in self.validation_data.iterrows():
            sku_id = str(row['oid']).zfill(6)
            location_id = row['lo']
            item_description = row['Item Description']
            unit_of_measure = row['unit_of_measure']
            lead_time_days = float(row['lead_time'])
            burn_rate = float(row['burn_rate'])
            
            # Use existing analytical safety stock for validation
            analytical_safety_stock = row['Stock Units Analytical']
            if pd.notna(analytical_safety_stock):
                target_level = float(analytical_safety_stock)
            else:
                target_level = burn_rate * lead_time_days * 2.05  # Fallback calculation
            
            # Create SKU
            sku = ResourceFactory.create_sku(
                sku_id=sku_id,
                location_id=location_id,
                target_level=target_level,
                lead_time_days=lead_time_days,
                demand_rate=burn_rate
            )
            
            # Add additional attributes
            sku.name = item_description
            sku.unit_of_measure = unit_of_measure
            sku.analytical_safety_stock = row['Stock Units Analytical']
            
            self.antology.add_sku(sku)
            
            # Add SKU to location
            location = self.antology.locations.get(location_id)
            if location:
                location.add_sku(sku)
        
        print(f"   ✅ Created {len(self.antology.sku_registry)} validation SKU instances")
        print(f"   ✅ Unique SKU types: {len(set(sku.resource_id for sku_list in self.antology.sku_registry.values() for sku in sku_list))}")
    
    def get_sku_data_for_frontend(self, sku_id: str) -> Dict[str, Any]:
        """Get SKU data formatted for frontend consumption."""
        sku_instances = self.antology.sku_registry.get(sku_id, [])
        
        if not sku_instances:
            return {"error": f"SKU {sku_id} not found"}
        
        sku_data = {
            "sku_id": sku_id,
            "name": sku_instances[0].name if hasattr(sku_instances[0], 'name') else sku_id,
            "instances": []
        }
        
        for sku in sku_instances:
            location = self.antology.locations.get(sku.location_id)
            if location:
                sku_data["instances"].append({
                    "location_id": sku.location_id,
                    "location_type": location.location_type,
                    "target_level": sku.target_level,
                    "current_level": sku.current_level,
                    "lead_time_days": sku.lead_time_days,
                    "demand_rate": sku.demand_rate,
                    "is_stockout": sku.current_level <= 0,
                    "analytical_safety_stock": getattr(sku, 'analytical_safety_stock', None)
                })
        
        return sku_data

def create_integrated_antology(use_validation_subset: bool = False) -> Tuple[AntologyGenerator, DataIntegrator]:
    """Create a fully integrated AntologyGenerator with production data."""
    
    integrator = DataIntegrator()
    integrator.load_production_data()
    antology = integrator.create_antology_structure(use_validation_subset=use_validation_subset)
    
    return antology, integrator

if __name__ == "__main__":
    # Test the data integration
    print("Testing CedarSim Production Data Integration...")
    
    try:
        # Test with validation subset
        antology, integrator = create_integrated_antology(use_validation_subset=True)
        total_skus = sum(len(sku_list) for sku_list in antology.sku_registry.values())
        print(f"\n✅ SUCCESS: Created antology with {len(antology.locations)} locations and {total_skus} SKUs")
        
        # Test with full dataset
        antology_full, integrator_full = create_integrated_antology(use_validation_subset=False)
        total_skus_full = sum(len(sku_list) for sku_list in antology_full.sku_registry.values())
        print(f"✅ SUCCESS: Created full antology with {len(antology_full.locations)} locations and {total_skus_full} SKUs")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
