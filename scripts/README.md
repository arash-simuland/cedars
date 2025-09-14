# CedarSim Scripts Directory (CLEANED)

This directory contains essential executable code for the CedarSim project. All redundant and WIP files have been moved to `archive_master/scripts_archive/`.

## 📁 Essential Scripts

### **Core Data Pipeline:**
- **`cedarsim_complete_pipeline.py`** - ✅ MAIN - Complete data processing pipeline
- **`new_excel_converter.py`** - ✅ Data conversion utility for new Excel formats
- **`validate_excel.py`** - ✅ Excel file validation utilities

### **Analysis & Utilities:**
- **`mapping_analysis_final.py`** - ✅ SKU-location mapping analysis
- **`cleanup_workspace.py`** - ✅ Workspace cleanup utilities
- **`README_Converter.md`** - ✅ Data conversion documentation

## 🗂️ **Archived Scripts**

All redundant, duplicate, and WIP scripts have been moved to:
- **`archive_master/scripts_archive/`** - Complete archive of old scripts
- **`archive_master/scripts_archive/archive/`** - 12 old analysis scripts
- **`archive_master/scripts_archive/pipeline/`** - Duplicate pipeline implementation
- **`archive_master/scripts_archive/simulation/`** - Duplicate simulation scripts
- **`archive_master/scripts_archive/utilities/`** - Redundant utility scripts

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
