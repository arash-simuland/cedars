import pandas as pd
import numpy as np
from datetime import datetime
import os
import shutil
from pathlib import Path
import logging
import time
import gc

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def safe_excel_operation(operation_name, operation_func, *args, **kwargs):
    """
    Safely execute Excel operations with error handling and rollback
    
    Args:
        operation_name: Name of the operation for logging
        operation_func: Function to execute
        *args, **kwargs: Arguments for the function
    
    Returns:
        tuple: (success: bool, result: any, error: str)
    """
    try:
        logger.info(f"Starting {operation_name}...")
        result = operation_func(*args, **kwargs)
        logger.info(f"✅ {operation_name} completed successfully")
        return True, result, None
    except Exception as e:
        error_msg = f"❌ {operation_name} failed: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg

def create_robust_excel_file(data_dict, output_file, backup_dir="backups"):
    """
    Create Excel file with comprehensive error handling, validation, and rollback
    
    Args:
        data_dict: Dictionary with sheet names as keys and DataFrames as values
        output_file: Path to output Excel file
        backup_dir: Directory to store backups
    
    Returns:
        tuple: (success: bool, error_message: str)
    """
    
    logger.info(f"Creating robust Excel file: {output_file}")
    
    # Create backup directory
    Path(backup_dir).mkdir(exist_ok=True)
    
    # Create backup of existing file if it exists
    if os.path.exists(output_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"{Path(output_file).stem}_backup_{timestamp}.xlsx")
        shutil.copy2(output_file, backup_file)
        logger.info(f"✅ Backup created: {backup_file}")
    
    # Validate input data
    logger.info("📊 Validating input data...")
    for sheet_name, df in data_dict.items():
        if not isinstance(df, pd.DataFrame):
            return False, f"Sheet '{sheet_name}' is not a DataFrame"
        if df.empty:
            logger.warning(f"⚠️  Sheet '{sheet_name}' is empty")
        logger.info(f"  {sheet_name}: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Create temporary file first
    temp_file = output_file.replace('.xlsx', '_temp.xlsx')
    
    try:
        logger.info(f"💾 Writing to temporary file: {temp_file}")
        
        # Write to temporary file with error handling
        success, _, error = safe_excel_operation(
            "Excel file writing",
            write_excel_sheets,
            temp_file, data_dict
        )
        
        if not success:
            return False, error
        
        # Validate temporary file
        logger.info("🔍 Validating temporary file...")
        validation_result = validate_excel_file_robust(temp_file, data_dict)
        
        if not validation_result['valid']:
            return False, f"Temporary file validation failed: {validation_result['error']}"
        
        logger.info("✅ Temporary file validation passed")
        
        # Move temporary file to final location
        if os.path.exists(output_file):
            os.remove(output_file)
        shutil.move(temp_file, output_file)
        logger.info(f"✅ Final file created: {output_file}")
        
        # Final validation
        final_validation = validate_excel_file_robust(output_file, data_dict)
        if not final_validation['valid']:
            return False, f"Final file validation failed: {final_validation['error']}"
        
        logger.info("✅ Final file validation passed")
        logger.info(f"📊 File size: {os.path.getsize(output_file):,} bytes")
        
        return True, None
        
    except Exception as e:
        error_msg = f"Error creating Excel file: {str(e)}"
        logger.error(error_msg)
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            logger.info("🧹 Cleaned up temporary file")
        
        # Restore backup if it exists
        try:
            backup_files = [f for f in os.listdir(backup_dir) if f.startswith(Path(output_file).stem)]
            if backup_files:
                latest_backup = max(backup_files, key=lambda x: os.path.getctime(os.path.join(backup_dir, x)))
                backup_path = os.path.join(backup_dir, latest_backup)
                shutil.copy2(backup_path, output_file)
                logger.info(f"🔄 Restored from backup: {latest_backup}")
        except Exception as restore_error:
            logger.error(f"Failed to restore backup: {restore_error}")
        
        return False, error_msg

def write_excel_sheets(file_path, data_dict):
    """
    Write multiple sheets to Excel file with individual error handling
    
    Args:
        file_path: Path to Excel file
        data_dict: Dictionary with sheet names and DataFrames
    """
    writer = None
    try:
        writer = pd.ExcelWriter(file_path, engine='openpyxl')
        
        for sheet_name, df in data_dict.items():
            logger.info(f"  Writing sheet: {sheet_name}")
            
            # Clean DataFrame before writing
            df_clean = df.copy()
            
            # Handle NaN values
            df_clean = df_clean.fillna('')
            
            # Ensure string columns don't have mixed types
            for col in df_clean.columns:
                if df_clean[col].dtype == 'object':
                    df_clean[col] = df_clean[col].astype(str)
            
            # Write sheet with error handling
            try:
                df_clean.to_excel(writer, sheet_name=sheet_name, index=False)
                logger.info(f"    ✅ {sheet_name}: {df_clean.shape[0]:,} rows written")
            except Exception as e:
                logger.error(f"    ❌ Failed to write sheet {sheet_name}: {str(e)}")
                raise
        
        # Ensure writer is properly closed
        writer.close()
        writer = None
        
        # Force garbage collection and small delay to ensure file is released
        gc.collect()
        time.sleep(0.1)
        
    except Exception as e:
        if writer is not None:
            writer.close()
        raise

def validate_excel_file_robust(file_path, expected_data):
    """
    Robust validation of Excel file with detailed error reporting
    
    Args:
        file_path: Path to Excel file
        expected_data: Dictionary with expected sheet names and DataFrames
    
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
        try:
            xl_file = pd.ExcelFile(file_path)
        except Exception as e:
            return {'valid': False, 'error': f'Cannot open Excel file: {str(e)}'}
        
        actual_sheets = xl_file.sheet_names
        
        # Check if all expected sheets exist
        expected_sheets = set(expected_data.keys())
        actual_sheets_set = set(actual_sheets)
        
        if not expected_sheets.issubset(actual_sheets_set):
            missing_sheets = expected_sheets - actual_sheets_set
            return {'valid': False, 'error': f'Missing sheets: {missing_sheets}'}
        
        # Check sheet shapes and data integrity
        for sheet_name, expected_df in expected_data.items():
            try:
                actual_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Check shape
                if actual_df.shape != expected_df.shape:
                    return {'valid': False, 'error': f'Sheet {sheet_name} shape mismatch: expected {expected_df.shape}, got {actual_df.shape}'}
                
                # Check for completely empty sheets
                if actual_df.empty:
                    return {'valid': False, 'error': f'Sheet {sheet_name} is empty'}
                
                # Check for critical columns (if they exist in expected data)
                if hasattr(expected_df, 'columns'):
                    critical_cols = ['Oracle Item Number', 'Item Description', 'Department Name']
                    missing_critical = [col for col in critical_cols if col in expected_df.columns and col not in actual_df.columns]
                    if missing_critical:
                        return {'valid': False, 'error': f'Sheet {sheet_name} missing critical columns: {missing_critical}'}
                
            except Exception as e:
                return {'valid': False, 'error': f'Cannot read sheet {sheet_name}: {str(e)}'}
        
        return {'valid': True, 'error': None}
        
    except Exception as e:
        return {'valid': False, 'error': f'File validation error: {str(e)}'}

def create_cedarsim_robust_excel():
    """
    Create the CedarSim simulation-ready Excel file with robust error handling
    """
    logger.info("🏥 CedarSim Robust Excel File Creation")
    logger.info("=" * 60)
    
    # Load data from fixed file
    try:
        logger.info("📂 Loading data from fixed Excel file...")
        
        if not os.path.exists('CedarSim_Simulation_Ready_Data_FIXED.xlsx'):
            logger.error("❌ Fixed Excel file not found. Please run the fix_excel.py script first.")
            return False
        
        # Load the fixed data
        df = pd.read_excel('CedarSim_Simulation_Ready_Data_FIXED.xlsx')
        logger.info(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")
        
        # Create data dictionary for Excel creation
        # In real implementation, you would load the actual cleaned data from different sources
        data_dict = {
            '01_SKU_Inventory_Clean': df.head(1000),  # Sample - replace with actual clean SKU data
            '02_Demand_Data_Clean': df.head(500),     # Sample - replace with actual demand data
            '03_Validation_Sample': df.head(100),     # Sample - replace with actual validation data
            '04_Phase2_Unmapped_SKUs': df.head(50)    # Sample - replace with actual unmapped SKUs
        }
        
    except Exception as e:
        logger.error(f"❌ Error loading data: {str(e)}")
        return False
    
    # Create Excel file with robust error handling
    success, error = create_robust_excel_file(
        data_dict=data_dict,
        output_file='CedarSim_Simulation_Ready_Data_ROBUST.xlsx',
        backup_dir='excel_backups'
    )
    
    if success:
        logger.info("🎉 SUCCESS: Excel file created with robust error handling!")
        logger.info("📁 Files created:")
        logger.info("  - CedarSim_Simulation_Ready_Data_ROBUST.xlsx")
        logger.info("  - excel_backups/ (backup directory)")
        return True
    else:
        logger.error(f"❌ FAILED: Excel file creation failed. Error: {error}")
        return False

if __name__ == "__main__":
    success = create_cedarsim_robust_excel()
    if success:
        print("\n✅ Script completed successfully!")
    else:
        print("\n❌ Script failed. Check logs for details.")
