# CedarSim Scripts Directory

This directory contains all executable code organized by purpose.

## 📁 Directory Structure

### `data_processing/`
**Data cleaning and preparation scripts:**
- **`cedarsim_complete_pipeline.py`** - Complete data processing pipeline
- **`robust_data_cleaning.py`** - Robust data cleaning implementation
- **`improved_excel_creation.py`** - Excel file creation utilities
- **`validate_excel.py`** - Excel validation utilities
- **`fix_excel.py`** - Excel file repair utilities
- **`check_*.py`** - Various data checking utilities

### `analysis/`
**Analysis and exploration scripts:**
- **`mapping_analysis_final.py`** - SKU-location mapping analysis
- **`complete_analysis.py`** - Complete data analysis
- **`detailed_sku_analysis.py`** - Detailed SKU analysis
- **`run_analysis.py`** - Analysis execution script
- **`run_pre_removal_analysis.py`** - Pre-removal analysis

### `utilities/`
**Utility and helper scripts:**
- **`cleanup_workspace.py`** - Workspace cleanup utilities
- **`compare_results.py`** - Results comparison utilities
- **`examine_columns.py`** - Column examination utilities
- **`find_missing_sku.py`** - Missing SKU detection

## 🚀 Usage

### For Data Processing:
```bash
cd scripts/data_processing
python cedarsim_complete_pipeline.py
```

### For Analysis:
```bash
cd scripts/analysis
python mapping_analysis_final.py
```

### For Utilities:
```bash
cd scripts/utilities
python cleanup_workspace.py
```

## 📝 Notes

- All scripts are designed to work with the data in the `data/` directory
- Scripts maintain compatibility with the organized data structure
- Check individual script documentation for specific usage instructions
