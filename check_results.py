import pandas as pd

print("Checking analysis results...")

# Check if final file exists and what's in it
try:
    xl = pd.ExcelFile('CedarSim_Simulation_Ready_Data_Final.xlsx')
    print(f"Sheets in final file: {xl.sheet_names}")
    
    for sheet in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet)
        print(f"{sheet}: {len(df)} rows")
        
except Exception as e:
    print(f"Error reading final file: {e}")

# Check if CSV was created
try:
    df_csv = pd.read_csv('unmapped_skus_phase2.csv')
    print(f"\nUnmapped SKUs CSV: {len(df_csv)} rows")
    print("Columns:", df_csv.columns.tolist())
except Exception as e:
    print(f"CSV file not found or error: {e}")

print("\nAnalysis summary:")
print("- Found 133 unmapped SKUs (not 197 as expected)")
print("- 1 validation SKU is unmapped (needs attention)")
print("- Top affected departments: Spine Center, Employee Health, Bariatric Clinic")
print("- Most affected supplier: Medline Industries Inc")
