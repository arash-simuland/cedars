# CedarSim Inventory Management Model - Understanding Document

## Project Overview
This document captures our understanding of the CedarSim inventory management simulation system for hospital inventory management. This serves as the main reference for model building and will be updated as we progress.

## Data Sources

### 1. 2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx
**Purpose**: Primary data source for inventory management simulation

**Key Tabs**:
- **01. Data (Department Rollup)**: 
  - Provides lead times for SKUs
  - Maps which SKUs are stored in which inventories
- **Full Data**: 
  - Provides historical demand data for simulation

### 2. 2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx
**Purpose**: Reference solution for validation
- Contains client's pre-calculated target inventories (analytical solution)
- Used for comparison with our simulation results

## System Architecture

### Object Graph Structure
The simulation is built on a graph of objects representing the inventory system:

#### **Location Objects (18 total)**
- **1 Perpetual Inventory** (Safety Stock): Central reserve inventory
- **17 PAR Locations** (Cycle Stocks): Department-level inventories including:
  - Level 1: Perpetual, Facilities/Biomed, EVS, ED, Imaging
  - Level 2: Pharm, Surgery/Procedures/PACU
  - Level 3: Sterile Processing, Food Service, Admin, Central Lab
  - Level 5-9: Observation, Telemetry, PCU, ICU, M/S Overflow
  - Respiratory Therapy

#### **SKU Objects**
- Each SKU is an object **inside** its location
- Each SKU carries a **current_inventory_level** variable
- Same SKU exists as multiple objects (one in perpetual + one in each PAR where stored)

#### **Graph Connections for Emergency Replenishment**
- **Perpetual SKU objects** are connected to **PAR SKU objects** of the same SKU
- These connections represent emergency replenishment paths
- When a PAR runs out of a SKU, it can draw from the perpetual SKU of the same type

#### **Object Hierarchy**
```
Perpetual_Location {
    SKU_001 { current_inventory_level: 50, lead_time: 1.0, target_level: 100 }
    SKU_002 { current_inventory_level: 30, lead_time: 0.5, target_level: 75 }
    ...
}

PAR_Level1_ED {
    SKU_001 { current_inventory_level: 25, lead_time: 1.0, target_level: 50 }
    SKU_004 { current_inventory_level: 10, lead_time: 0.5, target_level: 30 }
    ...
}
```

### Inventory Flow Logic
1. **Daily Demand**: PAR inventories face daily demand
2. **Sufficient Stock**: If PAR has enough → supplies demand → triggers replenishment order
3. **Lead Time**: Orders delivered after SKU-specific lead time
4. **PAR Stockout**: If PAR insufficient → stockout occurs
5. **Emergency Replenishment**: Follow graph edges from PAR SKU to Perpetual SKU
6. **Hospital Stockout**: Remaining unsupplied demand becomes hospital-level stockout

## Core Mathematical Model

### 1. Inventory Gap Calculation
```
Inventory Gap = MAX(0, ((depleting*DT + target_inventory) - (SKUs_in_Shipment + PAR)))
```
- **What we want**: depleting*DT + target_inventory
- **What we have**: SKUs_in_Shipment + PAR
- **Gap**: Amount needed to order

### 2. PAR Stockout Calculation
```
PAR Stockout = (demand_projection - depleting*DT/day)
```
- **Constraint**: PARs cannot go negative
- **Depleting**: Automatically bound to available PAR stock
- **Stockout**: Occurs when demand exceeds available stock

### 3. Transit Time
```
Transit time for SKU in Shipment = Lead Time
```

### 4. Perpetual Inventory Supply
```
Perpetual.supplying_PAR = SUM(PAR.PAR_stockouts[itemType,*]) * day/DT
```
- Supplies combined PAR level stockouts for each SKU at each time step

### 5. Allocation Function
```
Supplying from Perpetual = ALLOCATE(
    Perpetual.supplying_PAR[itemType]*DT/day,  # What to allocate
    PARInventory,                              # Allocation category
    PAR_stockouts[itemType,*],                 # Amount each PAR needs
    PAR_priority[itemType,*],                  # Priority (1 for all PARs)
    0                                          # Distribution spread
)
```

