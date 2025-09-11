#!/usr/bin/env python3
"""
CedarSim 3D Visualization Pipeline
==================================

This script creates a 3D visualization of the CedarSim inventory management system,
showing locations, SKU objects, and their connections in a hierarchical 3D space.

Features:
- 3D location nodes positioned hierarchically by level
- SKU objects as particles within each location
- Emergency replenishment connections between locations
- Interactive visualization with rotation, zoom, and selection
- Real-time inventory level visualization
- Connection strength based on SKU overlap

Author: CedarSim Visualization Team
Date: September 11, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CedarSim3DVisualizer:
    """3D Visualization engine for CedarSim inventory management system"""
    
    def __init__(self, data_file: str = "../../data/final/CedarSim_Simulation_Ready_Data_Final.xlsx"):
        self.data_file = Path(data_file)
        self.sku_data = None
        self.demand_data = None
        
        # Location hierarchy and positioning (Z-axis represents hospital floor levels)
        # Updated to match actual Cedar Hospital 9-level stacking diagram with Level 0 for Perpetual
        self.location_hierarchy = {
            'Level0': {'level': 0, 'x': 0, 'y': 0, 'z': 0, 'color': 'darkgreen', 'size': 1200},   # Level 0 - Perpetual Inventory (Underground Distribution Hub)
            'Level1': {'level': 1, 'x': 0, 'y': 0, 'z': 1, 'color': 'orange', 'size': 1000},      # Level 1 - Emergency, Imaging, Mat Management, Security, Lobby Admin
            'Level2': {'level': 2, 'x': 0, 'y': 0, 'z': 2, 'color': 'red', 'size': 800},          # Level 2 - Pharmacy, Surgery/Procedures/PACU/Pre-Op, Energy Center
            'Level3': {'level': 3, 'x': 0, 'y': 0, 'z': 3, 'color': 'green', 'size': 600},        # Level 3 - Sterile Processing, Central Lab, Admin, Food Service
            'Level4': {'level': 4, 'x': 0, 'y': 0, 'z': 4, 'color': 'gray', 'size': 500},         # Level 4 - Support (MECH/ELEC/MTR)
            'Level5': {'level': 5, 'x': 0, 'y': 0, 'z': 5, 'color': 'lightblue', 'size': 400},    # Level 5 - Marina 5 (32 beds) - Observation, Medical Tele & Non-Tele
            'Level6': {'level': 6, 'x': 0, 'y': 0, 'z': 6, 'color': 'blue', 'size': 400},         # Level 6 - Marina 6 (32 beds) - Telemetry, Cardiac & Stroke Focus
            'Level7': {'level': 7, 'x': 0, 'y': 0, 'z': 7, 'color': 'darkblue', 'size': 400},     # Level 7 - Marina 7-PCU (16 beds) + Marina 7-ICU (16 beds)
            'Level8': {'level': 8, 'x': 0, 'y': 0, 'z': 8, 'color': 'navy', 'size': 400},         # Level 8 - Marina 8 (32 beds) - M/S Overflow, VIP Med, Int'l Med
            'Level9': {'level': 9, 'x': 0, 'y': 0, 'z': 9, 'color': 'indigo', 'size': 400}        # Level 9 - Marina 9 (32 beds) - Surgical, Non-Infectious + Mechanical
        }
        
        # Location mapping from data columns to actual Cedar Hospital layout
        self.location_mapping = {
            # Level 0 - Perpetual Inventory (Underground Distribution Hub)
            'Level 1 Perpetual_1400': 'Level0',  # Perpetual inventory (underground distribution hub)
            
            # Level 1 - Emergency Department, Imaging, Mat Management, Security, Lobby Admin
            'Level 1 Facilities/Biomed_1232': 'Level1',  # Material Management
            'Level 1 EVS_1321': 'Level1',  # Security/Support
            'Level 1 ED_1229': 'Level1',  # Emergency Department
            'Level 1 Imaging_1329': 'Level1',  # Imaging
            'Level 1 Lobby Admin': 'Level1',  # Lobby Admin
            
            # Level 2 - Pharmacy, Surgery/Procedures/PACU/Pre-Op Recovery, Energy Center
            'Level 2 Pharm_2500': 'Level2',  # Pharmacy
            'Level 2 Surgery/Procedures/PACU_2209_2321_2323_2450_2200B_2450A': 'Level2',  # Surgery/Procedures/PACU/Pre-Op
            'Level 2 Energy Center': 'Level2',  # Energy Center
            
            # Level 3 - Sterile Processing, Central Lab, Admin, Food Service
            'Level 3 Sterile Processing_3307_3309': 'Level3',  # Sterile Processing
            'Level 3 Central Lab_3411': 'Level3',  # Central Lab
            'Level 3 Admin': 'Level3',  # Admin
            'Level 3 Food Service': 'Level3',  # Food Service
            
            # Level 4 - Support (MECH/ELEC/MTR) - Mechanical, Electrical, Materials
            'Level 4 Support': 'Level4',  # Support - MECH/ELEC/MTR
            
            # Level 5 - Marina 5 (32 beds) - Observation, Medical Tele & Non-Tele
            'Level 5 Observation, Medical Tele & Non-Tele_5206': 'Level5',  # Marina 5
            
            # Level 6 - Marina 6 (32 beds) - Telemetry, Cardiac & Stroke Focus
            'Level 6 Telemetry, Cardiac & Stroke': 'Level6',  # Marina 6
            
            # Level 7 - Marina 7-PCU (16 beds) + Marina 7-ICU (16 beds)
            'Level 7 ICU': 'Level7',  # Marina 7-ICU
            'Level 7 PCU': 'Level7',  # Marina 7-PCU
            
            # Level 8 - Marina 8 (32 beds) - M/S Overflow, VIP Med, Int'l Med
            'Level 8 M/S Overflow, VIP & Int\'l Med': 'Level8',  # Marina 8
            
            # Level 9 - Marina 9 (32 beds) - Surgical, Non-Infectious + Mechanical
            'Level 9 Surgical, Non-Infectious': 'Level9',  # Marina 9
            
            # Additional locations that may exist in data
            'Respiratory Therapy': 'Level4'  # Respiratory therapy (mapped to Level 4 support)
        }
        
        # SKU visualization properties
        self.sku_properties = {
            'size_scale': 0.1,
            'opacity': 0.7,
            'color_by': 'inventory_level'  # or 'lead_time', 'demand_rate'
        }
    
    def load_data(self) -> bool:
        """Load data from Excel files"""
        try:
            logger.info(f"Loading data from {self.data_file}")
            
            # Load SKU inventory data
            self.sku_data = pd.read_excel(self.data_file, sheet_name='01_SKU_Inventory_Final')
            logger.info(f"Loaded {len(self.sku_data)} SKUs")
            
            # Load demand data (sampled for performance with smaller batches)
            self.demand_data = pd.read_excel(self.data_file, sheet_name='02_Demand_Data_Clean')
            if len(self.demand_data) > 500:
                self.demand_data = self.demand_data.sample(n=500, random_state=42)
            logger.info(f"Loaded {len(self.demand_data)} demand records (sampled)")
            
            # Note: Validation data not needed for visualization - only for simulation optimization
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def get_location_columns(self) -> List[str]:
        """Get all PAR location columns from SKU data"""
        return [col for col in self.sku_data.columns if 'Level' in col or 'Perpetual' in col or 'Respiratory' in col]
    
    def calculate_location_positions(self) -> Dict[str, Dict]:
        """Calculate 3D positions for each location based on hierarchy"""
        locations = {}
        location_columns = self.get_location_columns()
        
        # Group locations by hierarchy level
        level_groups = {}
        for col in location_columns:
            hierarchy_key = self.location_mapping.get(col, 'Level9')  # Default to highest level
            if hierarchy_key not in level_groups:
                level_groups[hierarchy_key] = []
            level_groups[hierarchy_key].append(col)
        
        # Calculate positions for each level
        for hierarchy_key, location_list in level_groups.items():
            base_config = self.location_hierarchy[hierarchy_key]
            n_locations = len(location_list)
            
            # Special handling for Level 1 - place Perpetual at center
            if hierarchy_key == 'Level1':
                # Find Perpetual location and place it at center
                perpetual_location = None
                other_locations = []
                
                for location in location_list:
                    if 'Perpetual' in location:
                        perpetual_location = location
                    else:
                        other_locations.append(location)
                
                # Place Perpetual at center (0, 0, z)
                if perpetual_location:
                    locations[perpetual_location] = {
                        'x': 0,
                        'y': 0,
                        'z': base_config['z'],
                        'level': base_config['level'],
                        'color': base_config['color'],
                        'size': base_config['size'],
                        'hierarchy': hierarchy_key
                    }
                
                # Arrange other Level 1 locations in a circle around Perpetual
                for i, location in enumerate(other_locations):
                    angle = 2 * np.pi * i / len(other_locations)
                    radius = 3  # Fixed radius around center
                    
                    x = radius * np.cos(angle)
                    y = radius * np.sin(angle)
                    z = base_config['z']
                    
                    locations[location] = {
                        'x': x,
                        'y': y, 
                        'z': z,
                        'level': base_config['level'],
                        'color': base_config['color'],
                        'size': base_config['size'],
                        'hierarchy': hierarchy_key
                    }
            else:
                # Arrange other levels in a circle as before
                for i, location in enumerate(location_list):
                    angle = 2 * np.pi * i / n_locations
                    radius = 3 + hierarchy_key.count('Level') * 2  # Increase radius for higher levels
                    
                    x = radius * np.cos(angle)
                    y = radius * np.sin(angle)
                    z = base_config['z']
                    
                    locations[location] = {
                        'x': x,
                        'y': y, 
                        'z': z,
                        'level': base_config['level'],
                        'color': base_config['color'],
                        'size': base_config['size'],
                        'hierarchy': hierarchy_key
                    }
        
        return locations
    
    def calculate_sku_positions(self, location: str, sku_count: int) -> List[Dict]:
        """Calculate 3D positions for SKUs within a location"""
        if sku_count == 0:
            return []
        
        # Get location center
        location_pos = self.calculate_location_positions()[location]
        center_x, center_y, center_z = location_pos['x'], location_pos['y'], location_pos['z']
        
        # Arrange SKUs in a sphere around the location center
        sku_positions = []
        radius = 1.5  # Sphere radius around location
        
        for i in range(sku_count):
            # Generate points on sphere surface
            phi = np.random.uniform(0, 2 * np.pi)
            costheta = np.random.uniform(-1, 1)
            theta = np.arccos(costheta)
            
            x = center_x + radius * np.sin(theta) * np.cos(phi)
            y = center_y + radius * np.sin(theta) * np.sin(phi)
            z = center_z + radius * np.cos(theta)
            
            sku_positions.append({
                'x': x,
                'y': y,
                'z': z,
                'location': location
            })
        
        return sku_positions
    
    def calculate_connections(self) -> List[Dict]:
        """Calculate emergency replenishment connections - FROM Perpetual TO PARs"""
        connections = []
        location_columns = self.get_location_columns()
        
        # Find the Perpetual location
        perpetual_location = None
        for col in location_columns:
            if 'Perpetual' in col:
                perpetual_location = col
                break
        
        if not perpetual_location:
            logger.warning("No Perpetual location found")
            return connections
        
        # Find SKUs that exist in both Perpetual and PAR locations
        for _, sku_row in self.sku_data.iterrows():
            sku_id = sku_row['Oracle Item Number']
            
            # Check if SKU exists in Perpetual
            if pd.notna(sku_row[perpetual_location]):
                # Find which PAR locations this SKU also exists in
                par_locations = []
                for col in location_columns:
                    if col != perpetual_location and pd.notna(sku_row[col]):
                        par_locations.append(col)
                
                # Create connections FROM Perpetual TO each PAR (logical flow direction)
                for par_location in par_locations:
                    connections.append({
                        'from': perpetual_location,
                        'to': par_location,
                        'sku_id': sku_id,
                        'weight': 1,
                        'type': 'emergency_replenishment'
                    })
        
        return connections
    
    def create_combined_visualization(self, output_file: str = "cedarsim_combined_visualization.html") -> bool:
        """Create simple combined 3D network visualization (like the originals)"""
        try:
            logger.info("Creating simple combined 3D network visualization...")
            
            # Calculate positions
            location_positions = self.calculate_location_positions()
            connections = self.calculate_connections()
            
            # Create figure
            fig = go.Figure()
            
            # Add network connections first (as base layer)
            connection_counts = {}
            for conn in connections:
                edge_key = tuple(sorted([conn['from'], conn['to']]))
                connection_counts[edge_key] = connection_counts.get(edge_key, 0) + 1
            
            for (loc1, loc2), count in connection_counts.items():
                from_pos = location_positions.get(loc1)
                to_pos = location_positions.get(loc2)
                
                if from_pos and to_pos:
                    fig.add_trace(go.Scatter3d(
                        x=[from_pos['x'], to_pos['x']],
                        y=[from_pos['y'], to_pos['y']],
                        z=[from_pos['z'], to_pos['z']],
                        mode='lines',
                        line=dict(
                            color='gray',
                            width=2,
                            dash='dash'
                        ),
                        name=f"Connection {loc1} → {loc2}",
                        showlegend=False,
                        hovertemplate=f"Emergency Replenishment<br>From: {loc1}<br>To: {loc2}<br>SKU Connections: {count}<extra></extra>"
                    ))
            
            # Add location nodes (simple, like the originals)
            for location, pos in location_positions.items():
                # Count SKUs in this location
                sku_count = self.sku_data[location].notna().sum()
                
                fig.add_trace(go.Scatter3d(
                    x=[pos['x']],
                    y=[pos['y']],
                    z=[pos['z']],
                    mode='markers',
                    marker=dict(
                        size=15,  # Fixed size like originals
                        color=pos['color'],
                        opacity=0.8,
                        line=dict(width=2, color='black')
                    ),
                    name=location,
                    text=f"{location}<br>SKUs: {sku_count}",
                    hovertemplate="<b>%{text}</b><br>" +
                                "X: %{x:.2f}<br>" +
                                "Y: %{y:.2f}<br>" +
                                "Z: %{z:.2f}<extra></extra>"
                ))
            
            # Update layout (simple like originals)
            fig.update_layout(
                title="CedarSim Hospital Inventory Network - 3D Visualization<br><sub>Z-axis represents Cedar Hospital floor levels (Level 0=Underground, Level 1=Ground, Level 9=Top Floor)<br>Level 0: Perpetual Inventory (Underground Distribution Hub) | Level 1: Emergency, Imaging, Materials Mgmt<br>Level 2: Pharmacy, Surgery, PACU | Level 3: Lab, SPD, Food Service | Level 4: Support (MECH/ELEC/MTR)<br>Levels 5-9: Marina Nursing Units (32 beds each)</sub>",
                scene=dict(
                    xaxis_title="X Position",
                    yaxis_title="Y Position", 
                    zaxis_title="Hospital Floor Level",
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.5)
                    )
                ),
                width=1200,
                height=800,
                showlegend=True
            )
            
            # Save visualization
            output_path = Path(output_file)
            fig.write_html(str(output_path))
            logger.info(f"Simple combined 3D network visualization saved to {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating combined visualization: {str(e)}")
            return False
    
    def create_network_visualization(self, output_file: str = "cedarsim_network.html") -> bool:
        """Create network graph visualization of location connections"""
        try:
            logger.info("Creating network visualization...")
            
            # Create network graph
            G = nx.Graph()
            
            # Add location nodes
            location_positions = self.calculate_location_positions()
            for location, pos in location_positions.items():
                sku_count = self.sku_data[location].notna().sum()
                G.add_node(location, 
                          x=pos['x'], 
                          y=pos['y'], 
                          z=pos['z'],
                          sku_count=sku_count,
                          level=pos['level'],
                          hierarchy=pos['hierarchy'])
            
            # Add connections
            connections = self.calculate_connections()
            connection_counts = {}
            for conn in connections:
                edge_key = tuple(sorted([conn['from'], conn['to']]))
                connection_counts[edge_key] = connection_counts.get(edge_key, 0) + 1
            
            for (loc1, loc2), count in connection_counts.items():
                G.add_edge(loc1, loc2, weight=count)
            
            # Create network visualization
            pos_3d = {node: (data['x'], data['y'], data['z']) for node, data in G.nodes(data=True)}
            
            # Extract coordinates
            x_nodes = [pos_3d[node][0] for node in G.nodes()]
            y_nodes = [pos_3d[node][1] for node in G.nodes()]
            z_nodes = [pos_3d[node][2] for node in G.nodes()]
            
            # Create edge traces
            edge_x = []
            edge_y = []
            edge_z = []
            
            for edge in G.edges():
                x0, y0, z0 = pos_3d[edge[0]]
                x1, y1, z1 = pos_3d[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_z.extend([z0, z1, None])
            
            # Create figure
            fig = go.Figure()
            
            # Add edges
            fig.add_trace(go.Scatter3d(
                x=edge_x, y=edge_y, z=edge_z,
                mode='lines',
                line=dict(color='gray', width=2),
                hoverinfo='none',
                showlegend=False
            ))
            
            # Add nodes
            fig.add_trace(go.Scatter3d(
                x=x_nodes, y=y_nodes, z=z_nodes,
                mode='markers',
                marker=dict(
                    size=20,  # Fixed size for all nodes
                    color=[G.nodes[node]['level'] for node in G.nodes()],
                    colorscale='Viridis',
                    opacity=0.8,
                    line=dict(width=2, color='black')
                ),
                text=[f"{node}<br>SKUs: {G.nodes[node]['sku_count']}" for node in G.nodes()],
                hovertemplate="<b>%{text}</b><br>" +
                            "X: %{x:.2f}<br>" +
                            "Y: %{y:.2f}<br>" +
                            "Z: %{z:.2f}<extra></extra>",
                name="Locations"
            ))
            
            # Update layout
            fig.update_layout(
                title="CedarSim Location Network - Emergency Replenishment Connections<br><sub>Z-axis represents hospital floor levels (Level 0=Underground, Level 1=Ground, Level 9=Top Floor)<br>Perpetual Inventory (Underground Distribution Hub) serves all levels above</sub>",
                scene=dict(
                    xaxis_title="X Position",
                    yaxis_title="Y Position",
                    zaxis_title="Hospital Floor Level",
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
                ),
                width=1200,
                height=800
            )
            
            # Save visualization
            output_path = Path(output_file)
            fig.write_html(str(output_path))
            logger.info(f"Network visualization saved to {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating network visualization: {str(e)}")
            return False
    
    def generate_visualization_report(self) -> str:
        """Generate a concise summary report of the visualization"""
        location_positions = self.calculate_location_positions()
        connections = self.calculate_connections()
        
        # Count SKUs per location
        sku_counts = {}
        for location in location_positions.keys():
            sku_counts[location] = self.sku_data[location].notna().sum()
        
        # Get top 5 locations by SKU count
        top_locations = sorted(sku_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        report = f"""# CedarSim 3D Visualization Report
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Locations**: {len(location_positions)} hospital locations across 9 levels
- **SKUs**: {len(self.sku_data):,} total inventory items
- **Connections**: {len(connections):,} emergency replenishment paths
- **Type**: Interactive 3D visualizations with Plotly

