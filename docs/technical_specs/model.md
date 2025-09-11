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

### Inventory Structure
- **1 Safety Stock** (Perpetual Inventory): Central reserve inventory
- **17 Cycle Stocks** (PARs - Periodic Automatic Replenishment): Department-level inventories
- **Independent Replenishment**: Each inventory replenishes independently
- **Stockout Coverage**: If PAR level stockout occurs, safety stock covers the shortage

### Inventory Flow Logic
1. **Daily Demand**: PAR inventories face daily demand
2. **Sufficient Stock**: If PAR has enough → supplies demand → triggers replenishment order
3. **Lead Time**: Orders delivered after SKU-specific lead time
4. **PAR Stockout**: If PAR insufficient → stockout occurs
5. **Safety Stock Coverage**: Perpetual inventory covers PAR stockouts
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

## Next Steps for Model Development

1. **Data Processing**: Load and validate Excel data sources
2. **Parameter Extraction**: Extract lead times, demand patterns, and target inventories
3. **Simulation Engine**: Implement core mathematical equations
4. **Validation Framework**: Compare results with client's analytical solution
5. **Sensitivity Analysis**: Test impact of missing data (lead time variability, storage policies)

---
*Last Updated: [Current Date]*
*Status: Initial understanding captured from CedarSim_pipeline.docx*
