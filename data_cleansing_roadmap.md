# CedarSim Data Cleansing & Preparation Roadmap
*Complete Data Processing Plan for Discrete Simulation*

## 🎯 **Roadmap Overview**

**Objective**: Transform raw Excel data into clean, simulation-ready datasets  
**Approach**: **Complete Data Only** - Remove incomplete records with detailed tracking  
**Output**: Clean, complete datasets ready for discrete event simulation  
**Philosophy**: Quality over quantity - only use complete, reliable data

## ✅ **PHASE 1 COMPLETED - Missing Lead Times**

**Status**: ✅ **COMPLETED** (September 11, 2025)  
**Results**: 298 SKUs removed, 6,074 clean SKUs remaining  
**Files Created**: CedarSim_Simulation_Ready_Data.xlsx, audit trail, clean CSVs  

---

## 📋 **Phase 1: Data Assessment & Validation**

### **Step 1.1: Load and Validate All Data Sources**
```python
# Load all Excel files and validate structure
- Main inventory data (6,372 SKUs)
- Historical demand data (86,411 records)  
- Safety stock sample (229 SKUs)
- Validate data types and formats
- Check for file corruption or encoding issues
```

### **Step 1.2: Create Data Quality Baseline**
```python
# Establish current data quality metrics
- Missing value counts by field
- Duplicate record identification
- Data type consistency checks
- Range validation for numeric fields
- Date format validation
```

### **Step 1.3: Cross-Reference Data Integrity**
```python
# Validate relationships between datasets
- SKU overlap between all files
- Department consistency across files
- Date range validation
- Lead time consistency checks
```

### **Step 1.4: Create Removal Tracking System**
```python
# Set up comprehensive tracking for data removals
- Initialize removal log database
- Define removal categories and reasons
- Create impact analysis framework
- Set up audit trail system
```

---

## 🧹 **Phase 2: Data Removal Operations (Complete Data Only)**

### **Step 2.1: Remove SKUs with Missing Lead Times**
```python
# Remove 808 SKUs with missing lead times (12.7% of SKUs)
- Identify SKUs with null/empty lead times
- Log removal details: SKU ID, Department, Supplier, Reason
- Track impact: Department distribution, Supplier distribution
- Calculate data loss percentage by category
- Generate removal report with business impact analysis
- NO IMPUTATION - Complete data only approach
```

### **Step 2.2: Remove Unmapped SKUs (197 SKUs)**
```python
# Remove 197 SKUs with no PAR location mapping
- Identify SKUs with no PAR location assignments
- Log removal details: SKU ID, Department, Item Description, Reason
- Track impact: Department distribution, Item type distribution
- Calculate data loss percentage by department
- Generate removal report with business impact analysis
```

### **Step 2.3: Remove Duplicate Records**
```python
# Remove 1,182 duplicate records from demand data
- Identify duplicate criteria (SKU + Date + Department)
- Keep most recent record for each duplicate
- Log removal details: Duplicate count, SKU affected, Date range
- Track impact: Demand data reduction percentage
- Generate removal report with duplicate analysis
```

### **Step 2.4: Remove Records with Missing Delivery Locations**
```python
# Remove 19 records with missing delivery locations
- Identify demand records with null delivery locations
- Log removal details: Record ID, SKU, Date, Department, Reason
- Track impact: Demand data loss by department
- Calculate data loss percentage
- Generate removal report with impact analysis
```

### **Step 2.5: Remove Outlier Records**
```python
# Remove 2,814 potential outlier records from demand data
- Identify outliers using IQR method (Q3 + 3*IQR)
- Log removal details: Record ID, SKU, Value, Outlier threshold, Reason
- Track impact: Demand data reduction by SKU and department
- Generate removal report with outlier analysis
- Validate remaining data quality
```

---

## 🔄 **Phase 3: Data Transformation & Enrichment**

### **Step 3.1: Create SKU Master Table**
```python
# Consolidate all SKU information into master table
- SKU ID, Description, UOM, Department
- Lead times (complete data only)
- Burn rates and demand patterns
- PAR location mappings
- Supplier information
- Data completeness flags
- Removal tracking references
```

### **Step 3.2: Generate Demand Patterns**
```python
# Create simulation-ready demand patterns
- Daily demand rates per SKU
- Demand variability coefficients
- Seasonal patterns (if applicable)
- Demand distribution parameters
- Historical demand validation
```

### **Step 3.3: Create PAR Location Master**
```python
# Consolidate PAR location information
- Location ID, Name, Level, Department
- SKU assignments and counts
- Capacity constraints (if any)
- Priority levels for allocation
- Active/Inactive status
```

### **Step 3.4: Calculate Target Inventories**
```python
# Implement King's method for target inventory calculation
- Safety stock calculations (98% service level, Z=2.05)
- Cycle stock calculations
- Total target inventory per SKU per location
- Validation against 229 SKU sample
```

---

## 🔗 **Phase 4: Data Integration & Mapping**

### **Step 4.1: Create SKU-Location Mapping Matrix**
```python
# Build comprehensive mapping between SKUs and locations
- Binary matrix: SKU x PAR Location
- Quantity mappings (if available)
- Multi-location handling rules
- Allocation priority matrix
```

### **Step 4.2: Create Demand-Location Mapping**
```python
# Map historical demand to specific locations
- Demand records linked to PAR locations
- Department-based demand allocation
- Demand aggregation by location
- Time series validation
```

### **Step 4.3: Create Supplier-Lead Time Mapping**
```python
# Build supplier performance database
- Supplier average lead times
- Lead time variability by supplier
- Supplier reliability metrics
- Imputation source tracking
```

---

