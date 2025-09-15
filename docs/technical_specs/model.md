# CedarSim Inventory Management Model - Understanding Document

## Project Overview
This document captures our understanding of the CedarSim inventory management simulation system for **Cedars-Sinai Marina del Rey Hospital**. This is a production-ready healthcare operations optimization project that serves as the main reference for model building and will be updated as we progress.

### **Project Context**
- **Client**: Cedars-Sinai Health System
- **Facility**: Marina del Rey Hospital (new facility)
- **Objective**: Use digital twin simulation to optimize medical supply inventory management
- **Partnership**: Confidential Core consulting and simulation engineering firm

### **Core Focus Areas**
- ✅ Ensuring optimal medical supplies availability across all PAR locations
- ✅ Eliminating excess inventory waste
- ✅ Minimizing stockouts and emergency replenishment needs
- ✅ Maintaining patient safety through reliable supply chains

## Data Sources

### 1. Complete Input Dataset (5,941 SKUs)
**File**: `data/final/csv_complete/Complete_Input_Dataset_20250913_220808.csv`
**Purpose**: Primary data source for inventory management simulation

**Key Fields**:
- **Oracle Item Number**: Unique SKU identifier
- **Avg Daily Burn Rate**: Demand rate per SKU
- **Avg Lead Time**: Lead time for replenishment from supplier
- **PAR Mapping**: X marks indicating which PARs each SKU is stored in
- **UOM**: Units of measure

### 2. Historical Demand Data (74,549 records)
**File**: `data/final/csv_complete/02_Demand_Data_Clean_Complete.csv`
**Purpose**: Historical demand patterns and delivery information

**Key Understanding**:
- **Delivery Locations (36)**: Physical delivery points (MDRCS, MDR6010JIT, etc.)
- **PAR Locations (18)**: Inventory management units where items are consumed
- **Flow**: Delivery locations receive supplies → distributed to PAR locations for consumption

### 3. Validation Dataset (74 SKUs)
**File**: `data/final/csv_complete/Validation_Input_Subset_20250913_220808.csv`
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
2. **Normal Replenishment**: If PAR has enough → supplies demand → triggers replenishment order from external supplier
3. **Lead Time**: Orders delivered after SKU-specific lead time from supplier
4. **PAR Stockout**: If PAR insufficient → stockout occurs
5. **Emergency Replenishment**: Follow graph edges from PAR SKU to Perpetual SKU (same SKU type)
6. **Hospital Stockout**: Remaining unsupplied demand becomes hospital-level stockout

### **Order-Up-To-Level Policy**
We use an **Order-Up-To-Level** inventory replenishment policy, which is a special case of the min-max policy.

**Policy Mechanism**: "If inventory goes below target, reorder up to target"

**How It Works**:
1. **Set Target Level** - Define optimal inventory level for each PAR location
2. **Monitor Inventory** - Track current stock levels continuously  
3. **Trigger Replenishment** - When inventory drops below target
4. **Order Up to Target** - Replenish exactly to the target level

**Key Characteristics**:
- **Deterministic Replenishment** - Always order to the same target level
- **No Order Quantity Optimization** - Focus on target level setting instead
- **Simplified Decision Making** - Clear, consistent replenishment logic

### Key Understanding - Replenishment Flow:
- **Primary Replenishment**: External Supplier → PAR Location (based on lead time)
- **Emergency Replenishment**: PAR Location → Perpetual Location (same SKU, immediate)
- **Perpetual Role**: Safety net for stockouts, not primary replenishment source

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

### **Two-Phase Implementation Approach**

#### **Phase 1: Pilot Phase - Model Verification**
- **Purpose**: Verify model internal consistency using analytical methods
- **Method**: Test with conventional safety stock formulas for both cycle and safety inventory
- **Validation**: Compare simulation results with analytical solutions
- **Outcome**: ✅ Simulation model internal consistency successfully verified

#### **Phase 2: Expansion Phase - Optimization Engine**
- **Purpose**: Use simulation as optimization engine for inventory target finding
- **Capability**: Process daily demand patterns and produce daily inventory trajectories
- **Focus**: Optimize inventory management while reducing holding costs

### Time Horizon
- **Duration**: One year of historical data
- **Focus**: Frequency of stockouts rather than accumulative volume

### **Monte Carlo Capabilities**
The simulation contains **two independent randomness sources**:

| **Engine** | **Purpose** | **Impact** |
|------------|-------------|------------|
| **🎲 Demand Pattern Engine** | Generates different demand scenarios | Affects inventory depletion rates |
| **⏱️ Lead Time Engine** | Simulates varying replenishment cycles | Determines safety stock requirements |

