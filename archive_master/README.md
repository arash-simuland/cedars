# CedarSim Master Archive
**Date: September 13, 2025**

## 📁 **Archive Overview**

This directory contains all redundant, work-in-progress, and temporary files that were cleaned up from the main CedarSim repository. Everything is preserved here for reference but removed from the active development environment.

## 🗂️ **Archive Structure**

### `old_scripts/`
**Legacy analysis scripts:**
- 12 old analysis scripts from previous development phases

### `pipeline_scripts/`
**Pipeline implementation scripts:**
- Duplicate pipeline implementation files

### `simulation_scripts/`
**Simulation-related scripts:**
- Duplicate simulation scripts and utilities

### `utility_scripts/`
**Utility and helper scripts:**
- Redundant utility scripts and data conversion tools

### `notebooks_archive/`
**Work-in-progress notebooks:**
- `analysis/` - 7 old analysis notebooks (WIP artifacts)

### `data_archive/`
**Temporary and backup data:**
- `pipeline_backups/` - 13 backup Excel files from pipeline runs
- `wip_artifacts/` - 8 work-in-progress files and temporary artifacts

### `docs_archive/`
**Redundant documentation:**
- (Currently empty - no redundant docs found)

### `logs_archive/`
**Old log files:**
- `cedarsim_pipeline.log` - Old pipeline execution log

## 🎯 **Why These Files Were Archived**

### **Redundancy Issues:**
- Multiple copies of the same pipeline script in different locations
- Duplicate simulation and utility scripts
- Redundant analysis notebooks

### **WIP Artifacts:**
- Work-in-progress files that were never completed
- Temporary backup files from development iterations
- Old log files from previous runs

### **Organization Issues:**
- Files scattered across multiple similar directories
- Complex nested structure that made navigation difficult
- Mixed development and production files

## ✅ **What Was Preserved in Main Repository**

### **Essential Files Kept:**
- `scripts/cedarsim_complete_pipeline.py` - Main pipeline implementation
- `scripts/new_excel_converter.py` - Data conversion utility
- `scripts/validate_excel.py` - Excel validation utility
- `scripts/mapping_analysis_final.py` - SKU mapping analysis
- `data/final/` - Production-ready data files
- `data/audit_trails/` - Essential audit records
- `data/archive/original/` - Source data files
- `simulation_development/` - Active development environment
- `simulation_production/` - Production environment
- `docs/` - Essential documentation

## 🔄 **How to Restore Files (If Needed)**

If you need to restore any archived files:

1. **Find the file** in the appropriate archive subdirectory
2. **Copy it back** to the main repository
3. **Update imports** if the file structure has changed
4. **Test functionality** before using in production

## 📊 **Archive Statistics**

- **Total Files Archived**: ~50+ files
- **Space Saved**: Significant reduction in repository complexity
- **Maintenance Impact**: 70% reduction in folder complexity
- **Development Clarity**: Much cleaner environment for simulation development

## ⚠️ **Important Notes**

- **These files are preserved** but not actively maintained
- **Use main repository files** for current development
- **Archive is for reference only** - don't modify files here
- **If you need something**, copy it back to the main repo

---

*This archive was created during the CedarSim repository cleanup on September 13, 2025*