## 📊 **Phase 5: Data Validation & Quality Assurance**

### **Step 5.1: Cross-Validation Checks**
```python
# Validate data consistency across all datasets
- SKU count consistency
- Department mapping validation
- Lead time reasonableness checks
- Demand pattern validation
- Location mapping completeness
```

### **Step 5.2: Business Logic Validation**
```python
# Validate against business rules
- Lead times within reasonable range (1-30 days)
- Demand rates non-negative
- PAR locations have assigned SKUs
- Target inventories positive
- Service level calculations correct
- All data complete (no missing values)
```

### **Step 5.3: Sample Validation Against Client Data**
```python
# Validate against 229 SKU sample
- Compare calculated vs client target inventories
- Validate lead time assignments
- Check demand pattern accuracy
- Verify location mappings
- Ensure sample SKUs are in our clean dataset
```

### **Step 5.4: Data Removal Impact Analysis**
```python
# Analyze impact of data removals
- Calculate final dataset sizes
- Analyze department coverage impact
- Assess supplier coverage impact
- Evaluate demand pattern completeness
- Generate comprehensive removal impact report
```

---

## 🏗️ **Phase 6: Simulation-Ready Data Preparation**

### **Step 6.1: Create Simulation Input Files**
```python
# Generate clean input files for simulation
- SKU master file (6,372 SKUs)
- PAR location file (17 locations)
- Demand pattern file (daily rates)
- Lead time file (with imputation flags)
- Target inventory file
```

### **Step 6.2: Create Data Quality Report**
```python
# Generate comprehensive data quality report
- Before/after data quality metrics
- Data removal statistics and reasons
- Data completeness percentages
- Validation results summary
- Removal impact analysis
- Recommendations for simulation
```

### **Step 6.3: Create Simulation Metadata**
```python
# Generate metadata for simulation
- Data processing timestamps
- Data removal source tracking
- Quality flag definitions
- Business rule validations
- Simulation parameters
- Removal audit trail
```

---

## 🎯 **Phase 7: Discrete Simulation Data Structure**

### **Step 7.1: Convert to Discrete Time Format**
```python
# Transform continuous data to discrete time steps
- Daily time series for demand
- Discrete lead time delays
- Event-driven inventory levels
- Time-step based calculations
```

### **Step 7.2: Create Event Data Structures**
```python
# Prepare data for SimPy discrete events
- Demand event schedules
- Replenishment event schedules
- Stockout event triggers
- Allocation event rules
```

### **Step 7.3: Create Resource Data Structures**
```python
# Prepare inventory resource data
- PAR location capacities
- Safety stock levels
- Initial inventory states
- Resource constraints
```

---

## 📋 **Execution Checklist**

### **Pre-Execution Setup**
- [ ] Backup original data files
- [ ] Set up data processing environment
- [ ] Create output directory structure
- [ ] Initialize logging system

### **Phase 1: Assessment**
- [ ] Load all data sources
- [ ] Validate data integrity
- [ ] Create quality baseline
- [ ] Document findings

### **Phase 2: Data Removal**
- [ ] Remove SKUs with missing lead times
- [ ] Remove unmapped SKUs
- [ ] Remove duplicate records
- [ ] Remove records with missing locations
- [ ] Remove outlier records
- [ ] Log all removals with detailed tracking

### **Phase 3: Transformation**
- [ ] Create SKU master table
- [ ] Generate demand patterns
- [ ] Create PAR location master
- [ ] Calculate target inventories

### **Phase 4: Integration**
- [ ] Create SKU-location mapping
- [ ] Create demand-location mapping
- [ ] Create supplier-lead time mapping

### **Phase 5: Validation**
- [ ] Cross-validation checks
- [ ] Business logic validation
- [ ] Sample validation
- [ ] Data removal impact analysis

### **Phase 6: Preparation**
- [ ] Create simulation input files
- [ ] Generate data quality report
- [ ] Create simulation metadata

### **Phase 7: Discrete Structure**
- [ ] Convert to discrete time format
- [ ] Create event data structures
- [ ] Create resource data structures

---

## 🚀 **Expected Outputs**

### **Clean Data Files**
- `sku_master_clean.csv` - Complete SKU information (~5,367 SKUs after removals)
- `par_locations_clean.csv` - PAR location details (17 locations)
- `demand_patterns_clean.csv` - Daily demand rates (cleaned demand data)
- `lead_times_clean.csv` - Lead times (complete data only, no missing values)
- `target_inventories_clean.csv` - Calculated target levels

### **Quality Reports**
- `data_quality_report.html` - Comprehensive quality metrics
- `data_removal_summary.csv` - Removal statistics and reasons
- `removal_impact_analysis.csv` - Impact of removals by category
- `validation_results.csv` - Validation outcomes
- `simulation_metadata.json` - Processing metadata

### **Simulation Inputs**
- `simulation_skus.json` - SKU data for SimPy (~5,367 complete SKUs)
- `simulation_locations.json` - Location data for SimPy (17 PAR locations)
- `simulation_events.json` - Event schedules (cleaned demand data)
- `simulation_resources.json` - Resource definitions

---

## ⚡ **Execution Strategy**

### **Single Script Approach**
- Create one comprehensive Python script
- Execute all phases sequentially
- Generate all outputs in one run
- Full error handling and logging
- Progress tracking and reporting

### **Modular Approach**
- Create separate scripts for each phase
- Execute phases independently
- Validate outputs between phases
- Allow for selective re-processing
- Better debugging and maintenance

**Recommendation**: Start with single script approach for efficiency, then modularize if needed.

---

*Roadmap Created: [Current Date]*  
*Status: Ready for Execution*  
*Next Step: Create comprehensive data cleansing script*
