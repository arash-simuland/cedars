# CedarSim Simulation Input Data

This directory contains the input data files for the CedarSim hospital inventory management simulation.

## 📁 Input Files

### 1. **sku_inventory_data.csv**
- **Source**: `data/final/csv_complete/Complete_Input_Dataset_20250913_220808.csv`
- **Rows**: 5,941
- **Purpose**: Primary SKU inventory data for simulation
- **Key Fields**:
  - `Oracle Item Number`: Unique SKU identifier
  - `Avg Daily Burn Rate`: Daily demand rate (units/day) ✅
  - `Avg_Lead Time`: Lead time in days ✅
  - `Item Description`: Product description
  - `UOM`: Units of measure
  - `Department Name`: Department assignment
  - `Supplier Name`: Supplier information
  - **17 PAR Location Columns**: X marks indicating which PARs store each SKU

### 2. **historical_demand_data.csv**
- **Source**: `data/final/csv_complete/02_Demand_Data_Clean_Complete.csv`
- **Rows**: 74,549
- **Purpose**: Historical demand patterns for simulation
- **Key Fields**:
  - `PO Week Ending Date`: Time series data (2024)
  - `Oracle Item Number`: Links to SKU data
  - `Total Qty Issues`: Actual demand quantities
  - `Total Qty PO`: Purchase order quantities
  - `Avg Daily Burn Rate`: Daily demand rate (units/day) ✅
  - `Deliver to Location`: Delivery location
  - `Department Name`: Department context

### 3. **validation_subset_data.csv**
- **Source**: `data/final/csv_complete/Validation_Input_Subset_20250913_220808.csv`
- **Rows**: 74
- **Purpose**: Validation subset for testing simulation accuracy
- **Key Fields**:
  - All fields from sku_inventory_data.csv
  - `Z-score`: 2.05 (standard for all validation items)
  - `Safety stock_units`: Pre-calculated safety stock levels
  - **Use**: Compare simulation results with analytical solution

## 🚀 Simulation Workflow

### Phase 1: Validation Testing
1. **Start with**: `validation_subset_data.csv` (74 SKUs)
2. **Validate results** against pre-calculated safety stock
3. **Ensure accuracy** before scaling up

### Phase 2: Full Simulation
1. **Scale up to**: `sku_inventory_data.csv` (5,941 SKUs)
2. **Use demand patterns from**: `historical_demand_data.csv`
3. **Run full-scale simulation**

## ✅ Data Quality

- **Lead Time Coverage**: 100% (all SKUs have lead times)
- **PAR Mapping Coverage**: 100% (all SKUs have location mappings)
- **Unit Consistency**: Daily demand rates match daily lead times ✅
- **Data Completeness**: 100% (no missing values)
- **Validation Ready**: Pre-calculated safety stock for 74 SKUs

## 📊 Usage Example

```python
import pandas as pd

# Load simulation input data
sku_data = pd.read_csv('data/input_data/sku_inventory_data.csv')
demand_data = pd.read_csv('data/input_data/historical_demand_data.csv')
validation_data = pd.read_csv('data/input_data/validation_subset_data.csv')

print(f"SKU data: {len(sku_data):,} rows")
print(f"Demand data: {len(demand_data):,} rows")
print(f"Validation data: {len(validation_data):,} rows")
```

## 📝 Notes

- All data has been processed and cleaned
- Daily burn rates and lead times are in consistent units (days)
- Ready for immediate use in simulation
- Files are optimized for simulation performance
