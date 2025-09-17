# CedarSim Production Input Data

## 📁 Location
**`simulation_development/data/prod-input-data/`**

This folder contains the **source of truth** input data for the CedarSim simulation system.

## 📋 Files Overview

### 1. `SIMULATION_READY_SKU_INVENTORY_DATA.xlsx` ⭐ **PRIMARY SKU DATA**
- **Purpose**: Master SKU inventory data with burn rates, lead times, and analytical safety stock
- **Records**: 4,776 records
- **Unique SKUs**: 2,813 SKUs
- **Source**: Filtered from `2025-09-12-final-list-with-results.xlsx`
- **Coverage**: 91.2% of original final list (273 SKUs removed due to no demand history)
- **Key Columns**:
  - `Oracle Item Number`: Unique SKU identifier
  - `Item Description`: SKU description
  - `burn_rate`: Average daily consumption rate
  - `lead_time`: Average lead time in days
  - `Stock Units Analytical`: Pre-calculated safety stock (for validation)
  - `Deliver To`: Target location for delivery

### 2. `SIMULATION_READY_DEMAND_DATA.csv` ⭐ **PRIMARY DEMAND DATA**
- **Purpose**: Historical demand time series data for simulation
- **Records**: 74,511 records
- **Time Range**: 2019-12-15 to 2025-07-06 (5.5+ years)
- **Source**: Filtered from `historical_demand_data.csv`
- **Coverage**: Only includes SKUs present in SKU inventory data
- **Key Columns**:
  - `PO Week Ending Date`: Demand date
  - `Oracle Item Number`: SKU identifier
  - `Total Qty Issues`: Quantity consumed
  - `Avg Daily Burn Rate`: Daily consumption rate
  - `Deliver to Location`: Consumption location

### 3. `REMOVED_SKUS_NO_DEMAND_HISTORY.csv` 📝 **DOCUMENTATION**
- **Purpose**: Record of SKUs removed due to lack of historical demand data
- **Records**: 537 records (273 unique SKUs)
- **Reason**: No corresponding demand data found in historical dataset
- **Use**: Documentation and audit trail

### 4. `DATA_FILTERING_SUMMARY.txt` 📊 **SUMMARY REPORT**
- **Purpose**: Detailed summary of data filtering process
- **Contains**: Statistics, coverage percentages, file descriptions
- **Date**: 2025-09-17 13:16:43

## 🔄 Data Processing History

### Original Data Sources:
- **Source of Truth**: `2025-09-12-final-list-with-results.xlsx` (3,086 unique SKUs)
- **Historical Demand**: `historical_demand_data.csv` (2,840 unique SKUs)

### Filtering Process:
1. **SKU Normalization**: Removed leading zeros for proper matching
2. **Overlap Analysis**: Found 2,813 SKUs with both inventory and demand data
3. **Data Filtering**: Removed 273 SKUs without demand history
4. **Coverage Achieved**: 91.2% of original final list

### Quality Checks:
- ✅ All SKUs in inventory data have corresponding demand data
- ✅ All demand records correspond to SKUs in inventory data
- ✅ No orphaned data or unused records
- ✅ Proper SKU normalization applied

## 🎯 Simulation Usage

### For SKU Inventory:
```python
import pandas as pd
sku_data = pd.read_excel('simulation_development/data/prod-input-data/SIMULATION_READY_SKU_INVENTORY_DATA.xlsx')
```

### For Demand Data:
```python
import pandas as pd
demand_data = pd.read_csv('simulation_development/data/prod-input-data/SIMULATION_READY_DEMAND_DATA.csv')
```

### For Validation:
```python
# Use 'Stock Units Analytical' column for validation against simulation results
validation_data = sku_data[['Oracle Item Number', 'Stock Units Analytical']].dropna()
```

## 📈 Data Statistics

| Metric | Value |
|--------|-------|
| **Total SKUs** | 2,813 |
| **Inventory Records** | 4,776 |
| **Demand Records** | 74,511 |
| **Time Range** | 2019-12-15 to 2025-07-06 |
| **Coverage** | 91.2% |
| **Removed SKUs** | 273 (8.8%) |

## ⚠️ Important Notes

1. **Source of Truth**: These files represent the definitive input data for simulation
2. **No Missing Data**: Every SKU has both inventory and demand data
3. **Normalized SKUs**: Leading zeros removed for proper matching
4. **Audit Trail**: Complete record of what was removed and why
5. **Ready for Production**: Data is clean and simulation-ready

## 🔧 Maintenance

- **Last Updated**: 2025-09-17
- **Filtering Script**: `scripts/filter_final_list_to_demand_coverage.py`
- **Original Sources**: Archived in `data/archive/` and `simulation_development/data/archive-input_data/`

---
*This documentation is automatically generated and should be updated when data changes.*