### Key Steps
1. **Historical Analysis**: Use historical demand data to calculate stockouts
2. **Target Implementation**: Implement client's target inventories
3. **Stockout Calculation**: Compute stockouts using target inventories
4. **Validation**: Compare results with client's analytical solution
5. **Optimization**: Use simulation to find optimal inventory targets

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

## **Advanced Simulation Capabilities**

### **Patient-Focused Modeling**
Revolutionary approach that shifts from demand forecasting to patient characteristics:

#### **Agent-Based Modeling**
- **Simulate patient admissions** with specific disease profiles
- **Create consumption blueprints** for each patient type
- **Automatically generate demand patterns** from patient scenarios

#### **Patient-to-Demand Translation Process**
```
Patient Admission → Disease Profile → Consumption Blueprint → SKU Demand Pattern
     ↓                    ↓                    ↓                    ↓
[Patient arrives]  [COVID-19, ICU]  [Timeline template]  [Daily SKU usage]
     ↓                    ↓                    ↓                    ↓
[Admission data]   [Comorbidities]   [Department routing]  [Inventory depletion]
```

#### **Machine Learning Opportunities**
- **Pattern Recognition**: Patient demographics → SKU usage timeline
- **Template Creation**: Historical patient data → Disease-specific consumption blueprints
- **Comorbidity Stacking**: Multiple conditions → Additive consumption patterns
- **Timeline Prediction**: Patient admission data → Department-specific usage schedule

### **Optimization Engine Capabilities**

#### **Scenario Testing Framework**
The simulation functions as a **dynamic calculator** for inventory experimentation:

**Input**: Target levels + daily demand + lead times  
**Output**: Inventory levels over time + stockout/emergency counts  
**Purpose**: Test any scenario to understand inventory behavior

#### **Generalized Optimization Algorithm**
1. **Start with initial values** based on analytical methods
2. **Set fixed scenario** (specific daily demand + lead times)
3. **Run simulation** to test current targets
4. **Adjust targets** based on results (minimize stockouts)
5. **Repeat** until optimal solution found

#### **Virtual Negative Inventory Technique**
Advanced optimization method that accelerates target finding:
1. **Release Stockout Constraint** - Allow inventory to go negative during iterations
2. **Track Negative Values** - Monitor how much inventory would be needed
3. **Estimate Gap** - Calculate how much perpetual inventory to increase
4. **Adjust Targets** - Use negative values to guide next iteration

## **Business Value & Unique Positioning**

### **What Makes This Different**
**Unique complexity**: Two independent inventory systems with emergency connections
- **PAR locations**: Independent replenishment cycles
- **Perpetual location**: Centralized safety stock
- **Emergency connections**: Complex routing network between PARs and perpetual

### **Smart Inventory Capabilities**

#### **1. Precise Scenario Testing**
- **Daily demand patterns** with realistic variability
- **Patient admission-based** demand generation
- **Disease-specific** emergency scenarios
- **Targeted preparedness** for known incidents

#### **2. Dual Optimization Approach**

| **Optimization Path** | **Method** | **Outcome** |
|----------------------|------------|-------------|
| **Forecasting Improvement** | Better demand + external lead time forecasts | Reduced inventory levels |
| **Operations Enhancement** | Internal process modeling + efficiency gains | Improved replenishment cycles |

#### **3. Space Optimization Capability**
- **Precise Space Planning** - Know exactly what goes in perpetual inventory
- **Capacity Optimization** - Prioritize items based on space efficiency
- **Dynamic Reallocation** - Adjust inventory mix to maximize space utilization
- **Constraint Integration** - Space limitations become optimization constraints

### **Why This Complexity Matters**
> **"This complex network of PAR-perpetual connections with emergency routing cannot be modeled by generic inventory software"**

- ❌ **Generic tools**: Assume single inventory system
- ❌ **Our reality**: Two independent systems with emergency connections
- ✅ **Our solution**: Custom simulation modeling this exact architecture

### **Final Outcome**
> **"Tool that carries the least amount of inventory with the least amount of risk - immune against targeted realistic scenarios"**

### **Unique Value Proposition**
> **"This level of operational complexity requires custom simulation development - delivering results that off-the-shelf solutions simply cannot match"**

## Next Steps for Model Development

1. **Object Graph Creation**: Implement Location, SKU, and Graph Manager classes
2. **Data Integration**: Load Excel data into object structure
3. **Simulation Engine**: Implement daily time-step processing
4. **Mathematical Model**: Implement core equations within object methods
5. **Validation Framework**: Compare results with client's analytical solution
6. **Monte Carlo Implementation**: Add demand pattern and lead time variability engines
7. **Patient Modeling**: Implement agent-based patient admission simulation
8. **Optimization Engine**: Build scenario testing and target optimization framework
9. **Testing**: Start with 74 validation SKUs before full-scale implementation

---
*Last Updated: September 13, 2025*
*Status: Comprehensive understanding captured from presentation and technical specifications*
