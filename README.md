# CedarSim Inventory Management Simulation

## 🎯 Project Overview

CedarSim is a discrete event simulation system for hospital inventory management, designed to optimize PAR (Periodic Automatic Replenishment) inventory levels and reduce stockouts through intelligent allocation algorithms.

## 📊 Current Status: **SIMULATION DEVELOPMENT PHASE** 🚀

The CedarSim data processing pipeline is complete and we are now actively developing the discrete event simulation engine. The pre-simulation structure framework is complete and we're implementing data integration and SimPy-based simulation execution.

### Key Achievements

- ✅ **Data Pipeline**: Successfully processed 6,372 → 5,941 clean SKUs
- ✅ **Data Integration**: Integrated new Excel format with updated burn rates, lead times, UOM
- ✅ **Data Quality**: 100% complete data (no missing values or lead times)
- ✅ **PAR Mapping**: 100% coverage for all remaining SKUs
- ✅ **Validation Dataset**: 74 validation SKUs with pre-calculated safety stock levels
- ✅ **File Validation**: All input files validated, no corruption detected
- ✅ **Data Coverage Validation**: 99.5% of original demand data preserved (188/189 weeks)
- ✅ **Object Graph Design**: Defined Location and SKU object structure for simulation
- ✅ **Design Patterns**: Observer, Strategy, Factory, and Manager patterns implemented
- ✅ **Frontend Specification**: Complete dashboard design and architecture
- ✅ **Simulation Environment**: Professional development and production folder structures
- ✅ **Replenishment Flow Understanding**: Clear understanding of normal vs emergency replenishment
- ✅ **Pre-Simulation Structure**: Complete object structure and network topology framework
- ✅ **AntologyGenerator**: Pre-simulation setup tool for creating object structure
- ✅ **Bidirectional Connections**: PAR-perpetual SKU communication implemented
- ✅ **Negative Inventory Support**: Perpetual SKUs can go negative for emergency supply
- 🚧 **Data Integration**: Building CSV loading functions to populate AntologyGenerator
- 🚧 **SimPy Module**: Creating separate simulation module that uses pre-built structure

## 🚀 Quick Start

### For Simulation Implementation

1. **Development Environment**: `simulation_development/` (start here)
   - Install dependencies: `pip install -r requirements.txt`
   - Access optimized data from `input_data/` directory
   - Pre-simulation structure framework is complete
   - Build data integration and SimPy simulation execution
2. **Production Environment**: `simulation_production/` (final models)
   - Ready for production simulation runs
   - Client deliverables and reports
3. **Complete CSV Files**: `data/final/csv_complete/` (data source)
   - `Complete_Input_Dataset_20250913_220808.csv` - 5,941 SKUs with updated data
   - `Validation_Input_Subset_20250913_220808.csv` - 74 validation SKUs
   - `02_Demand_Data_Clean_Complete.csv` - Historical demand data (74,549 records)
   - `01_SKU_Inventory_Final_Complete.csv` - Updated main dataset
   - `03_Validation_Sample_Complete.csv` - Original validation data (229 SKUs)
4. **Technical Specs**: `docs/technical_specs/model.md`
5. **Current Status**: `docs/reports/MODEL_BUILDING_STATUS.md`
6. **Project Completion**: `docs/reports/CedarSim_Project_Completion_Summary.md`
7. **Input Data Guide**: `simulation_development/input_data/README.md`

### For Data Analysis

1. **Analysis Reports**: `docs/reports/`
2. **Jupyter Notebooks**: `notebooks/`
3. **Processing Scripts**: `scripts/`

### For Dashboard Frontend

1. **Frontend Specification**: `simulation_development/FRONTEND_SPECIFICATION.md`
2. **Dashboard Implementation**: `simulation_development/frontend/` (coming soon)
3. **API Integration**: Flask backend with AntologyGenerator

## 📁 Repository Structure (SIMPLIFIED)