## Top Locations by SKU Count
"""
        
        for location, count in top_locations:
            report += f"- **{location}**: {count:,} SKUs\n"
        
        report += f"""
## Files Generated
- `cedarsim_combined_visualization.html` - Combined 3D network visualization
- `cedarsim_network.html` - Network graph visualization
- `cedarsim_visualization_report.md` - This report

---
*Open the HTML files in your browser to explore the interactive 3D visualizations.*
"""
        
        return report
    
    def run_complete_pipeline(self) -> bool:
        """Run the complete 3D visualization pipeline"""
        print("=" * 70)
        print("CEDARSIM 3D VISUALIZATION PIPELINE")
        print("=" * 70)
        logger.info("=" * 70)
        logger.info("CEDARSIM 3D VISUALIZATION PIPELINE")
        logger.info("=" * 70)
        
        try:
            # Step 1: Load data
            print("Step 1: Loading data...")
            if not self.load_data():
                print("ERROR: Data loading failed")
                return False
            print("✅ Data loaded successfully")
            
            # Step 2: Create combined 3D network visualization
            print("Step 2: Creating combined 3D network visualization...")
            if not self.create_combined_visualization():
                print("ERROR: Combined visualization creation failed")
                return False
            print("✅ Combined 3D network visualization created")
            
            # Step 3: Create network graph visualization
            print("Step 3: Creating network graph visualization...")
            if not self.create_network_visualization():
                print("ERROR: Network visualization creation failed")
                return False
            print("✅ Network graph visualization created")
            
            # Step 4: Generate report
            report = self.generate_visualization_report()
            report_file = Path("cedarsim_visualization_report.md")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Visualization report saved to {report_file}")
            
            logger.info("=" * 70)
            logger.info("3D VISUALIZATION PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("=" * 70)
            logger.info("Generated files:")
            logger.info("  - cedarsim_combined_visualization.html (Combined 3D Network with Location Clusters)")
            logger.info("  - cedarsim_network.html (Network Graph Visualization)")
            logger.info("  - cedarsim_visualization_report.md (Summary Report)")
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return False

def main():
    """Main function to run the 3D visualization pipeline"""
    print("CedarSim 3D Visualization Pipeline")
    print("=" * 50)
    
    # Initialize visualizer
    visualizer = CedarSim3DVisualizer()
    
    # Run complete pipeline
    success = visualizer.run_complete_pipeline()
    
    if success:
        print("\n✅ SUCCESS: 3D visualization pipeline completed!")
        print("Open the HTML files in your browser to view the visualizations.")
    else:
        print("\n❌ FAILED: Pipeline execution failed. Check logs for details.")
    
    return success

if __name__ == "__main__":
    main()
