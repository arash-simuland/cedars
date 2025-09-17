# CedarSim Data and Model Loading Explanation

**Date**: September 17, 2025  
**Purpose**: Comprehensive explanation of input data structure and model loading process

## 📊 **INPUT DATA OVERVIEW**

### **1. SKU Inventory Data** - `SIMULATION_READY_SKU_INVENTORY_DATA.xlsx`

**What it contains**: Master inventory data for all medical supplies (SKUs) across hospital locations

| **Metric** | **Value** | **Description** |
|------------|-----------|-----------------|
| **Total Records** | 4,776 | SKU-location combinations (includes duplicates) |
| **Unique SKUs** | 2,813 | Different medical supply items |
| **Unique Locations** | 14 | Hospital departments/areas |
| **Data Format** | Excel (.xlsx) | Structured inventory data |

**Key Columns**:
- `Oracle Item Number`: Unique 6-digit SKU identifier (e.g., '000005')
- `Item Description`: Human-readable product name
- `unit_of_measure`: Unit type (e.g., 'Each', 'Box', 'Case')
- `Deliver To`: Target hospital location
- `lead_time`: Average supply chain delay (days)
- `burn_rate`: Daily consumption rate (units/day)
- `Stock Units Analytical`: Pre-calculated safety stock for validation

**Sample Data**:
```
Oracle Item Number: 000005
Item Description: Pitcher Graduated Triangular Disposable 32oz
unit_of_measure: Each
Deliver To: Level 1 ED
lead_time: 0.5 days
burn_rate: 10.0 units/day
Stock Units Analytical: 10.0 units
```

### **2. Demand Data** - `SIMULATION_READY_DEMAND_DATA.csv`

**What it contains**: Historical consumption patterns over time

| **Metric** | **Value** | **Description** |
|------------|-----------|-----------------|
| **Total Records** | 74,511 | Historical demand events |
| **Unique SKUs** | 2,814 | SKUs with demand history |
| **Time Range** | 2019-12-15 to 2025-07-06 | 5.5+ years of data |
| **Unique Locations** | 36 | Consumption locations |
| **Data Format** | CSV | Time series data |

**Key Columns**:
- `PO Week Ending Date`: Demand date (week ending)
- `Oracle Item Number`: SKU identifier
- `Deliver to Location`: Where consumption occurred
- `Total Qty Issues`: Actual quantity consumed
- `Avg Daily Burn Rate`: Daily consumption rate
- `Total Qty PO`: Quantity ordered
- `Supplier Name`: Supply source

**Sample Data**:
```
PO Week Ending Date: 2024-01-07
Oracle Item Number: 000005
Deliver to Location: MDRCS
Total Qty Issues: 0 (no consumption this week)
Avg Daily Burn Rate: 9.1 units/day
Total Qty PO: 70.0 units
```

### **3. Removed SKUs** - `REMOVED_SKUS_NO_DEMAND_HISTORY.csv`

**What it contains**: Audit trail of SKUs removed due to missing demand data

| **Metric** | **Value** | **Description** |
|------------|-----------|-----------------|
| **Total Records** | 537 | Removed SKU-location combinations |
| **Unique SKUs** | 273 | SKUs without demand history |
| **Purpose** | Documentation | Data quality audit trail |

## 🏥 **HOSPITAL LOCATION STRUCTURE**

### **14 Primary Locations**:

1. **Level 1 ED** - Emergency Department
2. **Level 1 EVS_1321** - Environmental Services
3. **Level 1 Imaging** - Radiology/Imaging
4. **Level 2 Pharm** - Pharmacy
5. **Level 2 Surgery/Procedures/PACU** - Surgical Services
6. **Level 3 Admin** - Administration
7. **Level 3 Central Lab** - Laboratory Services
8. **Level 3 Food Service** - Nutrition Services
9. **Level 3 Sterile Processing_3307_3309** - Sterile Processing
10. **Level 5 Observation, Medical Tele & Non-Tele** - Medical Units
11. **Level 6 Telemetry, Cardiac & Stroke** - Cardiac Care
12. **Level 7 ICU** - Intensive Care Unit
13. **Perpetual** - Central Warehouse
14. **Respiratory Therapy** - Respiratory Services

### **Location Types**:
- **PAR Locations** (13): Patient care areas with limited inventory
- **Perpetual Location** (1): Central warehouse with unlimited capacity

## 🔄 **DATA LOADING PROCESS**

### **Step 1: Data Integration Module** (`data_integration.py`)

```python
from data.input_data.data_integration import create_integrated_antology

# Load and integrate all data
antology, integrator = create_integrated_antology(use_validation_subset=False)
```

**What happens**:
1. **Load SKU Data**: Reads Excel file with inventory information
2. **Load Demand Data**: Reads CSV file with historical consumption
3. **Create Validation Subset**: Filters SKUs with analytical safety stock
4. **Map Column Names**: Converts old format to new format automatically
5. **Validate Data Quality**: Ensures 100% SKU coverage between datasets

### **Step 2: AntologyGenerator Structure Creation**

