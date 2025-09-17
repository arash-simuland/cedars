# CedarSim Input Data Schema

## 📊 **Data Schema Overview**

This document defines the schema and relationships between the primary input data tables for the CedarSim simulation system.

## 🗂️ **Primary Tables**

### 1. **SKU_INVENTORY_DATA** (Master SKU Table)
**File**: `SIMULATION_READY_SKU_INVENTORY_DATA.xlsx`  
**Records**: 4,776 (includes 574 duplicates)  
**Unique SKU-Location Combinations**: 4,202  
**Unique SKUs**: 2,813  

| Column Name | Data Type | Description | Constraints |
|-------------|-----------|-------------|-------------|
| `Oracle Item Number` | VARCHAR(6) | Primary SKU identifier | NOT NULL, Zero-padded format (e.g., '000005') |
| `Item Description` | VARCHAR(255) | Human-readable SKU description | NOT NULL |
| `unit_of_measure` | VARCHAR(10) | Unit of measurement (e.g., 'Each') | NOT NULL |
| `Deliver To` | VARCHAR(50) | Target location for delivery | NOT NULL, References LOCATIONS table |
| `lead_time` | DECIMAL(3,1) | Average lead time in days | NOT NULL, Range: 0.5-365 |
| `burn_rate` | DECIMAL(8,2) | Average daily consumption rate | NOT NULL, Range: 0.01-1000 |
| `Stock Units Analytical` | DECIMAL(8,2) | Pre-calculated safety stock | NULLABLE, Used for validation |

**Primary Key**: (`Oracle Item Number`, `Deliver To`)  
**Indexes**: 
- `idx_sku_number` on `Oracle Item Number`
- `idx_deliver_to` on `Deliver To`

### 2. **DEMAND_DATA** (Historical Demand Time Series)
**File**: `SIMULATION_READY_DEMAND_DATA.csv`  
**Records**: 74,511  
**Time Range**: 2019-12-15 to 2025-07-06  

| Column Name | Data Type | Description | Constraints |
|-------------|-----------|-------------|-------------|
| `PO Week Ending Date` | DATE | Demand date (week ending) | NOT NULL |
| `Business Unit` | VARCHAR(20) | Business unit identifier | NOT NULL |
| `Department Name` | VARCHAR(100) | Department name | NOT NULL |
| `Department Number` | INTEGER | Department identifier | NOT NULL |
| `Deliver to Location` | VARCHAR(50) | Consumption location | NOT NULL, References LOCATIONS table |
| `Oracle Item Number` | VARCHAR(6) | SKU identifier | NOT NULL, References SKU_INVENTORY_DATA |
| `Item Description` | VARCHAR(255) | SKU description | NOT NULL |
| `UOM` | VARCHAR(10) | Unit of measurement | NOT NULL |
| `Supplier Name` | VARCHAR(100) | Supplier name | NOT NULL |
| `Avg_Lead Time` | DECIMAL(3,1) | Lead time for this period | NOT NULL |
| `Total Qty PO` | DECIMAL(10,2) | Total quantity ordered | NOT NULL, Range: 0-999999 |
| `Total Qty Issues` | DECIMAL(10,2) | Total quantity consumed | NOT NULL, Range: 0-999999 |
| `Total Quantity` | DECIMAL(10,2) | Total quantity available | NOT NULL |
| `Avg Daily Burn Rate` | DECIMAL(8,2) | Daily consumption rate | NOT NULL |
| `Medline item? Y/N` | CHAR(1) | Medline supplier flag | NOT NULL, Values: 'Y' or 'N' |
| `On-PAR or Special Request` | VARCHAR(20) | Request type | NOT NULL, Values: 'On-PAR' or 'Special Request' |

**Primary Key**: (`PO Week Ending Date`, `Oracle Item Number`, `Deliver to Location`)  
**Indexes**:
- `idx_demand_sku` on `Oracle Item Number`
- `idx_demand_location` on `Deliver to Location`
- `idx_demand_date` on `PO Week Ending Date`

### 3. **REMOVED_SKUS** (Audit Trail)
**File**: `REMOVED_SKUS_NO_DEMAND_HISTORY.csv`  
**Records**: 537 (273 unique SKUs)  

