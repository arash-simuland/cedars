#!/usr/bin/env python3
"""
Clean up workspace by moving interim files to archive and keeping only final pipeline output.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def cleanup_workspace():
    """Clean up workspace by organizing files into proper structure."""
    
    print("🧹 CedarSim Workspace Cleanup")
    print("=" * 50)
    
    # Create archive structure
    archive_dirs = [
        'archive/interim_files',
        'archive/test_files', 
        'archive/scripts',
        'archive/analysis_scripts'
    ]
    
    for dir_path in archive_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")
    
    # Files to keep in root (FINAL OUTPUT)
    keep_in_root = [
        'CedarSim_Simulation_Ready_Data_Final.xlsx',  # Final pipeline output
        'CedarSim_Pipeline_Status_Update.md',         # Status documentation
        'cedarsim_pipeline.log',                      # Pipeline log
        'phase1_missing_lead_times_removal.csv',      # Audit trail
        'phase2_unmapped_skus_removal.csv'            # Audit trail
    ]
    
    # Files to move to archive/interim_files
    move_to_interim = [
        'CedarSim_Simulation_Ready_Data_FIXED.xlsx',
        'CedarSim_Simulation_Ready_Data_CORRUPTED.xlsx'
    ]
    
    # Files to move to archive/test_files
    move_to_test = [
        'CedarSim_Simulation_Ready_Data_ROBUST.xlsx',
        'CedarSim_Simulation_Ready_Data_ROBUST_temp.xlsx'
    ]
    
    # Files to move to archive/scripts
    move_to_scripts = [
        'cedarsim_complete_pipeline.py',
        'robust_data_cleaning.py',
        'improved_excel_creation.py',
        'fix_excel.py',
        'check_fixed_file.py',
        'compare_results.py',
        'examine_columns.py',
        'find_missing_sku.py',
        'detailed_sku_analysis.py',
        'check_robust_files.py',
        'cleanup_workspace.py',
        'validate_excel.py'
    ]
    
    # Files to move to archive/analysis_scripts
    move_to_analysis = [
        'test_python.bat',
        'manual_uninstall.bat',
        'python.bat'
    ]
    
    print(f"\n📁 Keeping in root directory:")
    for file_path in keep_in_root:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (not found)")
    
    print(f"\n📦 Moving interim files to archive/interim_files:")
    for file_path in move_to_interim:
        if os.path.exists(file_path):
            dest = f"archive/interim_files/{file_path}"
            shutil.move(file_path, dest)
            print(f"   ✅ Moved: {file_path} → {dest}")
        else:
            print(f"   ❌ {file_path} (not found)")
    
    print(f"\n🧪 Moving test files to archive/test_files:")
    for file_path in move_to_test:
        if os.path.exists(file_path):
            dest = f"archive/test_files/{file_path}"
            shutil.move(file_path, dest)
            print(f"   ✅ Moved: {file_path} → {dest}")
        else:
            print(f"   ❌ {file_path} (not found)")
    
    print(f"\n📜 Moving scripts to archive/scripts:")
    for file_path in move_to_scripts:
        if os.path.exists(file_path):
            dest = f"archive/scripts/{file_path}"
            shutil.move(file_path, dest)
            print(f"   ✅ Moved: {file_path} → {dest}")
        else:
            print(f"   ❌ {file_path} (not found)")
    
    print(f"\n🔧 Moving analysis scripts to archive/analysis_scripts:")
    for file_path in move_to_analysis:
        if os.path.exists(file_path):
            dest = f"archive/analysis_scripts/{file_path}"
            shutil.move(file_path, dest)
            print(f"   ✅ Moved: {file_path} → {dest}")
        else:
            print(f"   ❌ {file_path} (not found)")
    
    # Move backup directories
    backup_dirs = ['excel_backups', 'pipeline_backups']
    for backup_dir in backup_dirs:
        if os.path.exists(backup_dir):
            dest = f"archive/{backup_dir}"
            shutil.move(backup_dir, dest)
            print(f"   ✅ Moved directory: {backup_dir} → {dest}")
    
    # Move other files
    other_files = ['path_backup.txt']
    for file_path in other_files:
        if os.path.exists(file_path):
            dest = f"archive/{file_path}"
            shutil.move(file_path, dest)
            print(f"   ✅ Moved: {file_path} → {dest}")
    
    print(f"\n🎉 Cleanup Complete!")
    print(f"📊 Final workspace structure:")
    print(f"   Root directory contains only:")
    print(f"   - CedarSim_Simulation_Ready_Data_Final.xlsx (Final pipeline output)")
    print(f"   - CedarSim_Pipeline_Status_Update.md (Documentation)")
    print(f"   - cedarsim_pipeline.log (Pipeline log)")
    print(f"   - phase1_missing_lead_times_removal.csv (Audit trail)")
    print(f"   - phase2_unmapped_skus_removal.csv (Audit trail)")
    print(f"   - docs/ (Documentation folder)")
    print(f"   - archive/ (All other files organized)")

if __name__ == "__main__":
    cleanup_workspace()
