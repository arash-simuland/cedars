# CedarSim Data Directory

This directory contains all data files organized by purpose and status.

## 📁 Directory Structure

### `final/`
**Production-ready data files:**
- **`CedarSim_Simulation_Ready_Data_Final.xlsx`** - Main simulation dataset (5,941 clean SKUs)

### `audit_trails/`
**Data cleaning audit records:**
- **`phase1_missing_lead_times_removal.csv`** - 298 SKUs removed for missing lead times
- **`phase2_unmapped_skus_removal.csv`** - 133 SKUs removed for no PAR mapping

### `archive/`
**Historical and backup data:**
- **`original/`** - Source data files from client
- **`wip_artifacts/`** - Work-in-progress files and temporary artifacts
- **`pipeline_backups/`** - Pipeline execution backup files

## 📊 Data Summary

- **Final Dataset**: 5,941 clean SKUs with complete lead times and PAR mapping
- **Data Quality**: 100% complete (no missing values)
- **Validation Sample**: 74 SKUs with pre-calculated safety stock levels
- **Audit Trail**: Complete removal records for both cleaning phases
- **Pipeline Status**: ✅ COMPLETE - Ready for simulation
- **Testing Status**: ✅ VALIDATED - All data loading mechanisms tested and working

## 🧪 **Data Validation Results**

### **Comprehensive Testing Completed**
All data components have been thoroughly tested and validated:

- **Data Loading Tests**: 5/5 passed
  - SKU inventory data: 5,941 SKUs loaded successfully
  - Historical demand data: 74,549 records processed
  - Validation subset: 74 SKUs with safety stock levels
  - Data quality: 100% lead time and burn rate coverage
  - Configuration: All parameters loaded correctly

- **Data Integration Tests**: 5/5 passed
  - AntologyGenerator: Successfully created with real data
  - Location structure: 19 locations (18 PARs + 1 Perpetual)
  - SKU distribution: Properly distributed across locations
  - Network connections: Emergency supply chain established
  - Object relationships: All connections working

### **Test Coverage**
- **Data Quality**: 100% lead time and burn rate coverage
- **Data Integration**: Seamless CSV → AntologyGenerator pipeline
- **Memory Usage**: ~58.2 MB total data size
- **Time Range**: 2019-12-15 to 2025-07-06 (5+ years of data)
- **Validation Ready**: 74 SKUs with pre-calculated safety stock for testing

## 🚀 Usage

- **For Simulation**: Use `final/CedarSim_Simulation_Ready_Data_Final.xlsx`
- **For Analysis**: Review audit trails in `audit_trails/`
- **For Reference**: Check original data in `archive/original/`

## 📝 Data Processing

The data has been processed through two main phases:
1. **Phase 1**: Removed 298 SKUs with missing lead times
2. **Phase 2**: Removed 133 SKUs with no PAR location mapping

All processing decisions and impacts are documented in the audit trail files.