| Column Name | Data Type | Description | Constraints |
|-------------|-----------|-------------|-------------|
| `Oracle Item Number` | VARCHAR(6) | SKU identifier | NOT NULL |
| `Item Description` | VARCHAR(255) | SKU description | NOT NULL |
| `Removal Reason` | VARCHAR(100) | Reason for removal | NOT NULL, Default: 'No demand history' |
| `Original Source` | VARCHAR(100) | Source file | NOT NULL |

**Primary Key**: `Oracle Item Number`  
**Purpose**: Audit trail for data quality and filtering decisions

## 🔗 **Table Relationships**

### **Primary Relationships**

```
SKU_INVENTORY_DATA (1) ←→ (M) DEMAND_DATA
├── Oracle Item Number (FK) → Oracle Item Number (PK)
└── Deliver To (FK) → Deliver to Location (FK)

SKU_INVENTORY_DATA (1) ←→ (0..1) REMOVED_SKUS
└── Oracle Item Number (PK) → Oracle Item Number (FK)
```

### **Relationship Details**

1. **SKU_INVENTORY_DATA ↔ DEMAND_DATA**
   - **Type**: One-to-Many
   - **Join Key**: `Oracle Item Number`
   - **Additional Join**: `Deliver To` = `Deliver to Location`
   - **Cardinality**: Each SKU-Location combination can have multiple demand records
   - **Coverage**: 100% overlap (every SKU has demand data)

2. **SKU_INVENTORY_DATA ↔ REMOVED_SKUS**
   - **Type**: One-to-Zero-or-One
   - **Join Key**: `Oracle Item Number`
   - **Purpose**: Tracks which SKUs were removed from the dataset
   - **Cardinality**: Most SKUs (2,813) are NOT in REMOVED_SKUS

## 📍 **Location Reference**

### **Location Types**
- **PAR Locations**: 13 locations (Level 1 ED, Level 2 ICU, etc.)
- **Perpetual Location**: 1 location (Central Supply)
- **Total Locations**: 14 unique locations

### **Location Hierarchy**
```
Hospital System
├── Emergency Department (Level 1 ED)
├── Intensive Care Units (Level 2 ICU)
├── Medical Units (Level 3, 4, 5)
├── Surgical Units (Level 6, 7, 8)
├── Specialized Units (Level 9, 10)
└── Central Supply (Perpetual)
```

## 🔍 **Data Quality Constraints**

### **SKU Format Standardization**
- All SKUs must be 6-character zero-padded format
- Example: '5' becomes '000005'
- Ensures consistent matching between tables

### **Referential Integrity**
- Every SKU in DEMAND_DATA must exist in SKU_INVENTORY_DATA
- Every location in both tables must be valid
- No orphaned records allowed

### **Data Validation Rules**
- `lead_time` > 0
- `burn_rate` > 0
- `Total Qty Issues` >= 0
- `PO Week Ending Date` within valid range
- `Medline item? Y/N` in ('Y', 'N')

## 📊 **Data Statistics**

| Metric | SKU_INVENTORY_DATA | DEMAND_DATA | REMOVED_SKUS |
|--------|-------------------|-------------|--------------|
| **Total Records** | 4,776 | 74,511 | 537 |
| **Unique SKUs** | 2,813 | 2,813 | 273 |
| **Unique Locations** | 14 | 14 | N/A |
| **Time Range** | N/A | 2019-12-15 to 2025-07-06 | N/A |
| **Coverage** | 91.2% of original | 100% of inventory SKUs | 8.8% of original |

## 🎯 **Simulation Usage**

### **Primary Keys for Simulation**
- **SKU Selection**: Use `Oracle Item Number` from SKU_INVENTORY_DATA
- **Location Mapping**: Use `Deliver To` for inventory, `Deliver to Location` for demand
- **Time Series**: Use `PO Week Ending Date` for temporal analysis
- **Consumption Rates**: Use `burn_rate` for inventory calculations

### **Data Loading Order**
1. Load SKU_INVENTORY_DATA (master reference)
2. Load DEMAND_DATA (time series)
3. Validate referential integrity
4. Apply business rules and constraints

---

*This schema documentation is automatically generated and should be updated when data structure changes.*
