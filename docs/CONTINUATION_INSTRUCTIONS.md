# CedarSim Project Continuation Instructions

## Project Overview
We're building a CedarSim inventory management simulation system for hospital inventory management. The project involves analyzing Excel data and implementing a simulation model based on specifications in a Word document.

## Current Status
- ✅ **Model Understanding**: Complete understanding captured in `model.md`
- ✅ **Data Analysis Setup**: Jupyter notebook `excel_data_review.ipynb` created with comprehensive analysis
- ✅ **Data Structure**: Identified 6,372 SKUs (full inventory) vs 229 SKUs (analytical sample)
- 🔄 **SKU-to-Location Mapping Analysis**: In progress - need to complete

## Files Created
1. **`model.md`** - Main understanding document with all specifications
2. **`excel_data_review.ipynb`** - Comprehensive data analysis notebook
3. **`mapping_analysis_final.py`** - Script to analyze SKU-to-location mapping
4. **`CedarSim_pipeline.docx`** - Original Word document with specifications

## Data Files
1. **`2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx`** - Main data file
   - 6,372 SKUs across 17 PAR locations + 1 Perpetual inventory
   - Lead times, demand data, SKU-inventory mapping
2. **`2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx`** - Validation data
   - 229 SKUs with pre-calculated target inventories
   - Client's analytical solution for validation

## Immediate Next Steps

### 1. Complete SKU-to-Location Mapping Analysis
**Goal**: Determine if Excel data clearly maps each SKU to hospital locations

**Method**: Run the mapping analysis script
```bash
python mapping_analysis_final.py
```

**Expected Output**: 
- Mapping completeness for each of 17 PAR locations
- Whether values are quantities or presence/absence indicators
- Examples of SKU mappings
- Overall mapping statistics

**Key Questions to Answer**:
- Do most SKUs have clear location mappings?
- Are the values quantities (how much) or categorical (whether stored)?
- How many SKUs are unmapped?
- How many SKUs are in multiple locations?

### 2. Run Jupyter Notebook Analysis
**Goal**: Execute the comprehensive data analysis

**Method**: Open `excel_data_review.ipynb` and run all cells

**Key Analysis Points**:
- Data structure and quality assessment
- SKU overlap between datasets
- Demand pattern analysis
- Lead time analysis
- Data completeness for simulation

### 3. Validate Data Against Model Requirements
**Goal**: Ensure data meets simulation requirements from `model.md`

**Checklist**:
- [ ] Lead times available for all SKUs
- [ ] SKU-inventory mapping complete
- [ ] Historical demand data sufficient
- [ ] Target inventory levels available
- [ ] Service level targets confirmed (98%, Z-score 2.05)

## Model Implementation Plan

### Phase 1: Data Preparation
1. **Data Integration**: Map SKUs between all datasets
2. **Data Cleaning**: Handle missing values and outliers
3. **Data Validation**: Ensure consistency across datasets

### Phase 2: Simulation Engine
1. **Core Equations**: Implement mathematical model from `model.md`
2. **Inventory Flow Logic**: PAR → Safety Stock → Hospital Stockout
3. **Allocation Function**: Implement ALLOCATE function for distribution

### Phase 3: Validation
1. **Sample Testing**: Test on 229 SKU sample first
2. **Compare Results**: Validate against client's analytical solution
3. **Full Scale**: Apply to complete 6,372 SKU inventory

## Key Technical Details

### Mathematical Model (from model.md)
- **Inventory Gap** = MAX(0, ((depleting*DT+target_inventory)-(SKUs_in_Shipment+PAR)))
- **PAR Stockout** = (demand_projection-depleting*DT/day)
- **Service Level**: 98% (Z-score 2.05)
- **Lead Time**: Variable by SKU (no variability data available)

### Data Structure
- **6,372 SKUs** - Full hospital inventory
- **17 PAR Locations** - Department-level inventories
- **1 Perpetual Inventory** - Central safety stock
- **86,411 Demand Records** - Full year 2024 data

## Current Blockers
1. **SKU-to-Location Mapping**: Need to complete analysis to understand mapping clarity
2. **Data Quality**: Some missing lead time variability data mentioned in Word doc
3. **Storage Policy**: 2-day minimum storage policy needs implementation

## Success Criteria
- [ ] Clear understanding of SKU-to-location mapping
- [ ] Data quality assessment complete
- [ ] Simulation model implemented and validated
- [ ] Results match client's analytical solution within acceptable tolerance

## Next Chat Session Instructions
1. **Start with**: "I'm continuing the CedarSim project. Please run the mapping analysis to understand SKU-to-location mapping."
2. **Run**: `python mapping_analysis_final.py`
3. **Analyze**: Results to determine mapping clarity
4. **Continue**: With data preparation and model implementation based on findings

## Files to Reference
- **`model.md`** - Complete project understanding
- **`excel_data_review.ipynb`** - Data analysis notebook
- **`mapping_analysis_final.py`** - Mapping analysis script
- **Excel files** - Source data

---
*Last Updated: [Current Date]*
*Status: Ready for continuation*