**Location Creation**:
```python
# Creates 22 total locations (14 from data + 8 standard)
for location_name in all_locations:
    if "Perpetual" in location_name:
        location_type = "PERPETUAL"
    else:
        location_type = "PAR"
    
    location = ResourceFactory.create_location(location_name, location_type)
    antology.add_location(location)
```

**SKU Creation**:
```python
# Creates SKU instances for each inventory record
for _, row in sku_data.iterrows():
    sku = ResourceFactory.create_sku(
        sku_id=row['Oracle Item Number'],
        location_id=row['Deliver To'],
        target_level=row['Stock Units Analytical'],  # Uses existing validation data
        lead_time_days=row['lead_time'],
        demand_rate=row['burn_rate']
    )
    antology.add_sku(sku)
```

### **Step 3: Network Topology Generation**

**Emergency Supply Chain**:
```python
# Creates bidirectional connections between PARs and Perpetual
antology.generate_network_connections()
antology.finalize_network()
```

**Network Structure**:
- **PAR-to-Perpetual**: Emergency replenishment when PAR runs out
- **Perpetual-to-PAR**: Regular replenishment orders
- **Bidirectional**: Allows emergency supply in both directions

## 🎯 **MODEL LOADING RESULTS**

### **Final Simulation Structure**:

| **Component** | **Count** | **Description** |
|---------------|-----------|-----------------|
| **Locations** | 22 | Hospital departments + warehouse |
| **SKU Instances** | 4,776 | Individual SKU-location combinations |
| **Unique SKUs** | 2,813 | Different medical supply types |
| **Network Connections** | 26 | Emergency supply chain links |
| **Validation SKUs** | 4,775 | SKUs with analytical safety stock |

### **Data Quality Metrics**:

✅ **100% SKU Coverage**: Every SKU has both inventory and demand data  
✅ **Perfect Data Match**: 2,813 SKUs overlap between datasets  
✅ **Complete Validation**: 4,775 SKUs have analytical safety stock  
✅ **No Missing Data**: All critical parameters populated  
✅ **Normalized Format**: All SKUs in 6-digit zero-padded format  

## 🔧 **HOW THE MODEL USES THE DATA**

### **1. Inventory Management**:
- **Current Level**: Tracks real-time inventory at each location
- **Target Level**: Uses `Stock Units Analytical` for safety stock
- **Reorder Point**: Calculated from lead time and demand rate
- **Emergency Supply**: PARs can request from Perpetual when stockout

### **2. Demand Simulation**:
- **Historical Patterns**: Uses 5.5+ years of demand data
- **Burn Rates**: Daily consumption from `burn_rate` column
- **Location-Specific**: Demand varies by hospital department
- **Time Series**: Weekly demand events from historical data

### **3. Supply Chain Logic**:
- **Lead Times**: Supply delays from `lead_time` column
- **Order Processing**: Weekly order cycles
- **Emergency Replenishment**: PAR-to-Perpetual emergency supply
- **Network Topology**: Bidirectional connections for flexibility

### **4. Validation Framework**:
- **Analytical Comparison**: Simulation results vs. `Stock Units Analytical`
- **Accuracy Metrics**: Measures simulation precision
- **Service Level**: Target 98% service level with 2.05 Z-score
- **Stockout Tracking**: Records when entire system is under stress

## 📈 **DATA FLOW DIAGRAM**

```
INPUT DATA FILES
├── SIMULATION_READY_SKU_INVENTORY_DATA.xlsx
│   ├── 2,813 unique SKUs
│   ├── 4,776 SKU-location combinations
│   └── Analytical safety stock values
├── SIMULATION_READY_DEMAND_DATA.csv
│   ├── 74,511 historical records
│   ├── 5.5+ years of data
│   └── Time series consumption patterns
└── REMOVED_SKUS_NO_DEMAND_HISTORY.csv
    └── 273 removed SKUs (audit trail)

    ↓ DATA INTEGRATION MODULE

ANTOLOGYGENERATOR STRUCTURE
├── 22 Locations (14 PAR + 1 Perpetual + 7 additional)
├── 4,776 SKU Instances
├── Network Topology (26 connections)
└── Validation Framework (4,775 SKUs)

    ↓ SIMULATION INITIALIZATION

READY FOR SIMPY SIMULATION
├── Pre-built object structure
├── Network connections established
├── Data validation complete
└── Ready for discrete event simulation
```

## ✅ **SUMMARY**

Your simulation model now has access to:

1. **Complete Inventory Data**: 2,813 SKUs across 14 hospital locations
2. **Historical Demand Patterns**: 5.5+ years of consumption data
3. **Validation Framework**: Pre-calculated analytical safety stock
4. **Network Topology**: Emergency supply chain connections
5. **Data Quality**: 100% coverage with no missing critical parameters

The model is **ready for simulation initialization** and can properly handle the presimulation phase with all the data it needs to create a realistic hospital inventory management simulation.

---

*This explanation documents the complete data structure and loading process for the CedarSim simulation system.*
