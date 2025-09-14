import pandas as pd
import numpy as np
from datetime import datetime
import os
import shutil
from pathlib import Path

def create_excel_with_error_handling(data_dict, output_file, backup_dir="backups"):
    """
    Create Excel file with comprehensive error handling and validation
    
    Args:
        data_dict: Dictionary with sheet names as keys and DataFrames as values
        output_file: Path to output Excel file
        backup_dir: Directory to store backups
    """
    
    print(f"Creating Excel file: {output_file}")
    print("=" * 50)
    
    # Create backup directory
    Path(backup_dir).mkdir(exist_ok=True)
    
    # Create backup of existing file if it exists
    if os.path.exists(output_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"{Path(output_file).stem}_backup_{timestamp}.xlsx")
        shutil.copy2(output_file, backup_file)
        print(f"✅ Backup created: {backup_file}")
    
    # Validate input data
    print("\n📊 Validating input data...")
    for sheet_name, df in data_dict.items():
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"Sheet '{sheet_name}' is not a DataFrame")
        if df.empty:
            print(f"⚠️  Warning: Sheet '{sheet_name}' is empty")
        print(f"  {sheet_name}: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Create temporary file first
    temp_file = output_file + ".tmp"
    
    try:
        print(f"\n💾 Writing to temporary file: {temp_file}")
        
        # Write to temporary file first
        with pd.ExcelWriter(temp_file, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                print(f"  Writing sheet: {sheet_name}")
                
                # Clean DataFrame before writing
                df_clean = df.copy()
                
                # Handle NaN values
                df_clean = df_clean.fillna('')
                
                # Ensure string columns don't have mixed types
                for col in df_clean.columns:
                    if df_clean[col].dtype == 'object':
                        df_clean[col] = df_clean[col].astype(str)
                
                # Write sheet
                df_clean.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"    ✅ {sheet_name}: {df_clean.shape[0]:,} rows written")
        
        print(f"\n✅ Temporary file created successfully")
        
        # Validate temporary file
        print("🔍 Validating temporary file...")
        validation_result = validate_excel_file(temp_file, data_dict)
        
        if validation_result['valid']:
            print("✅ Temporary file validation passed")
            
            # Move temporary file to final location
            if os.path.exists(output_file):
                os.remove(output_file)
            shutil.move(temp_file, output_file)
            print(f"✅ Final file created: {output_file}")
            
            # Final validation
            final_validation = validate_excel_file(output_file, data_dict)
            if final_validation['valid']:
                print("✅ Final file validation passed")
                print(f"📊 File size: {os.path.getsize(output_file):,} bytes")
                return True
            else:
                print("❌ Final file validation failed")
                return False
        else:
            print(f"❌ Temporary file validation failed: {validation_result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating Excel file: {str(e)}")
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print("🧹 Cleaned up temporary file")
        
        # Restore backup if it exists
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith(Path(output_file).stem)]
        if backup_files:
            latest_backup = max(backup_files, key=lambda x: os.path.getctime(os.path.join(backup_dir, x)))
            backup_path = os.path.join(backup_dir, latest_backup)
            shutil.copy2(backup_path, output_file)
            print(f"🔄 Restored from backup: {latest_backup}")
        
        return False

def validate_excel_file(file_path, expected_data):
    """
    Validate that Excel file can be read and contains expected data
    
    Args:
        file_path: Path to Excel file
        expected_data: Dictionary with expected sheet names and shapes
    
    Returns:
        dict: Validation result with 'valid' boolean and 'error' message
    """
    try:
        # Check if file exists and is readable
        if not os.path.exists(file_path):
            return {'valid': False, 'error': 'File does not exist'}
        
        if os.path.getsize(file_path) == 0:
            return {'valid': False, 'error': 'File is empty'}
        
        # Try to read the file
        xl_file = pd.ExcelFile(file_path)
        actual_sheets = xl_file.sheet_names
        
        # Check if all expected sheets exist
        expected_sheets = set(expected_data.keys())
        actual_sheets_set = set(actual_sheets)
        
        if not expected_sheets.issubset(actual_sheets_set):
            missing_sheets = expected_sheets - actual_sheets_set
            return {'valid': False, 'error': f'Missing sheets: {missing_sheets}'}
        
        # Check sheet shapes
        for sheet_name, expected_df in expected_data.items():
            try:
                actual_df = pd.read_excel(file_path, sheet_name=sheet_name)
                if actual_df.shape != expected_df.shape:
                    return {'valid': False, 'error': f'Sheet {sheet_name} shape mismatch: expected {expected_df.shape}, got {actual_df.shape}'}
            except Exception as e:
                return {'valid': False, 'error': f'Cannot read sheet {sheet_name}: {str(e)}'}
        
        return {'valid': True, 'error': None}
        
    except Exception as e:
        return {'valid': False, 'error': f'File validation error: {str(e)}'}

def create_cedarsim_excel():
    """
    Create the CedarSim simulation-ready Excel file with error handling
    """
    print("🏥 CedarSim Excel File Creation with Error Handling")
    print("=" * 60)
    
    # Load data (assuming the fixed file is available)
    try:
        print("📂 Loading data from fixed Excel file...")
        
        # Try to load from fixed file first
        if os.path.exists('CedarSim_Simulation_Ready_Data_FIXED.xlsx'):
            print("  Using fixed Excel file...")
            df = pd.read_excel('CedarSim_Simulation_Ready_Data_FIXED.xlsx')
            print(f"  ✅ Loaded {len(df)} rows × {len(df.columns)} columns")
            
            # Create sample data for demonstration
            # In real implementation, you would load the actual cleaned data
            data_dict = {
                '01_SKU_Inventory_Clean': df.head(1000),  # Sample data
                '02_Demand_Data_Clean': df.head(500),     # Sample data
                '03_Validation_Sample': df.head(100),     # Sample data
                '04_Phase2_Unmapped_SKUs': df.head(50)    # Sample data
            }
            
        else:
            print("❌ Fixed Excel file not found. Please run the fix_excel.py script first.")
            return False
            
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return False
    
    # Create Excel file with error handling
    success = create_excel_with_error_handling(
        data_dict=data_dict,
        output_file='CedarSim_Simulation_Ready_Data_ROBUST.xlsx',
        backup_dir='excel_backups'
    )
    
    if success:
        print("\n🎉 SUCCESS: Excel file created with robust error handling!")
        print("📁 Files created:")
        print("  - CedarSim_Simulation_Ready_Data_ROBUST.xlsx")
        print("  - excel_backups/ (backup directory)")
    else:
        print("\n❌ FAILED: Excel file creation failed. Check error messages above.")
    
    return success

if __name__ == "__main__":
    create_cedarsim_excel()
