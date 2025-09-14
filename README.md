# CedarSim Inventory Management Simulation

## 🎯 Project Overview

CedarSim is a discrete event simulation system for hospital inventory management, designed to optimize PAR (Periodic Automatic Replenishment) inventory levels and reduce stockouts through intelligent allocation algorithms.

## 📊 Current Status: **SIMULATION DEVELOPMENT READY** 🚀

The CedarSim data processing pipeline is complete with integrated new data and we're ready to build the discrete event simulation engine using an object-oriented approach.

### Key Achievements:
- ✅ **Data Pipeline**: Successfully processed 6,372 → 5,941 clean SKUs
- ✅ **Data Integration**: Integrated new Excel format with updated burn rates, lead times, UOM
- ✅ **Data Quality**: 100% complete data (no missing values or lead times)
- ✅ **PAR Mapping**: 100% coverage for all remaining SKUs
- ✅ **Validation Dataset**: 74 validation SKUs with pre-calculated safety stock levels
- ✅ **File Validation**: All input files validated, no corruption detected
- ✅ **Object Graph Design**: Defined Location and SKU object structure for simulation
- ✅ **3D Visualization**: Interactive 3D network visualizations of hospital inventory system
- ✅ **Simulation Environment**: Professional development and production folder structures
- 🚧 **Simulation Engine**: Ready to implement object-oriented simulation framework

## 🚀 Quick Start

### For Simulation Implementation:
1. **Development Environment**: `simulation_development/` (start here)
   - Complete input dataset with updated data
   - Validation subset for testing (74 SKUs)
   - Professional development folder structure
   - Requirements and documentation
2. **Production Environment**: `simulation_production/` (final models)
   - Ready for production simulation runs
   - Client deliverables and reports
3. **Complete CSV Files**: `data/final/csv_complete/` (data source)
   - `Complete_Input_Dataset_20250913_220808.csv` - 5,941 SKUs with updated data
   - `Validation_Input_Subset_20250913_220808.csv` - 74 validation SKUs
   - `02_Demand_Data_Clean_Complete.csv` - Historical demand data
4. **Technical Specs**: `docs/technical_specs/model.md`
5. **Project Status**: `docs/reports/completion_summary.md`

### For Data Analysis:
1. **Analysis Reports**: `docs/reports/`
2. **Jupyter Notebooks**: `notebooks/`
3. **Processing Scripts**: `scripts/`

### For 3D Visualization:
1. **Visualization Script**: `scripts/simulation/cedarsim_3d_viz.py`
2. **Generated HTML Files**: `scripts/simulation/cedarsim_combined_visualization.html`
3. **Documentation**: `scripts/simulation/README_3D_VISUALIZATION.md`

## 📁 Repository Structure

```
├── simulation_development/ # Development environment (start here)
│   ├── data/              # Development datasets
│   ├── models/            # Simulation model classes
│   ├── scripts/           # Development scripts
│   ├── notebooks/         # Jupyter notebooks
│   ├── reports/           # Development reports
│   └── logs/              # Development logs
├── simulation_production/  # Production environment
│   ├── data/              # Production datasets
│   ├── models/            # Production model classes
│   ├── scripts/           # Production scripts
│   ├── reports/           # Client deliverables
│   └── config/            # Configuration files
├── data/                  # All data files
│   ├── final/             # Production-ready simulation data
│   ├── converted/         # Data conversion outputs
│   ├── audit_trails/      # Data cleaning audit records
│   └── archive/           # Historical and backup data
├── docs/                  # All documentation
│   ├── technical_specs/   # Model and technical documentation
│   ├── reports/           # Analysis and progress reports
│   └── deliverables/      # Final deliverable structure
├── scripts/               # Executable code
│   ├── data_processing/   # Data cleaning and conversion scripts
│   ├── analysis/          # Analysis scripts
│   └── utilities/         # Utility scripts
├── notebooks/             # Jupyter notebooks
└── logs/                  # Log files
```

## 📋 Current Development Phase

The data processing pipeline is **COMPLETE** with integrated new data and we're ready to build the **discrete event simulation engine**. Current focus:

1. **Navigate to Development**: `cd simulation_development`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Object Graph Creation**: Implement Location, SKU, and Graph Manager classes
4. **Data Integration**: Load complete dataset into object structure  
5. **Simulation Engine**: Implement daily time-step processing
6. **Mathematical Model**: Implement core equations within object methods
7. **Validation Testing**: Test on 74 validation SKUs before full-scale implementation

## 🏗️ Simulation Architecture

The simulation uses an **object-oriented approach** with:

- **18 Location Objects**: 1 Perpetual + 17 PAR locations
- **SKU Objects**: Each SKU exists in multiple locations with current_inventory_level
- **Graph Connections**: Emergency replenishment paths between same SKUs in different locations
- **Daily Time Steps**: Process demand, update inventory, handle stockouts and replenishment

## 📊 Final Pipeline Results

- **Original SKUs**: 6,372
- **Phase 1 Removed**: 298 (missing lead times)
- **Phase 2 Removed**: 133 (no PAR mapping)  
- **Final Clean SKUs**: 5,941
- **Items Updated**: 2,883 (with new burn rates, lead times, UOM)
- **Validation SKUs**: 74 (with pre-calculated safety stock levels)
- **Demand Records**: 85,603 (complete clean dataset)
- **Data Quality**: 100% Complete
- **Simulation Ready**: ✅ YES (use development environment)

## 🔄 Data Integration Results

- **New Data Format**: Successfully integrated 2025-09-12_MDRH_Item_List.xlsx
- **Updated Fields**: Burn rates, lead times, UOM from new data
- **Preserved Context**: All departments, suppliers, PAR mappings maintained
- **Validation Ready**: 74 SKUs with pre-calculated safety stock for testing
- **Complete Dataset**: Ready for full simulation (5,941 SKUs)

## 📞 Contact

For questions about this project, refer to the documentation in the `docs/` directory or review the comprehensive reports in `docs/reports/`.

---
*Last Updated: September 13, 2025*
*Status: Data Integration Complete - Ready for Simulation Development*
