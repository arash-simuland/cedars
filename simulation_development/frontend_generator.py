"""
CedarSim Frontend Data Generator

This module integrates with AntologyGenerator to create visualization data
for the dashboard frontend when the model structure is initialized.

Key Features:
- Generates hospital layout data (PARs by level)
- Creates SKU connection mappings
- Produces time series data for inventory levels
- Exports data in JSON format for frontend consumption
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from core_models import AntologyGenerator, Location, SKU

logger = logging.getLogger(__name__)

class FrontendDataGenerator:
    """Generates visualization data for the dashboard frontend."""
    
    def __init__(self, antology: AntologyGenerator):
        self.antology = antology
        self.hospital_layout = {}
        self.sku_connections = {}
        self.inventory_data = {}
        
    def generate_hospital_layout(self) -> Dict[str, Any]:
        """Generate hospital layout data for the vertical 2D view."""
        
        # Define hospital levels and their PARs
        hospital_levels = {
            "Level 9": {
                "name": "ICU, PCU, Telemetry",
                "pars": ["ICU", "PCU", "Telemetry", "Observation"],
                "color": "#1f77b4",  # Blue
                "level": 9
            },
            "Level 8": {
                "name": "Observation, Medical Tele",
                "pars": ["Observation", "Medical_Tele", "Non_Tele"],
                "color": "#ff7f0e",  # Orange
                "level": 8
            },
            "Level 7": {
                "name": "ICU",
                "pars": ["ICU"],
                "color": "#2ca02c",  # Green
                "level": 7
            },
            "Level 6": {
                "name": "M/S Overflow",
                "pars": ["M_S_Overflow"],
                "color": "#d62728",  # Red
                "level": 6
            },
            "Level 5": {
                "name": "Observation, Medical Tele",
                "pars": ["Observation", "Medical_Tele"],
                "color": "#9467bd",  # Purple
                "level": 5
            },
            "Level 4": {
                "name": "Respiratory Therapy",
                "pars": ["Respiratory_Therapy"],
                "color": "#8c564b",  # Brown
                "level": 4
            },
            "Level 3": {
                "name": "Central Lab, Sterile Processing",
                "pars": ["Central_Lab", "Sterile_Processing", "Food_Service"],
                "color": "#e377c2",  # Pink
                "level": 3
            },
            "Level 2": {
                "name": "Pharmacy, Surgery/PACU",
                "pars": ["Pharmacy", "Surgery", "PACU"],
                "color": "#7f7f7f",  # Gray
                "level": 2
            },
            "Level 1": {
                "name": "ED, Imaging, EVS, Facilities",
                "pars": ["ED", "Imaging", "EVS", "Facilities"],
                "color": "#bcbd22",  # Olive
                "level": 1
            },
            "Level 0": {
                "name": "PERPETUAL (Safety Stock)",
                "pars": ["PERPETUAL"],
                "color": "#17becf",  # Cyan
                "level": 0
            }
        }
        
        # Add SKU counts for each PAR
        for level_name, level_data in hospital_levels.items():
            level_data["pars_data"] = []
            for par_name in level_data["pars"]:
                par_location = self.antology.locations.get(par_name)
                if par_location:
                    sku_count = len(par_location.skus)
                    level_data["pars_data"].append({
                        "name": par_name,
                        "sku_count": sku_count,
                        "total_inventory": par_location.get_current_level(),
                        "stockout_rate": par_location.get_stockout_rate()
                    })
                else:
                    level_data["pars_data"].append({
                        "name": par_name,
                        "sku_count": 0,
                        "total_inventory": 0,
                        "stockout_rate": 0
                    })
        
        self.hospital_layout = hospital_levels
        return hospital_levels
    
    def generate_sku_connections(self) -> Dict[str, Any]:
        """Generate SKU connection mappings for the frontend."""
        
        connections = {}
        
        for sku_id, sku_list in self.antology.sku_registry.items():
            # Find perpetual SKU
            perpetual_sku = None
            par_skus = []
            
            for sku in sku_list:
                if sku.location_id == "PERPETUAL":
                    perpetual_sku = sku
                else:
                    par_skus.append(sku)
            
            if perpetual_sku and par_skus:
                connections[sku_id] = {
                    "perpetual_sku": {
                        "sku_id": perpetual_sku.resource_id,
                        "location_id": perpetual_sku.location_id,
                        "target_level": perpetual_sku.target_level,
                        "current_level": perpetual_sku.get_current_level(),
                        "lead_time_days": perpetual_sku.lead_time_days,
                        "demand_rate": perpetual_sku.demand_rate
                    },
                    "par_skus": [
                        {
                            "sku_id": sku.resource_id,
                            "location_id": sku.location_id,
                            "target_level": sku.target_level,
                            "current_level": sku.get_current_level(),
                            "lead_time_days": sku.lead_time_days,
                            "demand_rate": sku.demand_rate
                        }
                        for sku in par_skus
                    ],
                    "connection_count": len(par_skus)
                }
        
        self.sku_connections = connections
        return connections
    
    def generate_inventory_timeline(self, sku_id: str, weeks: int = 52) -> Dict[str, Any]:
        """Generate inventory timeline data for a specific SKU."""
        
        if sku_id not in self.sku_connections:
            return {"error": f"SKU {sku_id} not found"}
        
        sku_data = self.sku_connections[sku_id]
        timeline = {
            "weeks": list(range(1, weeks + 1)),
            "perpetual": [],
            "pars": {}
        }
        
        # Generate sample inventory data (in real implementation, this would come from simulation)
        import random
        random.seed(42)  # For reproducible results
        
        # Perpetual inventory timeline
        base_level = sku_data["perpetual_sku"]["target_level"]
        for week in range(weeks):
            # Simulate inventory fluctuations
            variation = random.uniform(-0.1, 0.1) * base_level
            level = max(0, base_level + variation)
            timeline["perpetual"].append(round(level, 2))
        
        # PAR inventory timelines
        for par_sku in sku_data["par_skus"]:
            par_id = par_sku["location_id"]
            base_level = par_sku["target_level"]
            timeline["pars"][par_id] = []
            
            for week in range(weeks):
                # Simulate demand and replenishment
                demand = par_sku["demand_rate"]
                variation = random.uniform(-0.2, 0.2) * base_level
                level = max(0, base_level + variation - (demand * week * 0.1))
                timeline["pars"][par_id].append(round(level, 2))
        
        return timeline
    
    def generate_frontend_data(self) -> Dict[str, Any]:
        """Generate complete frontend data package."""
        
        logger.info("Generating frontend data...")
        
        # Generate all data components
        hospital_layout = self.generate_hospital_layout()
        sku_connections = self.generate_sku_connections()
        
        # Create SKU list for dropdown
        sku_list = []
        for sku_id, sku_data in sku_connections.items():
            sku_list.append({
                "sku_id": sku_id,
                "perpetual_level": sku_data["perpetual_sku"]["current_level"],
                "par_count": sku_data["connection_count"],
                "total_demand": sum(par["demand_rate"] for par in sku_data["par_skus"])
            })
        
        # Sort by SKU ID for consistent ordering
        sku_list.sort(key=lambda x: x["sku_id"])
        
        frontend_data = {
            "hospital_layout": hospital_layout,
            "sku_connections": sku_connections,
            "sku_list": sku_list,
            "metadata": {
                "total_skus": len(sku_connections),
                "total_pars": len(self.antology.locations),
                "generated_at": pd.Timestamp.now().isoformat()
            }
        }
        
        logger.info(f"Generated frontend data: {len(sku_connections)} SKUs, {len(self.antology.locations)} PARs")
        return frontend_data
    
    def export_frontend_data(self, output_file: str = "frontend_data.json"):
        """Export frontend data to JSON file."""
        
        frontend_data = self.generate_frontend_data()
        
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(frontend_data, f, indent=2)
        
        logger.info(f"Frontend data exported to {output_path}")
        return output_path

# Integration with AntologyGenerator
def create_frontend_integration(antology: AntologyGenerator) -> FrontendDataGenerator:
    """Create frontend data generator integrated with AntologyGenerator."""
    
    # Generate frontend data when structure is finalized
    frontend_gen = FrontendDataGenerator(antology)
    
    # Export data for frontend consumption
    frontend_gen.export_frontend_data("frontend_data.json")
    
    return frontend_gen

# Example usage
if __name__ == "__main__":
    # This would be called after AntologyGenerator.finalize_network()
    from core_models import AntologyGenerator, ResourceFactory
    
    # Create sample antology (in real usage, this would be fully populated)
    antology = AntologyGenerator()
    
    # Add sample locations
    perpetual = ResourceFactory.create_location("PERPETUAL", "Perpetual")
    ed = ResourceFactory.create_location("ED", "PAR")
    surgery = ResourceFactory.create_location("Surgery", "PAR")
    
    antology.add_location(perpetual)
    antology.add_location(ed)
    antology.add_location(surgery)
    
    # Add sample SKUs
    sku_001_perpetual = ResourceFactory.create_sku("SKU_001", "PERPETUAL", 
                                                   target_level=100, lead_time_days=2.0, demand_rate=0)
    sku_001_ed = ResourceFactory.create_sku("SKU_001", "ED", 
                                           target_level=50, lead_time_days=1.5, demand_rate=10.0)
    sku_001_surgery = ResourceFactory.create_sku("SKU_001", "Surgery", 
                                                target_level=30, lead_time_days=1.0, demand_rate=5.0)
    
    antology.add_sku(sku_001_perpetual)
    antology.add_sku(sku_001_ed)
    antology.add_sku(sku_001_surgery)
    
    # Add SKUs to locations
    perpetual.add_sku(sku_001_perpetual)
    ed.add_sku(sku_001_ed)
    surgery.add_sku(sku_001_surgery)
    
    # Generate network connections
    antology.generate_network_connections()
    antology.finalize_network()
    
    # Create frontend integration
    frontend_gen = create_frontend_integration(antology)
    
    print("Frontend data generated successfully!")
    print(f"Generated {len(frontend_gen.sku_connections)} SKU connections")
    print(f"Generated {len(frontend_gen.hospital_layout)} hospital levels")