```text
├── simulation_development/    # Development environment (start here)
│   ├── requirements.txt       # Dependencies
│   ├── core_models.py         # Pre-simulation structure framework
│   ├── input_data/            # Optimized simulation input data
│   │   ├── sku_inventory_data.csv      # 5,941 SKUs
│   │   ├── historical_demand_data.csv  # 74,549 demand records
│   │   ├── validation_subset_data.csv  # 74 validation SKUs
│   │   └── simulation_config.py        # Configuration settings
│   ├── ARCHITECTURE.md        # Two-phase architecture documentation
│   └── README.md              # Development guide
├── simulation_production/     # Production environment
│   └── README.md              # Production guide
├── data/                      # All data files
│   ├── final/csv_complete/    # Production-ready simulation data
│   │   ├── Complete_Input_Dataset_20250913_220808.csv
│   │   ├── Validation_Input_Subset_20250913_220808.csv
│   │   └── 02_Demand_Data_Clean_Complete.csv
│   ├── audit_trails/          # Data cleaning audit records
│   └── archive/original/      # Source data files only
├── docs/                      # Essential documentation
│   ├── technical_specs/       # Model and technical documentation
│   └── reports/               # Analysis and progress reports
├── scripts/                   # Essential executable code
│   ├── cedarsim_complete_pipeline.py    # Main data pipeline
│   ├── new_excel_converter.py           # Data conversion utility
│   ├── validate_excel.py                # Excel validation
│   ├── mapping_analysis_final.py        # SKU mapping analysis
│   └── cleanup_workspace.py             # Workspace cleanup
├── notebooks/                 # Jupyter notebooks
│   └── README.md              # Notebooks guide
└── archive_master/            # Archived files
    ├── old_scripts/           # Legacy scripts
    ├── pipeline_scripts/      # Pipeline scripts
    ├── simulation_scripts/    # Simulation scripts
    ├── utility_scripts/       # Utility scripts
    ├── notebooks_archive/     # WIP notebooks
    ├── data_archive/          # Backup/temp data
    └── logs_archive/          # Old log files
```

## 📋 Current Development Phase

The data processing pipeline is **COMPLETE** and the pre-simulation structure framework is **COMPLETE**. We're now implementing data integration and SimPy-based simulation execution. Current focus:

1. **Navigate to Development**: `cd simulation_development`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Access Data**: Use files from `input_data/` (optimized for simulation)
4. **Data Integration**: Build CSV loading functions to populate AntologyGenerator
5. **SimPy Module**: Create separate simulation module that uses pre-built structure
6. **SimPy Generators**: Implement SKU process generators for simulation execution
7. **Validation Testing**: Test on 74 validation SKUs before full-scale implementation

## 🏗️ Simulation Architecture

The simulation uses a **two-phase approach** with clear separation:

### **Phase 1: Pre-Simulation Structure (COMPLETE)**

- **AntologyGenerator**: Creates object structure and network topology
- **18 Location Objects**: 1 Perpetual + 17 PAR locations
- **SKU Objects**: Each SKU exists in multiple locations with inventory management logic
- **Bidirectional Connections**: Emergency replenishment paths between PAR and Perpetual locations
- **Negative Inventory Support**: Perpetual SKUs can go negative for emergency supply

### **Phase 2: Simulation Execution (IN PROGRESS)**

- **SimPy Process-Based**: Uses pre-built structure for simulation execution
- **SKU Process Generators**: Daily time-step processing for demand, inventory, and replenishment
- **Mathematical Model**: Core equations implemented within object methods
- **Observer Pattern**: Real-time inventory change notifications

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
- **Optimized Input Data**: Available in `simulation_development/input_data/` for simulation

## 🏗️ Pre-Simulation Structure Status

- **AntologyGenerator**: Complete - creates object structure and network topology
- **Core Classes**: Complete - Resource, Location, SKU with business logic
- **Bidirectional Connections**: Complete - PAR-perpetual emergency supply paths
- **Negative Inventory Support**: Complete - Perpetual SKUs can go negative
- **Data Integration**: In Progress - CSV loading functions for AntologyGenerator
- **SimPy Module**: Pending - Will run simulation on pre-built structure

## 📞 Contact

For questions about this project, refer to the documentation in the `docs/` directory or review the comprehensive reports in `docs/reports/`.

---
*Last Updated: January 2025*
*Status: Pre-Simulation Structure Complete - Data Integration & SimPy Development In Progress*
