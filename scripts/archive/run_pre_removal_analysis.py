#!/usr/bin/env python3
"""
CedarSim Pre-Removal Analysis
Comprehensive Impact Analysis Before Data Cleaning
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("=== CedarSim Pre-Removal Analysis ===")
print("Libraries imported successfully")

# Load all data sources
data_dir = Path('data')

# Main inventory data
inventory_file = data_dir / '2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx'
validation_file = data_dir / '2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx'

print(f"\nLoading data from: {data_dir}")
print(f"Inventory file exists: {inventory_file.exists()}")
print(f"Validation file exists: {validation_file.exists()}")

# Load main inventory data
print("\nLoading main inventory data...")

# Load SKU inventory mapping
sku_data = pd.read_excel(inventory_file, sheet_name='01. Data (Department Rollup)')
print(f"SKU data shape: {sku_data.shape}")
print(f"Columns: {list(sku_data.columns)}")

# Load historical demand data
demand_data = pd.read_excel(inventory_file, sheet_name='02. Full Data')
print(f"\nDemand data shape: {demand_data.shape}")
print(f"Columns: {list(demand_data.columns)}")

# Load validation data
validation_data = pd.read_excel(validation_file)
print(f"\nValidation data shape: {validation_data.shape}")
print(f"Columns: {list(validation_data.columns)}")

# Basic data overview
print("\n=== MAIN INVENTORY DATA OVERVIEW ===")
print(f"Total SKUs: {sku_data.shape[0]:,}")
print(f"Total demand records: {demand_data.shape[0]:,}")
print(f"Validation SKUs: {validation_data.shape[0]:,}")

print("\n=== SKU DATA COLUMNS ===")
for col in sku_data.columns:
    print(f"{col}: {sku_data[col].dtype}")

# Check for missing values in SKU data
print("\n=== MISSING VALUES IN SKU DATA ===")
missing_values = sku_data.isnull().sum()
missing_pct = (missing_values / len(sku_data)) * 100

missing_df = pd.DataFrame({
    'Column': missing_values.index,
    'Missing Count': missing_values.values,
    'Missing %': missing_pct.values
})

print(missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False))

# Analyze SKUs with missing lead times
print("\n=== ANALYSIS: SKUs WITH MISSING LEAD TIMES ===")

missing_lead_times = sku_data[sku_data['Avg Lead Time'].isnull()]
print(f"SKUs with missing lead times: {len(missing_lead_times):,} ({len(missing_lead_times)/len(sku_data)*100:.1f}%)")

# Department analysis
dept_analysis = missing_lead_times['Department Name'].value_counts()
print(f"\nTop 10 departments with missing lead times:")
print(dept_analysis.head(10))

# Supplier analysis
supplier_analysis = missing_lead_times['Supplier Name'].value_counts()
print(f"\nTop 10 suppliers with missing lead times:")
print(supplier_analysis.head(10))

# Analyze unmapped SKUs (assuming PAR location is in a column)
print("\n=== ANALYSIS: UNMAPPED SKUs ===")

# First, let's see what columns might contain PAR location info
print("Available columns:")
for i, col in enumerate(sku_data.columns):
    print(f"{i+1}. {col}")

# Look for PAR location column (might be named differently)
par_location_cols = [col for col in sku_data.columns if 'par' in col.lower() or 'location' in col.lower()]
print(f"\nPotential PAR location columns: {par_location_cols}")

# Check validation data preservation
print("\n=== VALIDATION DATA PRESERVATION CHECK ===")

# Get validation SKU IDs (assuming there's a column with SKU identifiers)
validation_sku_cols = [col for col in validation_data.columns if 'sku' in col.lower() or 'item' in col.lower() or 'oracle' in col.lower()]
print(f"Potential SKU columns in validation data: {validation_sku_cols}")

# Get SKU IDs from main data
sku_id_cols = [col for col in sku_data.columns if 'sku' in col.lower() or 'item' in col.lower() or 'oracle' in col.lower()]
print(f"Potential SKU columns in main data: {sku_id_cols}")

# Let's examine the actual data structure more carefully
print("\n=== DETAILED DATA STRUCTURE ANALYSIS ===")

print("\nSKU Data Sample:")
print(sku_data.head())

print("\nValidation Data Sample:")
print(validation_data.head())

print("\nDemand Data Sample:")
print(demand_data.head())

# Generate comprehensive impact analysis report
print("\n=== COMPREHENSIVE IMPACT ANALYSIS REPORT ===")
print(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Overall data statistics
print(f"\n1. OVERALL DATA STATISTICS")
print(f"   Total SKUs in dataset: {len(sku_data):,}")
print(f"   Total demand records: {len(demand_data):,}")
print(f"   Validation SKUs: {len(validation_data):,}")

# Missing lead times impact
print(f"\n2. MISSING LEAD TIMES IMPACT")
print(f"   SKUs with missing lead times: {len(missing_lead_times):,} ({len(missing_lead_times)/len(sku_data)*100:.1f}%)")
print(f"   Departments affected: {missing_lead_times['Department Name'].nunique()}")
print(f"   Suppliers affected: {missing_lead_times['Supplier Name'].nunique()}")

# Data quality metrics
print(f"\n3. DATA QUALITY METRICS")
for col in sku_data.columns:
    completeness = (sku_data[col].count() / len(sku_data)) * 100
    print(f"   {col}: {completeness:.1f}% complete")

print(f"\n4. NEXT STEPS")
print(f"   - Identify PAR location column for unmapped SKU analysis")
print(f"   - Cross-reference validation SKUs with main dataset")
print(f"   - Calculate business impact of data removals")
print(f"   - Generate detailed removal impact report")

print("\n=== ANALYSIS COMPLETE ===")
