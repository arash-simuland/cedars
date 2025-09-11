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
- **`interim/`** - Intermediate processing files
- **`backups/`** - Various backup files from processing

## 📊 Data Summary

- **Final Dataset**: 5,941 clean SKUs with complete lead times and PAR mapping
- **Data Quality**: 100% complete (no missing values)
- **Validation Sample**: 229 SKUs preserved for validation
- **Audit Trail**: Complete removal records for both cleaning phases

## 🚀 Usage

- **For Simulation**: Use `final/CedarSim_Simulation_Ready_Data_Final.xlsx`
- **For Analysis**: Review audit trails in `audit_trails/`
- **For Reference**: Check original data in `archive/original/`

## 📝 Data Processing

The data has been processed through two main phases:
1. **Phase 1**: Removed 298 SKUs with missing lead times
2. **Phase 2**: Removed 133 SKUs with no PAR location mapping

All processing decisions and impacts are documented in the audit trail files.
