import pandas as pd
import numpy as np

print("=== CEDARSIM EXCEL DATA ANALYSIS ===")

# Load first Excel file
excel_file_1 = '2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx'
xl_file = pd.ExcelFile(excel_file_1)
print(f'\n=== EXCEL FILE 1 SHEETS ===')
print(f'Available sheets: {xl_file.sheet_names}')

# Load Department Rollup
print(f'\n=== DEPARTMENT ROLLUP (01. Data) ===')
dept_rollup = pd.read_excel(excel_file_1, sheet_name='01. Data (Department Rollup)')
print(f'Shape: {dept_rollup.shape}')
print(f'Columns: {list(dept_rollup.columns)}')
print(f'First 3 rows:')
print(dept_rollup.head(3))
print(f'Data types:')
print(dept_rollup.dtypes)

# Load Full Data
print(f'\n=== FULL DATA (02. Full Data) ===')
full_data = pd.read_excel(excel_file_1, sheet_name='02. Full Data')
print(f'Shape: {full_data.shape}')
print(f'Columns: {list(full_data.columns)}')
print(f'First 3 rows:')
print(full_data.head(3))
print(f'Data types:')
print(full_data.dtypes)

# Load Summary
print(f'\n=== SUMMARY (00. Summary) ===')
summary = pd.read_excel(excel_file_1, sheet_name='00. Summary')
print(f'Shape: {summary.shape}')
print(f'Columns: {list(summary.columns)}')
print(f'First 3 rows:')
print(summary.head(3))

# Load Hospital Levels
print(f'\n=== HOSPITAL LEVELS (03. Hospital Levels) ===')
hospital_levels = pd.read_excel(excel_file_1, sheet_name='03. Hospital Levels')
print(f'Shape: {hospital_levels.shape}')
print(f'Columns: {list(hospital_levels.columns)}')
print(f'First 3 rows:')
print(hospital_levels.head(3))

# Load Rooms
print(f'\n=== ROOMS (04. Rooms) ===')
rooms = pd.read_excel(excel_file_1, sheet_name='04. Rooms')
print(f'Shape: {rooms.shape}')
print(f'Columns: {list(rooms.columns)}')
print(f'First 3 rows:')
print(rooms.head(3))

# Load second Excel file
print(f'\n=== EXCEL FILE 2 ===')
excel_file_2 = '2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx'
xl_file_2 = pd.ExcelFile(excel_file_2)
print(f'Available sheets: {xl_file_2.sheet_names}')

safety_stock = pd.read_excel(excel_file_2, sheet_name=0)
print(f'\n=== SAFETY STOCK DATA ===')
print(f'Shape: {safety_stock.shape}')
print(f'Columns: {list(safety_stock.columns)}')
print(f'First 3 rows:')
print(safety_stock.head(3))
print(f'Data types:')
print(safety_stock.dtypes)

print(f'\n=== ANALYSIS COMPLETE ===')
