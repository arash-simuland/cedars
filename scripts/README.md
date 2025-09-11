# CedarSim Scripts Directory

This directory contains all executable code organized by purpose.

## 📁 Directory Structure

### `data_processing/`
**Production data processing scripts:**
- **`cedarsim_complete_pipeline.py`** - ✅ COMPLETE - Data processing pipeline
- **`validate_excel.py`** - Excel validation utilities
- **`cleanup_workspace.py`** - Workspace cleanup utilities

### `simulation/` (Coming Soon)
**Simulation engine development:**
- **`location.py`** - Location class implementation
- **`sku.py`** - SKU class implementation  
- **`graph_manager.py`** - Graph connections management
- **`simulation_engine.py`** - Main simulation engine
- **`data_loader.py`** - Excel data integration

### `analysis/`
**Analysis and exploration scripts:**
- **`mapping_analysis_final.py`** - SKU-location mapping analysis
- **`cedarsim_complete_pipeline.py`** - Complete analysis pipeline

### `archive/`
**Archived development scripts:**
- All temporary analysis, testing, and development scripts have been moved here
- Includes: robust_data_cleaning.py, improved_excel_creation.py, fix_excel.py, and others

## 🚀 Usage

### For Data Processing (MAIN PIPELINE):
```bash
cd scripts/data_processing
python cedarsim_complete_pipeline.py
```

### For Analysis:
```bash
cd scripts/analysis
python mapping_analysis_final.py
```

## ✅ Project Status
- **Data Processing**: ✅ COMPLETE - 5,941 clean SKUs ready for simulation
- **File Validation**: ✅ COMPLETE - All files validated, no corruption
- **Object Graph Design**: ✅ COMPLETE - Location and SKU object structure defined
- **Simulation Engine**: 🚧 IN PROGRESS - Implementing object-oriented framework

## 📝 Notes

- All scripts are designed to work with the data in the `data/` directory
- Scripts maintain compatibility with the organized data structure
- Check individual script documentation for specific usage instructions
