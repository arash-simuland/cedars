# CedarSim 3D Visualization System

## 🎯 Overview

The CedarSim 3D Visualization System creates interactive 3D visualizations of the hospital inventory management system, showing:

- **Location Hierarchy**: 18 locations arranged in 3D space by hierarchy level
- **SKU Objects**: Individual SKUs as particles within each location
- **Emergency Connections**: Replenishment paths between locations for shared SKUs
- **Interactive Features**: Rotation, zoom, selection, and hover information

## 🏗️ Architecture

### **3D Space Layout**
```
Z-Axis (Hierarchy Levels):
├── Level 0: Perpetual (Safety Stock) - Red, Large
├── Level 1: ED, Imaging, EVS, Facilities - Orange, Medium
├── Level 2: Pharmacy, Surgery/PACU - Yellow, Medium  
├── Level 3: Central Lab, Sterile Processing, Food Service - Green, Small
├── Level 4: Respiratory Therapy - Purple, Small
└── Level 5-9: ICU, PCU, Telemetry, Observation - Blue, Small
```

### **Visualization Components**

1. **Location Nodes**: Spheres positioned in 3D space
   - Size: Proportional to SKU count
   - Color: Based on hierarchy level
   - Position: Arranged in circles at each level

2. **SKU Particles**: Small spheres around each location
   - Position: Randomly distributed on sphere surface
   - Color: Matches parent location
   - Count: Limited to 50 per location for performance

3. **Connection Lines**: Dashed lines between locations
   - Represents: Emergency replenishment paths
   - Weight: Based on number of shared SKUs
   - Color: Gray with transparency

## 📁 Files

### **Core Scripts**
- `3d_visualization_pipeline.py` - Main visualization engine
- `test_3d_viz.py` - Test script with sample data
- `requirements_3d_viz.txt` - Python dependencies

### **Generated Outputs**
- `cedarsim_3d_visualization.html` - Interactive 3D visualization
- `cedarsim_network.html` - Network graph visualization  
- `cedarsim_visualization_report.md` - Summary report

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements_3d_viz.txt
```

### **2. Run Test (Recommended First)**
```bash
python test_3d_viz.py
```

### **3. Run Full Pipeline**
```bash
python 3d_visualization_pipeline.py
```

### **4. View Results**
Open the generated HTML files in your web browser:
- `cedarsim_3d_visualization.html` - Main 3D visualization
- `cedarsim_network.html` - Network graph view

## 🎮 Interactive Features

### **3D Navigation**
- **Rotate**: Click and drag to rotate the view
- **Zoom**: Mouse wheel or pinch to zoom
- **Pan**: Right-click and drag to pan
- **Reset**: Double-click to reset view

### **Hover Information**
- **Locations**: Name, SKU count, coordinates
- **SKUs**: Location and basic info
- **Connections**: SKU ID and connection details

### **Legend and Controls**
- **Color Coding**: Hierarchy levels
- **Size Scaling**: SKU count per location
- **Connection Visibility**: Toggle on/off

## 📊 Data Requirements

### **Input Data**
The visualization requires the processed CedarSim data:
- `data/final/CedarSim_Simulation_Ready_Data_Final.xlsx`
- Sheet 1: `01_SKU_Inventory_Final` - SKU inventory data
- Sheet 2: `02_Demand_Data_Clean` - Historical demand data
- Sheet 3: `03_Validation_Sample` - Validation SKUs

### **Location Mapping**
The system automatically maps Excel columns to 3D locations:
- `Perpetual` → Level 0 (Safety Stock)
- `Level 1 *` → Level 1 (Emergency Departments)
- `Level 2 *` → Level 2 (Surgery/Pharmacy)
- `Level 3 *` → Level 3 (Support Services)
- `Level 5-9 *` → Level 5-9 (Patient Care Units)
- `Respiratory Therapy` → Level 4 (Specialized)

## 🔧 Customization

### **Visual Properties**
```python
# Location hierarchy configuration
self.location_hierarchy = {
    'Perpetual': {'level': 0, 'color': 'red', 'size': 1000},
    'Level1': {'level': 1, 'color': 'orange', 'size': 800},
    # ... customize colors, sizes, levels
}

# SKU visualization properties
self.sku_properties = {
    'size_scale': 0.1,        # SKU particle size
    'opacity': 0.7,           # Transparency
    'color_by': 'inventory_level'  # Color coding method
}
```

### **Performance Tuning**
- **SKU Limit**: Max 50 SKUs per location (configurable)
- **Connection Limit**: Max 100 connections (configurable)
- **Demand Sampling**: 5000 records max (configurable)

## 📈 Analysis Features

### **Location Analysis**
- SKU count per location
- Hierarchy level distribution
- Connection strength analysis

### **Network Analysis**
- Emergency replenishment patterns
- SKU sharing between locations
- Critical connection identification

### **Visual Insights**
- Inventory concentration patterns
- Location clustering by SKU type
- Emergency replenishment flow visualization

## 🐛 Troubleshooting

### **Common Issues**

1. **Missing Dependencies**
   ```bash
   pip install plotly networkx openpyxl
   ```

2. **Data File Not Found**
   - Ensure `data/final/CedarSim_Simulation_Ready_Data_Final.xlsx` exists
   - Run the main data processing pipeline first

3. **Performance Issues**
   - Reduce SKU limit in `sku_properties`
   - Limit connection count in `calculate_connections()`
   - Use smaller demand data sample

4. **Visualization Not Loading**
   - Check browser console for JavaScript errors
   - Ensure all dependencies are installed
   - Try different browser (Chrome recommended)

### **Debug Mode**
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔮 Future Enhancements

### **Planned Features**
- **Real-time Updates**: Live inventory level updates
- **Animation**: Time-series visualization of inventory changes
- **Filtering**: Filter by SKU type, location, or hierarchy level
- **Export**: Save visualizations as images or videos
- **VR Support**: Virtual reality visualization mode

### **Advanced Analytics**
- **Stockout Visualization**: Highlight locations with low inventory
- **Demand Flow**: Animated demand patterns
- **Optimization Suggestions**: Visual recommendations
- **Performance Metrics**: Overlay KPIs on visualization

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the test script output
3. Check the generated report for data insights
4. Refer to the main CedarSim documentation

---

*Last Updated: September 11, 2025*  
*Status: Ready for Production Use*
