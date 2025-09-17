#!/usr/bin/env python3
"""
CedarSim Data Integration Module

This module integrates the complete CSV dataset with the AntologyGenerator
to create the full simulation structure for the dashboard interface.

Key Features:
- Loads complete 5,941 SKU dataset
- Creates AntologyGenerator with real data
- Populates all locations and SKUs
- Generates network topology
- Prepares data for frontend visualization
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

logger = logging.getLogger(__name__)

class DataIntegrator:
    """Integrates CSV data with AntologyGenerator for simulation structure."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize the data integrator."""
        if data_dir is None:
            # Default to the simulation development data directory
            self.data_dir = Path(__file__).parent
        else:
            self.data_dir = Path(data_dir)
        
        self.antology = None
        self.sku_data = None
        self.demand_data = None
        self.validation_data = None
        
    def load_complete_dataset(self) -> Dict[str, pd.DataFrame]:
        """Load the complete dataset from CSV files."""
        
        print("=" * 60)
        print("LOADING COMPLETE CEDARSIM DATASET")
        print("=" * 60)
        
        # Load SKU inventory data
        print("\n1. Loading SKU inventory data...")
        sku_file = self.data_dir / "sku_inventory_data.csv"
        if not sku_file.exists():
            raise FileNotFoundError(f"SKU inventory data not found: {sku_file}")
        
        self.sku_data = pd.read_csv(sku_file)
        print(f"   ✅ Loaded {len(self.sku_data):,} SKUs")
        print(f"   Columns: {len(self.sku_data.columns)}")
        
        # Load demand data
        print("\n2. Loading demand data...")
        demand_file = self.data_dir / "historical_demand_data.csv"
        if not demand_file.exists():
            raise FileNotFoundError(f"Demand data not found: {demand_file}")
        
        self.demand_data = pd.read_csv(demand_file)
        print(f"   ✅ Loaded {len(self.demand_data):,} demand records")
        
        # Load validation subset
        print("\n3. Loading validation subset...")
        validation_file = self.data_dir / "validation_subset_data.csv"
        if not validation_file.exists():
            raise FileNotFoundError(f"Validation data not found: {validation_file}")
        
        self.validation_data = pd.read_csv(validation_file)
        print(f"   ✅ Loaded {len(self.validation_data):,} validation SKUs")
        
        print("\n" + "=" * 60)
        print("✅ COMPLETE DATASET LOADED SUCCESSFULLY!")
        print("=" * 60)
        
        return {
            'sku_data': self.sku_data,
            'demand_data': self.demand_data,
            'validation_data': self.validation_data
        }
    
    def create_antology_structure(self, use_validation_subset: bool = False) -> AntologyGenerator:
        """Create the complete AntologyGenerator structure with real data."""
        
        print("\n" + "=" * 60)
        print("CREATING ANTOLOGY GENERATOR STRUCTURE")
        print("=" * 60)
        
        # Initialize AntologyGenerator
        self.antology = AntologyGenerator()
        
        # Create all locations (18 PARs + 1 Perpetual)
        print("\n1. Creating locations...")
        self._create_locations()
        
        # Load SKU data
        if not self.sku_data is not None:
            self.load_complete_dataset()
        
        # Create SKUs
        print("\n2. Creating SKUs...")
        if use_validation_subset:
            self._create_skus_from_validation()
        else:
            self._create_skus_from_complete()
        
        # Generate network connections
        print("\n3. Generating network topology...")
        self.antology.generate_network_connections()
        self.antology.finalize_network()
        
        print("\n" + "=" * 60)
        print("✅ ANTOLOGY STRUCTURE CREATED SUCCESSFULLY!")
        print("=" * 60)
        
        return self.antology
    
    def _create_locations(self):
        """Create all hospital locations."""
        
        # Define all PAR locations based on the data
        par_locations = [
            "ED", "Surgery", "ICU", "Pharmacy", "Central_Lab", "Respiratory_Therapy",
            "Observation", "Medical_Tele", "Non_Tele", "M_S_Overflow", "PCU", "Telemetry",
            "Imaging", "EVS", "Facilities", "Sterile_Processing", "Food_Service", "PACU"
        ]
        
        # Create Perpetual location
        perpetual = ResourceFactory.create_location("PERPETUAL", "Perpetual")
        self.antology.add_location(perpetual)
        print(f"   ✅ Created PERPETUAL location")
        
        # Create PAR locations
        for par_id in par_locations:
            location = ResourceFactory.create_location(par_id, "PAR")
            self.antology.add_location(location)
        
        print(f"   ✅ Created {len(par_locations)} PAR locations")
        print(f"   ✅ Total locations: {len(self.antology.locations)}")
    
    def _create_skus_from_complete(self):
        """Create SKUs from the complete dataset."""
        
        print(f"   Processing {len(self.sku_data):,} SKUs from complete dataset...")
        
        sku_count = 0
        for _, row in self.sku_data.iterrows():
            try:
                # Extract SKU information
                sku_id = str(row['Oracle Item Number'])
                item_description = str(row['Item Description'])
                burn_rate = float(row['Avg Daily Burn Rate']) if pd.notna(row['Avg Daily Burn Rate']) else 0.0
                lead_time_days = float(row['Avg_Lead Time']) if pd.notna(row['Avg_Lead Time']) else 0.0
                
                # Determine which PARs this SKU should be in
                par_locations = self._get_sku_par_locations(row)
                
                # Create SKU in Perpetual location first
                perpetual_sku = ResourceFactory.create_sku(
                    sku_id, "PERPETUAL",
                    target_level=burn_rate * lead_time_days * 2,  # 2x safety factor
                    lead_time_days=lead_time_days,
                    demand_rate=0.0  # Perpetual doesn't consume
                )
                perpetual_sku.name = item_description
                self.antology.add_sku(perpetual_sku)
                
                # Add to Perpetual location
                perpetual_location = self.antology.locations.get("PERPETUAL")
                if perpetual_location:
                    perpetual_location.add_sku(perpetual_sku)
                
                # Create SKU in each PAR location
                for par_id in par_locations:
                    par_sku = ResourceFactory.create_sku(
                        sku_id, par_id,
                        target_level=burn_rate * lead_time_days,  # Standard safety stock
                        lead_time_days=lead_time_days,
                        demand_rate=burn_rate
                    )
                    par_sku.name = item_description
                    self.antology.add_sku(par_sku)
                    
                    # Add to PAR location
                    par_location = self.antology.locations.get(par_id)
                    if par_location:
                        par_location.add_sku(par_sku)
                
                sku_count += 1
                
                if sku_count % 1000 == 0:
                    print(f"   Processed {sku_count:,} SKUs...")
                    
            except Exception as e:
                logger.warning(f"Failed to process SKU {row.get('Oracle Item Number', 'Unknown')}: {e}")
                continue
        
        print(f"   ✅ Created {sku_count:,} SKUs across all locations")
    
    def _create_skus_from_validation(self):
        """Create SKUs from the validation subset."""
        
        print(f"   Processing {len(self.validation_data):,} SKUs from validation subset...")
        
        sku_count = 0
        for _, row in self.validation_data.iterrows():
            try:
                # Extract SKU information
                sku_id = str(row['Oracle Item Number'])
                item_description = str(row['Item Description'])
                burn_rate = float(row['Avg Daily Burn Rate']) if pd.notna(row['Avg Daily Burn Rate']) else 0.0
                lead_time_days = float(row['Avg_Lead Time']) if pd.notna(row['Avg_Lead Time']) else 0.0
                
                # Determine which PARs this SKU should be in
                par_locations = self._get_sku_par_locations(row)
                
                # Create SKU in Perpetual location first
                perpetual_sku = ResourceFactory.create_sku(
                    sku_id, "PERPETUAL",
                    target_level=burn_rate * lead_time_days * 2,  # 2x safety factor
                    lead_time_days=lead_time_days,
                    demand_rate=0.0  # Perpetual doesn't consume
                )
                perpetual_sku.name = item_description
                self.antology.add_sku(perpetual_sku)
                
                # Add to Perpetual location
                perpetual_location = self.antology.locations.get("PERPETUAL")
                if perpetual_location:
                    perpetual_location.add_sku(perpetual_sku)
                
                # Create SKU in each PAR location
                for par_id in par_locations:
                    par_sku = ResourceFactory.create_sku(
                        sku_id, par_id,
                        target_level=burn_rate * lead_time_days,  # Standard safety stock
                        lead_time_days=lead_time_days,
                        demand_rate=burn_rate
                    )
                    par_sku.name = item_description
                    self.antology.add_sku(par_sku)
                    
                    # Add to PAR location
                    par_location = self.antology.locations.get(par_id)
                    if par_location:
                        par_location.add_sku(par_sku)
                
                sku_count += 1
                    
            except Exception as e:
                logger.warning(f"Failed to process validation SKU {row.get('Oracle Item Number', 'Unknown')}: {e}")
                continue
        
        print(f"   ✅ Created {sku_count:,} SKUs across all locations")
    
    def _get_sku_par_locations(self, row: pd.Series) -> List[str]:
        """Determine which PAR locations a SKU should be in based on the data."""
        
        par_locations = []
        
        # Check each PAR column to see if the SKU is mapped to it
        par_columns = [col for col in row.index if any(par in col for par in [
            'ED', 'Surgery', 'ICU', 'Pharmacy', 'Central_Lab', 'Respiratory_Therapy',
            'Observation', 'Medical_Tele', 'Non_Tele', 'M_S_Overflow', 'PCU', 'Telemetry',
            'Imaging', 'EVS', 'Facilities', 'Sterile_Processing', 'Food_Service', 'PACU'
        ])]
        
        for col in par_columns:
            if pd.notna(row[col]) and str(row[col]).strip() != '':
                # Extract PAR name from column name
                par_name = col.replace('Level_', '').replace('_', '_')
                if par_name in ['ED', 'Surgery', 'ICU', 'Pharmacy', 'Central_Lab', 'Respiratory_Therapy',
                               'Observation', 'Medical_Tele', 'Non_Tele', 'M_S_Overflow', 'PCU', 'Telemetry',
                               'Imaging', 'EVS', 'Facilities', 'Sterile_Processing', 'Food_Service', 'PACU']:
                    par_locations.append(par_name)
        
        # If no specific PARs found, default to common locations
        if not par_locations:
            par_locations = ['ED', 'Surgery', 'ICU']
        
        return par_locations
    
    def get_sku_list_for_frontend(self) -> List[Dict[str, Any]]:
        """Get a list of SKUs formatted for the frontend dropdown."""
        
        if not self.antology:
            raise ValueError("AntologyGenerator not initialized. Call create_antology_structure() first.")
        
        sku_list = []
        seen_skus = set()
        
        # Get unique SKUs from the SKU registry
        for sku_id, sku_list_for_id in self.antology.sku_registry.items():
            if sku_id not in seen_skus and sku_list_for_id:
                # Get the first SKU instance for this ID to get basic info
                sku = sku_list_for_id[0]
                sku_list.append({
                    'sku_id': sku.resource_id,
                    'name': getattr(sku, 'name', sku.resource_id),
                    'description': getattr(sku, 'name', sku.resource_id),
                    'burn_rate': sku.demand_rate,
                    'lead_time_days': sku.lead_time_days
                })
                seen_skus.add(sku_id)
        
        # Sort by SKU ID for consistent ordering
        sku_list.sort(key=lambda x: x['sku_id'])
        
        return sku_list
    
    def get_sku_data_for_frontend(self, sku_id: str) -> Dict[str, Any]:
        """Get detailed data for a specific SKU for frontend visualization."""
        
        if not self.antology:
            raise ValueError("AntologyGenerator not initialized. Call create_antology_structure() first.")
        
        sku_data = {
            'sku_id': sku_id,
            'locations': {},
            'network_connections': [],
            'summary': {}
        }
        
        # Find the SKU in all locations
        if sku_id in self.antology.sku_registry:
            for sku in self.antology.sku_registry[sku_id]:
                location_id = sku.location_id
                location = self.antology.locations.get(location_id)
                if location:
                    current_inventory = sku.get_current_level()
                    sku_data['locations'][location_id] = {
                        'location_id': location_id,
                        'location_type': location.location_type,
                        'current_inventory': current_inventory,
                        'target_level': sku.target_level,
                        'demand_rate': sku.demand_rate,
                        'lead_time_days': sku.lead_time_days,
                        'is_stockout': current_inventory <= 0,
                        'is_understocked': current_inventory < sku.target_level * 0.5
                    }
        
        # Get network connections for this SKU (if available)
        if hasattr(self.antology, 'sku_connections') and sku_id in self.antology.sku_connections:
            sku_data['network_connections'] = self.antology.sku_connections[sku_id]
        else:
            sku_data['network_connections'] = []
        
        # Calculate summary statistics
        locations = list(sku_data['locations'].values())
        if locations:
            sku_data['summary'] = {
                'total_locations': len(locations),
                'total_inventory': sum(loc['current_inventory'] for loc in locations),
                'stockout_locations': sum(1 for loc in locations if loc['is_stockout']),
                'understocked_locations': sum(1 for loc in locations if loc['is_understocked']),
                'avg_demand_rate': sum(loc['demand_rate'] for loc in locations) / len(locations) if locations else 0
            }
        
        return sku_data

