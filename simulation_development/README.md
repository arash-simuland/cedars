# Simulation Development - MODEL BUILDING PHASE

This directory is for developing the CedarSim simulation models. We are currently in the **model building phase** implementing the object-oriented simulation framework.

## Current Understanding

### Replenishment Flow:
- **Primary Replenishment**: External Supplier → PAR Location (based on lead time)
- **Emergency Replenishment**: PAR Location → Perpetual Location (same SKU, immediate)
- **Perpetual Role**: Safety net for stockouts, not primary replenishment source

### Data Structure:
- **Delivery Locations (36)**: Physical delivery points where supplies arrive
- **PAR Locations (18)**: Inventory management units where items are consumed
- **Flow**: Delivery → Distribution → Consumption at PARs

## Data Access

All simulation data is available in `../data/final/csv_complete/`:
- `Complete_Input_Dataset_20250913_220808.csv` - Full dataset (5,941 SKUs)
- `Validation_Input_Subset_20250913_220808.csv` - Validation subset (74 SKUs)
- `02_Demand_Data_Clean_Complete.csv` - Historical demand data

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Access data from `../data/final/csv_complete/`
3. Build simulation models in this directory
4. Reference technical specs in `../docs/technical_specs/model.md`

## Current Development Status

- ✅ **Data Understanding**: Clear understanding of replenishment flow and data structure
- 🚧 **Model Implementation**: Currently building object-oriented simulation framework
- ⏳ **Next Steps**: Implement Location, SKU, and GraphManager classes