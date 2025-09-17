# CedarSim Architecture: Pre-Simulation vs Simulation

## Overview
The CedarSim system has a clear separation between **pre-simulation setup** and **actual simulation execution**.

## Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRE-SIMULATION PHASE                        │
│                    (AntologyGenerator)                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Create Locations (21 PARs + 1 Perpetual = 22 total)        │
│ 2. Create SKUs (2,813 unique SKUs, 4,776 instances)           │
│ 3. Generate Network Topology (PAR-perpetual connections)      │
│ 4. Finalize Structure (Validate connections)                  │
│ 5. Hand off to SimPy simulation                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SIMULATION PHASE                            │
│                    (SimPy Process-Based)                       │
├─────────────────────────────────────────────────────────────────┤
│ 1. Load pre-built structure from AntologyGenerator            │
│ 2. Create SimPy generators for each SKU                       │
│ 3. Run weekly simulation cycles                               │
│ 4. Use established network connections for emergency supply   │
│ 5. Process demand, orders, deliveries                         │
└─────────────────────────────────────────────────────────────────┘
```

## Key Separation of Concerns

### AntologyGenerator (Pre-Simulation)
- **Purpose**: Creates the object structure and network topology
- **Responsibilities**:
  - Create Location objects (21 PARs + 1 Perpetual = 22 total)
  - Create SKU objects (2,813 unique SKUs, 4,776 instances)
  - Establish PAR-perpetual connections
  - Validate network structure
  - Hand off to simulation

### SimPy Simulation (Runtime)
- **Purpose**: Executes the actual simulation on the pre-built structure
- **Responsibilities**:
  - Load the structure created by AntologyGenerator
  - Create SimPy generators for each SKU
  - Process weekly simulation cycles
  - Use established connections for emergency supply
  - Handle demand, orders, deliveries

## Why This Separation?

1. **Clear Responsibilities**: AntologyGenerator focuses on structure, SimPy focuses on execution
2. **Reusability**: Same structure can be used for different simulation scenarios
3. **Maintainability**: Changes to network topology don't affect simulation logic
4. **Testing**: Can test structure creation separately from simulation execution
5. **Performance**: Structure is created once, simulation runs multiple times

## Data Flow

```
CSV Data → AntologyGenerator → Network Structure → SimPy Simulation → Results
    │              │                    │                │
    │              │                    │                │
    ▼              ▼                    ▼                ▼
Input Files   Object Creation    Pre-built Network   Simulation Results
(2,813 SKUs)  (22 Locations)     (26 Connections)    (Inventory Levels)
```

## Implementation Status

- ✅ **AntologyGenerator**: Complete - creates structure and network topology
- ✅ **Core Classes**: Complete - Resource, Location, SKU with business logic
- ⏳ **SimPy Integration**: Pending - will run simulation on pre-built structure
- ⏳ **Data Loading**: Pending - will populate AntologyGenerator from CSV files

## Next Steps

1. **Data Integration**: Load CSV data into AntologyGenerator
2. **SimPy Generators**: Create SKU process generators
3. **Simulation Engine**: Implement SimPy simulation that uses pre-built structure
4. **Validation**: Test with 74 validation SKUs before full implementation
