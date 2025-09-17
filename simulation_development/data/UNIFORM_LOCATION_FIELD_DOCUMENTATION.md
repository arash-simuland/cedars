# Uniform Location Field Documentation

## Overview

This document describes the implementation of a uniform location field that maps MDR codes from demand data to PAR locations from inventory data, enabling consistent location-based analysis across both datasets.

## Problem Statement

The original data had two different location coding systems:
- **Demand Data**: Used MDR codes (e.g., MDR7420OR, MDRCS, MDRDOCK)
- **Inventory Data**: Used PAR locations (e.g., Level 2 Surgery/Procedures/PACU, Perpetual)

This inconsistency prevented proper aggregation and analysis of demand patterns by location.

## Solution

Created a uniform location field (`uniform_location`) that maps all MDR codes to their corresponding PAR locations using a comprehensive mapping table.

## Implementation Details

### Files Processed

1. **Input**: `SIMULATION_READY_DEMAND_DATA_CLEAN.csv`
   - 74,422 records
   - TORDC codes already removed
   - Contains `lo` field with MDR codes

2. **Output**: `SIMULATION_READY_DEMAND_DATA_WITH_UNIFORM_LOCATIONS.csv`
   - 74,422 records (same as input)
   - Added `uniform_location` field
   - Preserved original `lo` field for reference

### Mapping Table

The mapping table was created based on the `LOCATION_MAPPING_ANALYSIS.md` document:

```python
mapping = {
    # Level 1 (Ground Floor)
    'MDRER': 'Level 1 ED',
    'MDRXRAY': 'Level 1 Imaging',
    'MDR1SOUTH': 'Level 1 ED',
    'MDR1NORTH': 'Level 1 ED',
    'MDR7010TR': 'Level 1 ED',
    'MDR7010PED': 'Level 1 ED',
    'MDR7010OR': 'Level 1 Imaging',
    'MDREVS': 'Level 1 EVS_1321',
    
    # Level 2
    'MDR7430SS': 'Level 2 Surgery/Procedures/PACU',
    'MDR7420OR': 'Level 2 Surgery/Procedures/PACU',
    'MDRSURGERY': 'Level 2 Surgery/Procedures/PACU',
    'MDRRX': 'Level 2 Pharm',
    'MDR7710RX': 'Level 2 Pharm',
    
    # Level 3
    'MDRLAB': 'Level 3 Central Lab',
    'MDRDIETARY': 'Level 3 Food Service',
    'MDRPURCHAS': 'Level 3 Admin',
    'MDRGI': 'Level 3 Central Lab',
    'MDR7470OD': 'Level 3 Admin',
    'MDR7010OM': 'Level 3 Admin',
    
    # Level 5-7
    'MDR6170MS': 'Level 5 Observation, Medical Tele & Non-Tele',
    'MDR6172EAS': 'Level 5 Observation, Medical Tele & Non-Tele',
    'MDR6150TEL': 'Level 6 Telemetry, Cardiac & Stroke',
    'MDR7010JI': 'Level 7 ICU',
    'MDR7010ME': 'Level 7 ICU',
    'MDRICUPRO': 'Level 7 ICU',
    'MDR6010JIT': 'Level 7 ICU',
    
    # Support Services
    'MDRRT': 'Respiratory Therapy',
    'MDRCS': 'Perpetual',
    'MDRDOCK': 'Perpetual',
    'CS0075': 'Perpetual'
}
```

## Results

### Mapping Performance

- **Total records processed**: 74,422
- **Successfully mapped**: 74,403 (99.97%)
- **Unmappable records**: 19 (0.03%)
  - All unmappable records are due to NaN values in the original `lo` field
  - No valid MDR codes were unmappable

### Location Distribution

