# 🔍 Safety Stock Reverse Engineering Plan

**Objective**: Uncover the exact formula and data range used to calculate safety stock values in the validation test data.

## **Current Understanding**

### **Hypothesis: They're Using King's Method from MIT**

Based on analysis of validation data, we believe they're using a variation of King's method:

**Safety Stock = Z × √(Lead Time) × √(Demand Variance over 21 months)**

### **Key Components Identified:**

1. **Z-Score**: 2.05 (consistent across all SKUs)
   - Represents 98% service level
   - Standard for hospital inventory management

2. **Lead Time**: Varies by SKU (0.5-0.66 days)
   - From the demand data "Avg_Lead Time" column
   - Used as Performance Cycle (PC) in King's formula

3. **Time Period**: 2024-01-01 to 2025-10-01 (21 months)
   - Based on the demand data time range
   - Provides sufficient data for variance calculation

4. **Demand Variance**: Calculated from historical demand patterns
   - Different for each SKU-department combination
   - Accounts for seasonal variations and demand volatility

### **Evidence from Sample Calculations:**

**SKU 136 - Surgery Supplies:**
- Safety Stock: 229 units
- Lead Time: 0.5 days
- Calculated σD: 158 (high variability)
- Formula: 2.05 × √0.5 × 158 = 229 ✅

**SKU 508 - Balance Sheet CC:**
- Safety Stock: 40 units  
- Lead Time: 0.66 days
- Calculated σD: 24 (lower variability)
- Formula: 2.05 × √0.66 × 24 = 40 ✅

## **5-Phase Plan**

### **Phase 1: Data Analysis & Preparation**

#### **Step 1.1: Extract All SKU-Department Combinations**
- Identify all unique SKU-department pairs from validation test data
- Extract corresponding safety stock values, burn rates, and lead times
- Create a comprehensive dataset for analysis

#### **Step 1.2: Analyze Demand Data Patterns**
- Group demand data by SKU-department combinations
- Calculate demand statistics (mean, variance, standard deviation)
- Identify time periods with actual demand vs. zero demand
- Look for seasonal patterns and trends

#### **Step 1.3: Test Different Time Ranges**
- Test 2024-2025 (21 months) as primary hypothesis
- Test 2023-2025 (33 months) for longer-term patterns
- Test 2024 only (12 months) for shorter-term patterns
- Test rolling windows (6, 12, 18 months)

### **Phase 2: Formula Testing**

#### **Step 2.1: Test King's Method Variations**
- **Basic King's**: `Z × √(Lead Time) × σD`
- **Modified King's**: `Z × √(Lead Time/T1) × σD`
- **With Lead Time Variance**: `Z × √(Lead Time × σD² + σLT² × D²)`
- **Department-Adjusted**: Add department-specific multipliers

#### **Step 2.2: Test Alternative Formulas**
- **Standard Safety Stock**: `Z × √(Lead Time) × Daily Burn Rate`
- **With Demand Variability**: `Z × √(Lead Time) × √(Demand Variance) × Daily Burn Rate`
- **Time-Adjusted**: Add time horizon factors
- **Hybrid Approaches**: Combine multiple methods

#### **Step 2.3: Test Different Variance Calculations**
- **Daily Variance**: Calculate from daily demand data
- **Weekly Variance**: Calculate from weekly aggregated data
- **Monthly Variance**: Calculate from monthly aggregated data
- **Rolling Variance**: Use rolling windows of different sizes

### **Phase 3: Systematic Testing**

#### **Step 3.1: Create Test Matrix**
```
Formula Type × Time Range × Variance Method × Department Factor
```

#### **Step 3.2: Calculate Predicted Values**
- Apply each formula combination to all SKU-department pairs
- Generate predicted safety stock values
- Compare with actual validation values

#### **Step 3.3: Measure Accuracy**
- Calculate Mean Absolute Error (MAE)
- Calculate Root Mean Square Error (RMSE)
- Calculate R² (coefficient of determination)
- Identify best-performing formula combinations

### **Phase 4: Refinement & Validation**

#### **Step 4.1: Analyze Errors**
- Identify SKU-department pairs with largest errors
- Look for patterns in prediction errors
- Determine if errors are systematic or random

#### **Step 4.2: Refine Formula**
- Adjust formula based on error analysis
- Test additional factors (seasonality, trends, etc.)
- Incorporate department-specific adjustments

#### **Step 4.3: Final Validation**
- Test refined formula on all validation data
- Calculate final accuracy metrics
- Document the discovered formula and parameters

### **Phase 5: Documentation & Implementation**

#### **Step 5.1: Document Findings**
- Record the exact formula discovered
- Document data range and parameters used
- Create implementation guide

#### **Step 5.2: Create Implementation Script**
- Build Python script to calculate safety stock using discovered formula
- Test on validation data to confirm accuracy
- Prepare for integration with simulation

## **Success Criteria**

- **Accuracy Target**: >90% of predictions within 20% of actual values
- **Formula Clarity**: Clear, implementable formula with documented parameters
- **Data Range**: Identified time period and data sources used
- **Validation**: Confirmed accuracy across all SKU-department combinations

## **Tools & Methods**

- **Data Analysis**: Pandas for data manipulation and statistics
- **Formula Testing**: Systematic testing of multiple formula variations
- **Accuracy Measurement**: Statistical metrics (MAE, RMSE, R²)
- **Visualization**: Charts to identify patterns and outliers
- **Documentation**: Clear documentation of findings and methodology

## **Data Sources**

- **Validation Test Data**: `data/final/validation_subset/validation_test_data.csv` (24 SKUs with safety stock values)
- **Demand Data**: `data/final/validation_subset/validation_demand_subset.csv` (15 SKUs with historical demand data)
- **SKU Data**: `data/final/validation_subset/validation_sku_subset.csv` (24 SKUs with master data)

## **Data Alignment Status**

✅ **SKU Data**: All 24 SKUs from test data are now aligned and have complete master data
❌ **Demand Data**: Only 15 out of 24 SKUs have historical demand data
- **Missing demand data for 9 SKUs**: 00235, 00262, 00386, 00535, 00536, 00555, 00565, 01077, 30847
- **Available demand data for 15 SKUs**: 00136, 00508, 00523, 00529, 00549, 00552, 00838, 698758, 698770, 803949, 803975, 803992, 804039, 804046, 804052

## **Revised Analysis Approach**

Since only 15 SKUs have complete data (test data + SKU data + demand data), the reverse engineering will focus on these 15 SKUs:

**Complete Dataset SKUs (15):**
- 00136, 00508, 00523, 00529, 00549, 00552, 00838, 698758, 698770, 803949, 803975, 803992, 804039, 804046, 804052

**Incomplete Dataset SKUs (9):**
- 00235, 00262, 00386, 00535, 00536, 00555, 00565, 01077, 30847

## **Next Steps**

1. **Start Phase 1**: Extract all SKU-department combinations
2. **Analyze demand patterns** for each combination
3. **Test different time ranges** to find optimal data period
4. **Systematically test formulas** until we achieve >90% accuracy
5. **Document final formula** and implementation

---

**Status**: Ready to begin Phase 1 - Data Analysis & Preparation
**Last Updated**: Current session
**Next Action**: Extract SKU-department combinations and analyze demand patterns
