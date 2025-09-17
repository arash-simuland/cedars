#!/usr/bin/env python3
"""
CedarSim Location Mapping Module

This module handles the mapping between SKU data locations and demand data locations
based on the manual analysis of location patterns.

Key Features:
- Maps SKU locations (e.g., "Level 1 ED") to demand locations (e.g., "MDRER")
- Handles both direct mappings and consolidated mappings
- Provides reverse mapping for demand data to SKU locations
- Supports validation and debugging of location mappings
"""

from typing import Dict, List, Optional, Tuple, Set
import logging

logger = logging.getLogger(__name__)

class LocationMapper:
    """Maps between SKU data locations and demand data locations."""
    
    def __init__(self):
        """Initialize the location mapper with predefined mappings."""
        self.sku_to_demand_mapping = self._create_sku_to_demand_mapping()
        self.demand_to_sku_mapping = self._create_demand_to_sku_mapping()
        self.unmapped_locations = set()
    
    def _create_sku_to_demand_mapping(self) -> Dict[str, str]:
        """Create mapping from SKU locations to demand locations based on analysis."""
        return {
            # SKU Data Locations → Demand Data Locations (Primary mappings)
            "Level 1 ED": "MDRER",
            "Level 1 EVS_1321": "MDREVS", 
            "Level 1 Imaging": "MDRXRAY",
            "Level 2 Pharm": "MDRRX",
            "Level 2 Surgery/Procedures/PACU": "MDRSURGERY",
            "Level 3 Admin": "MDRPURCHAS",
            "Level 3 Central Lab": "MDRLAB",
            "Level 3 Food Service": "MDRDIETARY",
            "Level 3 Sterile Processing_3307_3309": "MDRGI",
            "Level 5 Observation, Medical Tele & Non-Tele": "MDR7010ME",
            "Level 6 Telemetry, Cardiac & Stroke": "MDR6150TEL",
            "Level 7 ICU": "MDRICUPRO",
            "Perpetual": "MDRCS",
            "Respiratory Therapy": "MDRRT",
            
            # Standard Locations → Demand Data Locations
            "Level 2 ICU": "MDRICUPRO",
            "Level 3 Medical": "MDR7010ME",
            "Level 4 Medical": "MDR7010ME",
            "Level 6 Surgical": "MDRSURGERY",
            "Level 7 Surgical": "MDRSURGERY",
            "Level 8 Surgical": "MDRSURGERY",
            "Level 9 Surgical": "MDRSURGERY",
            "Level 10 Surgical": "MDRSURGERY",
        }
    
    def _create_demand_to_sku_mapping_extended(self) -> Dict[str, List[str]]:
        """Create extended mapping from demand locations to SKU locations."""
        return {
            # Primary mappings
            "MDRER": ["Level 1 ED"],
            "MDREVS": ["Level 1 EVS_1321"],
            "MDRXRAY": ["Level 1 Imaging"],
            "MDRRX": ["Level 2 Pharm"],
            "MDRSURGERY": ["Level 2 Surgery/Procedures/PACU", "Level 6 Surgical", "Level 7 Surgical", "Level 8 Surgical", "Level 9 Surgical", "Level 10 Surgical"],
            "MDRPURCHAS": ["Level 3 Admin"],
            "MDRLAB": ["Level 3 Central Lab"],
            "MDRDIETARY": ["Level 3 Food Service"],
            "MDRGI": ["Level 3 Sterile Processing_3307_3309"],
            "MDR7010ME": ["Level 3 Medical", "Level 4 Medical", "Level 5 Observation, Medical Tele & Non-Tele"],
            "MDR6150TEL": ["Level 6 Telemetry, Cardiac & Stroke"],
            "MDRICUPRO": ["Level 2 ICU", "Level 7 ICU"],
            "MDRCS": ["Perpetual"],
            "MDRRT": ["Respiratory Therapy"],
            
            # Extended mappings based on pattern analysis
            # MDR7010 variations (Medical units)
            "MDR7010JI": ["Level 3 Medical"],  # JIT/Just-In-Time pattern
            "MDR7010OM": ["Level 3 Medical"],  # Medical unit pattern
            "MDR7010OR": ["Level 3 Medical"],  # OR/Operating Room pattern
            "MDR7010PED": ["Level 3 Medical"], # Pediatric pattern
            "MDR7010TR": ["Level 3 Medical"],  # Medical unit pattern
            
            # MDR6 variations (Level 6 units)
            "MDR6170MS": ["Level 6 Surgical"],  # MS/Medical Surgical pattern
            "MDR6172EAS": ["Level 6 Surgical"], # Surgical unit pattern
            "MDR6010JIT": ["Level 6 Surgical"], # JIT pattern
            
            # MDR7 variations (Level 7 units)
            "MDR7420OR": ["Level 7 Surgical"],  # OR pattern
            "MDR7430SS": ["Level 7 Surgical"],  # Surgical unit pattern
            "MDR7470OD": ["Level 7 Surgical"],  # Surgical unit pattern
            "MDR7710RX": ["Level 7 Surgical"],  # RX pattern
            
            # Wing-based patterns
            "MDR1NORTH": ["Level 1 ED"],  # North wing of ED
            "MDR1SOUTH": ["Level 1 ED"],  # South wing of ED
            
            # Central Supply variations
            "TORDC\\MDRCS": ["Perpetual"],  # Central Supply with TORDC prefix
            "MDRDOCK": ["Perpetual"],  # Dock/Receiving pattern
            "CS0075": ["Perpetual"],  # Central Supply code
            
            # TORDC prefix variations (likely consolidated locations)
            "TORDC\\MDR7420OR": ["Level 2 Surgery/Procedures/PACU"],  # OR with TORDC prefix
            "TORDC\\MDRDIETARY": ["Level 3 Food Service"],  # Dietary with TORDC prefix
            "TORDC\\MDRPURCHAS": ["Level 3 Admin"],  # Purchasing with TORDC prefix
            "TORDC\\MDRRT": ["Respiratory Therapy"],  # RT with TORDC prefix
            "TORDC\\MDRRX": ["Level 2 Pharm"],  # RX with TORDC prefix
        }
    
    def _create_demand_to_sku_mapping(self) -> Dict[str, List[str]]:
        """Create reverse mapping from demand locations to SKU locations."""
        # Start with the extended mapping
        reverse_mapping = self._create_demand_to_sku_mapping_extended()
        
        # Add any additional mappings from the primary SKU to demand mapping
        for sku_loc, demand_loc in self.sku_to_demand_mapping.items():
            if demand_loc not in reverse_mapping:
                reverse_mapping[demand_loc] = []
            if sku_loc not in reverse_mapping[demand_loc]:
                reverse_mapping[demand_loc].append(sku_loc)
        
        return reverse_mapping
    
    def map_sku_to_demand_location(self, sku_location: str) -> Optional[str]:
        """
        Map a SKU location to its corresponding demand location.
        
        Args:
            sku_location: The location from SKU data (e.g., "Level 1 ED")
            
        Returns:
            The corresponding demand location (e.g., "MDRER") or None if not found
        """
        if sku_location in self.sku_to_demand_mapping:
            return self.sku_to_demand_mapping[sku_location]
        else:
            self.unmapped_locations.add(sku_location)
            logger.warning(f"No mapping found for SKU location: {sku_location}")
            return None
    
    def map_demand_to_sku_locations(self, demand_location: str) -> List[str]:
        """
        Map a demand location to its corresponding SKU locations.
        
        Args:
            demand_location: The location from demand data (e.g., "MDRER")
            
        Returns:
            List of corresponding SKU locations (e.g., ["Level 1 ED"])
        """
        return self.demand_to_sku_mapping.get(demand_location, [])
    
    def get_all_sku_locations(self) -> Set[str]:
        """Get all SKU locations that have mappings."""
        return set(self.sku_to_demand_mapping.keys())
    
    def get_all_demand_locations(self) -> Set[str]:
        """Get all demand locations that have mappings."""
        return set(self.demand_to_sku_mapping.keys())
    
    def get_unmapped_locations(self) -> Set[str]:
        """Get all locations that couldn't be mapped."""
        return self.unmapped_locations.copy()
    
    def validate_mappings(self, sku_locations: Set[str], demand_locations: Set[str]) -> Dict[str, any]:
        """
        Validate the mappings against actual data locations.
        
        Args:
            sku_locations: Set of actual SKU locations from data
            demand_locations: Set of actual demand locations from data
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'mapped_sku_locations': 0,
            'unmapped_sku_locations': [],
            'mapped_demand_locations': 0,
            'unmapped_demand_locations': [],
            'coverage_percentage': 0.0
        }
        
        # Check SKU locations
        for sku_loc in sku_locations:
            if sku_loc in self.sku_to_demand_mapping:
                results['mapped_sku_locations'] += 1
            else:
                results['unmapped_sku_locations'].append(sku_loc)
        
        # Check demand locations
        for demand_loc in demand_locations:
            if demand_loc in self.demand_to_sku_mapping:
                results['mapped_demand_locations'] += 1
            else:
                results['unmapped_demand_locations'].append(demand_loc)
        
        # Calculate coverage
        total_sku_locations = len(sku_locations)
        if total_sku_locations > 0:
            results['coverage_percentage'] = (results['mapped_sku_locations'] / total_sku_locations) * 100
        
        return results
    
    def print_mapping_summary(self):
        """Print a summary of the location mappings."""
        print("=" * 60)
        print("CEDARSIM LOCATION MAPPING SUMMARY")
        print("=" * 60)
        
        print(f"\n📊 Mapping Statistics:")
        print(f"   SKU Locations Mapped: {len(self.sku_to_demand_mapping)}")
        print(f"   Demand Locations Mapped: {len(self.demand_to_sku_mapping)}")
        print(f"   Unmapped Locations: {len(self.unmapped_locations)}")
        
        print(f"\n🔗 SKU → Demand Mappings:")
        for sku_loc, demand_loc in sorted(self.sku_to_demand_mapping.items()):
            print(f"   {sku_loc:<40} → {demand_loc}")
        
        print(f"\n🔄 Demand → SKU Mappings:")
        for demand_loc, sku_locs in sorted(self.demand_to_sku_mapping.items()):
            if len(sku_locs) == 1:
                print(f"   {demand_loc:<15} ← {sku_locs[0]}")
            else:
                print(f"   {demand_loc:<15} ← {', '.join(sku_locs)}")
        
        if self.unmapped_locations:
            print(f"\n⚠️  Unmapped Locations:")
            for loc in sorted(self.unmapped_locations):
                print(f"   {loc}")
        
        print("=" * 60)

# Global instance for easy access
location_mapper = LocationMapper()

def get_location_mapper() -> LocationMapper:
    """Get the global location mapper instance."""
    return location_mapper

if __name__ == "__main__":
    # Test the location mapper
    mapper = LocationMapper()
    mapper.print_mapping_summary()
    
    # Test some mappings
    print("\n🧪 Testing Mappings:")
    test_locations = [
        "Level 1 ED",
        "Level 2 ICU", 
        "Level 6 Surgical",
        "Perpetual",
        "Unknown Location"
    ]
    
    for loc in test_locations:
        mapped = mapper.map_sku_to_demand_location(loc)
        print(f"   {loc:<30} → {mapped}")