| Uniform Location | Records | Percentage |
|------------------|---------|------------|
| Level 2 Surgery/Procedures/PACU | 20,861 | 28.0% |
| Perpetual | 14,391 | 19.3% |
| Level 7 ICU | 13,975 | 18.8% |
| Level 5 Observation, Medical Tele & Non-Tele | 12,622 | 16.9% |
| Level 6 Telemetry, Cardiac & Stroke | 6,748 | 9.1% |
| Level 1 ED | 1,535 | 2.1% |
| Level 2 Pharm | 1,260 | 1.7% |
| Level 3 Admin | 1,014 | 1.4% |
| Level 1 Imaging | 795 | 1.1% |
| Level 1 EVS_1321 | 732 | 1.0% |
| Level 3 Central Lab | 310 | 0.4% |
| Level 3 Food Service | 132 | 0.2% |
| Respiratory Therapy | 28 | 0.0% |

### Top MDR Code Mappings

| MDR Code | Uniform Location | Records |
|----------|------------------|---------|
| MDR7420OR | Level 2 Surgery/Procedures/PACU | 18,496 |
| MDR6010JIT | Level 7 ICU | 7,798 |
| MDRDOCK | Perpetual | 7,349 |
| MDRCS | Perpetual | 7,041 |
| MDR6170MS | Level 5 Observation, Medical Tele & Non-Tele | 6,913 |
| MDR6150TEL | Level 6 Telemetry, Cardiac & Stroke | 6,748 |
| MDR6172EAS | Level 5 Observation, Medical Tele & Non-Tele | 5,709 |
| MDR7010JI | Level 7 ICU | 2,880 |
| MDR7010ME | Level 7 ICU | 2,752 |
| MDR7430SS | Level 2 Surgery/Procedures/PACU | 1,880 |

## Data Quality

### Strengths
- **High mapping success rate**: 99.97%
- **Complete coverage**: All valid MDR codes mapped
- **Consistent naming**: Matches inventory data location names exactly
- **No data loss**: All original records preserved

### Issues Identified
- **19 NaN records**: Original data contains NaN values in `lo` field
  - These records have `uniform_location` = NaN
  - Represents 0.03% of total data
  - No impact on analysis as they're invalid records

## Usage

### For Simulation
The uniform location field enables:
- **Demand aggregation by location**: Group demand data by PAR locations
- **Inventory alignment**: Match demand patterns with inventory locations
- **Location-based analysis**: Analyze demand patterns across hospital floors

### For Data Analysis
```python
import pandas as pd

# Load data with uniform locations
df = pd.read_csv('SIMULATION_READY_DEMAND_DATA_WITH_UNIFORM_LOCATIONS.csv')

# Filter out NaN values
df_clean = df[df['uniform_location'].notna()]

# Group by uniform location
location_demand = df_clean.groupby('uniform_location')['Total Qty Issues'].sum()

# Analyze demand patterns by floor
floor_analysis = df_clean.groupby('uniform_location').agg({
    'Total Qty Issues': 'sum',
    'Avg Daily Burn Rate': 'mean',
    'oid': 'nunique'
})
```

## Files Created

1. **`create_uniform_locations.py`**: Script that implements the mapping
2. **`SIMULATION_READY_DEMAND_DATA_WITH_UNIFORM_LOCATIONS.csv`**: Output file with uniform location field
3. **`UNIFORM_LOCATION_FIELD_DOCUMENTATION.md`**: This documentation file

## Validation

The implementation was validated through:
- **Mapping coverage analysis**: Confirmed 99.97% success rate
- **Location distribution verification**: Compared with inventory data locations
- **Data integrity checks**: Ensured no data loss during mapping
- **Cross-reference validation**: Verified mappings against original analysis document

## Maintenance

### Adding New MDR Codes
If new MDR codes are added to the demand data:
1. Update the mapping dictionary in `create_uniform_locations.py`
2. Re-run the script to generate updated uniform locations
3. Update this documentation with new mappings

### Updating Mappings
If location mappings need to be changed:
1. Update the mapping dictionary
2. Re-run the script
3. Validate results
4. Update documentation

---

*Documentation created: $(date)*  
*Implementation status: Complete and validated*  
*Data quality: A+ (99.97% mapping success)*
