# CedarSim Simulation Engine

This directory contains the discrete event simulation engine for CedarSim inventory management.

## 🏗️ Simulation Architecture

The simulation uses an **object-oriented approach** with a graph of objects:

### **Core Objects**
- **Location Objects**: 18 total (1 Perpetual + 17 PAR locations)
- **SKU Objects**: Each SKU exists in multiple locations with current_inventory_level
- **Graph Connections**: Emergency replenishment paths between same SKUs

### **Object Hierarchy**
```
Perpetual_Location {
    SKU_001 { current_inventory_level: 50, lead_time: 1.0, target_level: 100 }
    SKU_002 { current_inventory_level: 30, lead_time: 0.5, target_level: 75 }
    ...
}

PAR_Level1_ED {
    SKU_001 { current_inventory_level: 25, lead_time: 1.0, target_level: 50 }
    SKU_004 { current_inventory_level: 10, lead_time: 0.5, target_level: 30 }
    ...
}
```

## 📁 Planned File Structure

### **Core Classes**
- **`location.py`** - Location class implementation
- **`sku.py`** - SKU class implementation  
- **`graph_manager.py`** - Graph connections management

### **Simulation Engine**
- **`simulation_engine.py`** - Main simulation engine
- **`data_loader.py`** - Excel data integration
- **`validator.py`** - Validation against client's analytical solution

### **Utilities**
- **`config.py`** - Simulation configuration
- **`logger.py`** - Simulation logging
- **`utils.py`** - Helper functions

## 🚀 Implementation Plan

1. **Phase 1**: Create core classes (Location, SKU, Graph Manager)
2. **Phase 2**: Implement data loading from Excel files
3. **Phase 3**: Build simulation engine with daily time steps
4. **Phase 4**: Add mathematical model equations
5. **Phase 5**: Validation testing with 75 validation SKUs

## 📊 Current Status

- **Object Graph Design**: ✅ COMPLETE - Structure defined in model.md
- **Core Classes**: 🚧 IN PROGRESS - Implementing Location and SKU classes
- **Data Integration**: ⏳ PENDING - Excel data loading
- **Simulation Engine**: ⏳ PENDING - Daily time-step processing

## 📝 Notes

- All classes will be designed to work with the clean data from `data/final/`
- Simulation will start with 75 validation SKUs before full-scale implementation
- Object-oriented design ensures modularity and maintainability
