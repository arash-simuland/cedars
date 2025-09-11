# CedarSim Inventory Management Simulation

## 🎯 Project Overview

CedarSim is a discrete event simulation system for hospital inventory management, designed to optimize PAR (Periodic Automatic Replenishment) inventory levels and reduce stockouts through intelligent allocation algorithms.

## 📊 Current Status: **SIMULATION DEVELOPMENT** 🚀

The CedarSim data processing pipeline is complete and we're now building the discrete event simulation engine using an object-oriented approach.

### Key Achievements:
- ✅ **Data Pipeline**: Successfully processed 6,372 → 5,941 clean SKUs
- ✅ **Data Quality**: 100% complete data (no missing values or lead times)
- ✅ **PAR Mapping**: 100% coverage for all remaining SKUs
- ✅ **Validation**: 75 validation SKUs preserved from original 229
- ✅ **File Validation**: All input files validated, no corruption detected
- ✅ **Object Graph Design**: Defined Location and SKU object structure for simulation
- ✅ **3D Visualization**: Interactive 3D network visualizations of hospital inventory system
- 🚧 **Simulation Engine**: Currently implementing object-oriented simulation framework

## 🚀 Quick Start

### For Simulation Implementation:
1. **Complete CSV Files**: `data/final/csv_complete/` (recommended for simulation)
   - `01_SKU_Inventory_Final_Complete.csv` - 5,941 SKUs (complete dataset)
   - `02_Demand_Data_Clean_Complete.csv` - 74,549 demand records (complete dataset)
   - `03_Validation_Sample_Complete.csv` - 229 validation SKUs
2. **Excel Summary**: `data/final/CedarSim_Simulation_Ready_Data_Final.xlsx` (5 sheets, sampled for stability)
3. **Technical Specs**: `docs/technical_specs/model.md`
4. **Project Status**: `docs/reports/completion_summary.md`

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
├── data/                    # All data files
│   ├── final/              # Production-ready simulation data
│   ├── audit_trails/       # Data cleaning audit records
│   └── archive/            # Historical and backup data
├── docs/                   # All documentation
│   ├── technical_specs/    # Model and technical documentation
│   ├── reports/            # Analysis and progress reports
│   └── deliverables/       # Final deliverable structure
├── scripts/                # Executable code
│   ├── data_processing/    # Data cleaning scripts
│   ├── analysis/           # Analysis scripts
│   └── utilities/          # Utility scripts
├── notebooks/              # Jupyter notebooks
└── logs/                   # Log files
```

## 📋 Current Development Phase

The data processing pipeline is **COMPLETE** and we're now building the **discrete event simulation engine**. Current focus:

1. **Object Graph Creation**: Implement Location, SKU, and Graph Manager classes
2. **Data Integration**: Load Excel data into object structure  
3. **Simulation Engine**: Implement daily time-step processing
4. **Mathematical Model**: Implement core equations within object methods
5. **Validation Testing**: Test on 75 validation SKUs before full-scale implementation

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
- **Demand Records**: 86,411 → 74,549 (complete clean dataset)
- **Excel Sampling**: 5,000 rows (for file stability only)
- **Data Quality**: 100% Complete
- **Simulation Ready**: ✅ YES (use CSV files for complete dataset)

## 📞 Contact

For questions about this project, refer to the documentation in the `docs/` directory or review the comprehensive reports in `docs/reports/`.

---
*Last Updated: September 11, 2025*
*Status: Ready for Simulation Implementation*
