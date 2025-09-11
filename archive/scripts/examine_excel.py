import pandas as pd
import openpyxl

# Load the Excel files
files_to_examine = [
    '2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx',
    '2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx',
    'item_00136_clean.xlsx'
]

for file_path in files_to_examine:
    print(f"\n{'='*80}")
    print(f"EXAMINING FILE: {file_path}")
    print(f"{'='*80}")

    try:
        # Get sheet names
        xl = pd.ExcelFile(file_path)
        print("Sheet names:", xl.sheet_names)
        print("\n" + "="*50)
        
        # Examine each sheet
        for sheet_name in xl.sheet_names:
            print(f"\nSHEET: {sheet_name}")
            print("-" * 30)
            
            # Read the sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Shape: {df.shape} (rows, columns)")
            
            # Show column names
            print(f"Columns: {list(df.columns)}")
            
            # Show first few rows
            print("\nFirst 5 rows:")
            print(df.head())
            
            # Show data types
            print(f"\nData types:")
            print(df.dtypes)
            
            # Show any non-null counts
            print(f"\nNon-null counts:")
            print(df.count())
            
            print("\n" + "="*50)
            
    except Exception as e:
        print(f"Error examining {file_path}: {e}")