def create_integrated_antology(use_validation_subset: bool = False) -> Tuple[AntologyGenerator, DataIntegrator]:
    """Create a fully integrated AntologyGenerator with real data."""
    
    integrator = DataIntegrator()
    integrator.load_complete_dataset()
    antology = integrator.create_antology_structure(use_validation_subset=use_validation_subset)
    
    return antology, integrator

if __name__ == "__main__":
    # Test the data integration
    print("Testing CedarSim Data Integration...")
    
    # Test with validation subset first
    print("\n1. Testing with validation subset...")
    antology, integrator = create_integrated_antology(use_validation_subset=True)
    
    print(f"\nAntologyGenerator created with:")
    print(f"   - Locations: {len(antology.locations)}")
    print(f"   - SKUs: {len(antology.sku_registry)}")
    print(f"   - SKU types: {len(antology.sku_registry)} unique SKU IDs")
    
    # Test SKU list generation
    sku_list = integrator.get_sku_list_for_frontend()
    print(f"\nSKU list for frontend: {len(sku_list)} unique SKUs")
    
    if sku_list:
        print(f"Sample SKU: {sku_list[0]}")
        
        # Test SKU data generation
        sample_sku_id = sku_list[0]['sku_id']
        sku_data = integrator.get_sku_data_for_frontend(sample_sku_id)
        print(f"\nSample SKU data for {sample_sku_id}:")
        print(f"   - Locations: {len(sku_data['locations'])}")
        print(f"   - Summary: {sku_data['summary']}")
    
    print("\n✅ Data integration test completed successfully!")