**ALLOCATE Function Parameters**:
1. **What to allocate**: SKUs coming from perpetual
2. **Allocation category**: PAR inventories
3. **Needs**: Amount each PAR needs (PAR Stockouts)
4. **Priority**: Given to each PAR (1 for all PARs)
5. **Distribution spread**: 0 = higher priority indices supplied first

## King's Method Implementation

### Service Level Target
- **Desired Service Level**: 98%
- **Z-score**: 2.05

### Standard Deviation Calculation
- Based on historical demand data
- Used for safety stock calculations

### Cycle Stock Calculation
- **Method**: Same equation as safety stock
- **Demand Input**: MEAN per occurrence (not daily average)
- **Rationale**: Daily average results in very low stocks due to non-normal distribution
- **King's Recommendation**: Use mean per occurrence for cycle stock equations

## Simulation Process

### Time Horizon
- **Duration**: One year of historical data
- **Focus**: Frequency of stockouts rather than accumulative volume

### Key Steps
1. **Historical Analysis**: Use historical demand data to calculate stockouts
2. **Target Implementation**: Implement client's target inventories
3. **Stockout Calculation**: Compute stockouts using target inventories
4. **Validation**: Compare results with client's analytical solution

## Data Limitations & Assumptions

### Missing Data
- **Lead Time Variability**: Data not provided (mentioned in last meeting)
- **Storage Policy**: 2-day minimum storage policy mentioned but unclear implementation

### Key Assumptions
- **Normal Distribution**: Data doesn't follow normal distribution (affects calculation method)
- **Stockout Metric**: Focus on frequency, not volume
- **Priority**: All PARs have equal priority (priority = 1)

## Model Validation Strategy

### Comparison Points
1. **Target Inventories**: Compare our calculated targets with client's analytical solution
2. **Stockout Frequency**: Validate against expected service levels
3. **Inventory Levels**: Ensure calculated levels meet 98% service level target

### Success Metrics
- **Service Level**: Achieve 98% service level (z-score 2.05)
- **Stockout Frequency**: Minimize within one-year simulation
- **Inventory Efficiency**: Balance between stockout prevention and inventory costs

## Simulation Implementation Approach

### Object-Oriented Design
The simulation will be implemented using an object-oriented approach:

#### **Core Classes**
1. **Location Class**: Represents each inventory location (perpetual + 17 PARs)
   - Properties: location_id, location_name, location_type
   - Methods: add_sku(), remove_sku(), get_sku(), update_inventory()

2. **SKU Class**: Represents each SKU within a location
   - Properties: sku_id, current_inventory_level, lead_time, target_level, demand_pattern
   - Methods: update_inventory(), check_stockout(), calculate_reorder()

3. **Graph Manager Class**: Manages connections between SKU objects
   - Properties: emergency_connections, regular_connections
   - Methods: add_connection(), find_emergency_path(), allocate_inventory()

#### **Simulation Engine**
- **Daily Time Step**: Process each day sequentially
- **Demand Processing**: Apply daily demand to each PAR location
- **Inventory Updates**: Update current_inventory_level for each SKU
- **Emergency Replenishment**: Use graph connections to transfer inventory
- **Replenishment Orders**: Trigger new orders based on inventory gaps

#### **Data Integration**
- Load SKU data from Excel files into Location and SKU objects
- Map SKU-to-location relationships from PAR mapping columns
- Initialize current_inventory_level with target levels
- Set up graph connections based on SKU presence in locations

## Next Steps for Model Development

1. **Object Graph Creation**: Implement Location, SKU, and Graph Manager classes
2. **Data Integration**: Load Excel data into object structure
3. **Simulation Engine**: Implement daily time-step processing
4. **Mathematical Model**: Implement core equations within object methods
5. **Validation Framework**: Compare results with client's analytical solution
6. **Testing**: Start with 75 validation SKUs before full-scale implementation

---
*Last Updated: [Current Date]*
*Status: Initial understanding captured from CedarSim_pipeline.docx*
