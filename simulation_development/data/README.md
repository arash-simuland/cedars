# CedarSim Data Schema

## Data Files

### Production Input Data
- `prod-input-data/SIMULATION_READY_DEMAND_DATA.csv` - Original historical demand data (74,511 records)
- `prod-input-data/SIMULATION_READY_DEMAND_DATA_WITH_UNIFORM_LOCATIONS.csv` - **PRIMARY** demand data with uniform location field (74,403 records)
- `prod-input-data/SIMULATION_READY_SKU_INVENTORY_DATA.csv` - SKU inventory data (4,726 records)

### Documentation
- `LOCATION_MAPPING_ANALYSIS.md` - Complete MDR to PAR location mapping table
- `LOCATION_MAPPING_VALIDATION_REPORT.md` - Validation results and implementation status
- `UNIFORM_LOCATION_FIELD_DOCUMENTATION.md` - Detailed documentation of uniform location field

## Key Schema Detail

**Unique Identifier**: The combination of `oid` + `lo` creates a unique location-item pair.

### Examples:
- `000005` + `MDRCS` = Unique demand tracking location (MDR code)
- `000005` + `Level 1 ED` = Unique inventory location (PAR location)
- `000005` + `Level 7 ICU` = Different unique inventory location (PAR location)

The same oid can exist in multiple locations, and each `(oid, lo)` pair represents a unique inventory position or demand tracking point.

## Location Mapping

**MDR Codes** (demand data) are mapped to **PAR Locations** (inventory data) using a comprehensive mapping table:

- **MDR7420OR** → **Level 2 Surgery/Procedures/PACU**
- **MDRCS** → **Perpetual**
- **MDRDOCK** → **Perpetual**
- **MDR6010JIT** → **Level 7 ICU**
- And 26 more mappings...

## Uniform Location Field

The `uniform_location` field in the primary demand data file provides:
- **Consistent location naming** across demand and inventory data
- **100% mapping success rate** (74,403/74,403 records after cleaning)
- **Ready for simulation** with proper location-based aggregation
- **13 unique locations** matching between demand and inventory data

## Column Consistency

Both data files use uniform column names:
- `oid` - SKU identifier (Oracle Item Number)
- `lo` - Location identifier (MDR codes in demand, PAR locations in inventory)
- `uniform_location` - Mapped PAR location (demand data only)
