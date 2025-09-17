# CedarSim Flexible Data Loading

This directory provides flexible data loading options for different simulation scenarios.

## 🎯 Data Loading Modes

### 1. **Validation Subset Mode** (`validation_subset`)
- **SKUs**: Only 24 validation SKUs (legacy - now use production data)
- **Time Range**: 2022-01-02 to 2025-07-06
- **Purpose**: Compare simulation results against analytical solution
- **Use Case**: Testing and validation

```python
from load_simulation_data_flexible import load_simulation_data
data = load_simulation_data('validation_subset')
```

### 2. **Full Time Range Mode** (`full_time_range`)
- **SKUs**: All 2,813 SKUs (production-ready data)
- **Time Range**: 2022-01-02 to 2025-07-06 (same as validation)
- **Purpose**: Full simulation with consistent time range
- **Use Case**: Production simulation with validation-compatible time range

```python
from load_simulation_data_flexible import load_simulation_data
data = load_simulation_data('full_time_range')
```

### 3. **Complete Mode** (`complete`)
- **SKUs**: All 2,813 SKUs (production-ready data)
- **Time Range**: 2019-12-15 to 2025-07-06 (full historical)
- **Purpose**: Full-scale simulation with complete historical data
- **Use Case**: Maximum historical coverage

```python
from load_simulation_data_flexible import load_simulation_data
data = load_simulation_data('complete')
```

## 📊 Data Coverage Comparison

| Mode | SKUs | Time Range | Demand Records | Purpose |
|------|------|------------|----------------|---------|
| Validation Subset | 24 | 2022-2025 | 4,926 | Testing vs analytical |
| Full Time Range | 5,941 | 2022-2025 | 74,542 | Production simulation |
| Complete | 5,941 | 2019-2025 | 74,549 | Full historical |

## 🚀 Usage Examples

### For Testing and Validation
```python
# Load validation subset for testing
data = load_simulation_data('validation_subset')
print(f"Testing with {len(data['sku_data'])} SKUs")
print(f"Time range: {data['demand_data']['PO Week Ending Date'].min()} to {data['demand_data']['PO Week Ending Date'].max()}")
```

### For Production Simulation
```python
# Load full dataset with validation time range
data = load_simulation_data('full_time_range')
print(f"Production simulation with {len(data['sku_data'])} SKUs")
print(f"Time range: {data['demand_data']['PO Week Ending Date'].min()} to {data['demand_data']['PO Week Ending Date'].max()}")
```

### For Maximum Historical Coverage
```python
# Load complete dataset
data = load_simulation_data('complete')
print(f"Complete simulation with {len(data['sku_data'])} SKUs")
print(f"Time range: {data['demand_data']['PO Week Ending Date'].min()} to {data['demand_data']['PO Week Ending Date'].max()}")
```

## 📁 File Structure

```
simulation_development/data/input_data/
├── load_simulation_data_flexible.py    # Main flexible loader
├── load_validation_subset.py           # Validation subset loader
├── load_input_data.py                  # Original loader
├── validation_sku_subset.csv           # Validation SKU data
├── validation_demand_subset.csv        # Validation demand data
├── validation_test_data.csv            # Analytical solution data
├── sku_inventory_data.csv              # Complete SKU data
├── historical_demand_data.csv          # Complete demand data
└── validation_subset_data.csv          # Validation subset data
```

## 🔄 Workflow

1. **Start with Validation Subset**: Use `validation_subset` mode to test your simulation against the analytical solution
2. **Scale to Full Time Range**: Use `full_time_range` mode to run with all SKUs but same time range
3. **Optional Complete Mode**: Use `complete` mode if you need the full historical time range

## ⚠️ Important Notes

- **Validation Subset**: Only 8 out of 24 validation SKUs have historical demand data
- **Time Range Consistency**: Full time range mode uses the same time range as validation for fair comparison
- **Data Quality**: All modes maintain 100% lead time and burn rate coverage
- **Memory Usage**: Full time range mode uses ~58MB, validation subset uses ~3MB

## 🧪 Testing

Run the test script to verify all modes work correctly:

```bash
python simulation_development/data/input_data/load_simulation_data_flexible.py
```

This will test all three modes and show data summaries for each.
