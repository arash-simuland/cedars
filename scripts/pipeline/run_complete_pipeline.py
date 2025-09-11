#!/usr/bin/env python3
"""
CedarSim Complete Pipeline Runner
=================================

This script runs both the data processing pipeline and 3D visualization pipeline
with timestamped outputs.

Author: CedarSim Team
Date: September 11, 2025
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent / "analysis"))
sys.path.append(str(Path(__file__).parent.parent / "simulation"))

def run_complete_pipeline():
    """Run the complete CedarSim pipeline: data processing + 3D visualization"""
    
    # Create runs directory structure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    runs_dir = Path("runs")
    runs_dir.mkdir(exist_ok=True)
    
    output_dir = runs_dir / f"run_{timestamp}"
    output_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for organized output
    (output_dir / "data").mkdir(exist_ok=True)
    (output_dir / "visualizations").mkdir(exist_ok=True)
    (output_dir / "reports").mkdir(exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)
    
    print("=" * 80)
    print("CEDARSIM COMPLETE PIPELINE")
    print("=" * 80)
    print(f"Timestamp: {timestamp}")
    print(f"Output Directory: {output_dir}")
    print("=" * 80)
    
    try:
        # Step 1: Run data processing pipeline
        print("\n🔄 STEP 1: Data Processing Pipeline")
        print("-" * 50)
        
        from cedarsim_complete_pipeline import main as run_data_pipeline
        data_success = run_data_pipeline()
        
        if not data_success:
            print("❌ Data processing failed!")
            return False
        
        print("✅ Data processing completed successfully!")
        
        # Step 2: Run 3D visualization pipeline
        print("\n🎨 STEP 2: 3D Visualization Pipeline")
        print("-" * 50)
        
        # Change to simulation directory for visualization
        original_dir = os.getcwd()
        os.chdir(Path(__file__).parent.parent / "simulation")
        
        from cedarsim_3d_viz import main as run_viz_pipeline
        viz_success = run_viz_pipeline()
        
        # Change back to original directory
        os.chdir(original_dir)
        
        if not viz_success:
            print("❌ Visualization pipeline failed!")
            return False
        
        print("✅ 3D visualization completed successfully!")
        
        # Step 3: Copy outputs to organized timestamped directory
        print("\n📁 STEP 3: Organizing Outputs")
        print("-" * 50)
        
        import shutil
        
        # Copy data outputs to data/ subdirectory
        data_files = [
            ("../../data/final/CedarSim_Simulation_Ready_Data_Final.xlsx", "data/"),
            ("../../data/audit_trails/phase1_missing_lead_times_removal.csv", "data/"),
            ("../../data/audit_trails/phase2_unmapped_skus_removal.csv", "data/")
        ]
        
        for file_path, subdir in data_files:
            if Path(file_path).exists():
                shutil.copy2(file_path, output_dir / subdir / Path(file_path).name)
                print(f"✅ Copied to {subdir}: {Path(file_path).name}")
        
        # Copy visualization outputs to visualizations/ subdirectory
        viz_files = [
            ("../simulation/cedarsim_combined_visualization.html", "visualizations/"),
            ("../simulation/cedarsim_network.html", "visualizations/"),
            ("../simulation/cedarsim_visualization_report.md", "reports/")
        ]
        
        for file_path, subdir in viz_files:
            if Path(file_path).exists():
                shutil.copy2(file_path, output_dir / subdir / Path(file_path).name)
                print(f"✅ Copied to {subdir}: {Path(file_path).name}")
        
        # Create run summary
        run_summary = f"""# CedarSim Pipeline Run Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Run Details
- **Run ID**: run_{timestamp}
- **Status**: SUCCESS
- **Data Processing**: ✅ Completed
- **3D Visualization**: ✅ Completed

## Output Structure
- `data/` - Clean simulation data and audit trails
- `visualizations/` - Interactive 3D HTML visualizations
- `reports/` - Summary reports and documentation
- `logs/` - Pipeline execution logs

## Files Generated
### Data Files
- CedarSim_Simulation_Ready_Data_Final.xlsx
- phase1_missing_lead_times_removal.csv
- phase2_unmapped_skus_removal.csv

### Visualizations
- cedarsim_combined_visualization.html
- cedarsim_network.html

### Reports
- cedarsim_visualization_report.md
- run_summary.md (this file)

---
*Complete pipeline run with organized outputs*
"""
        
        with open(output_dir / "run_summary.md", 'w', encoding='utf-8') as f:
            f.write(run_summary)
        print(f"✅ Created: run_summary.md")
        
        print(f"\n🎉 COMPLETE PIPELINE SUCCESSFUL!")
        print(f"📁 All outputs saved to: {output_dir}")
        print(f"📂 Organized structure:")
        print(f"   ├── data/ (Excel files, audit trails)")
        print(f"   ├── visualizations/ (HTML files)")
        print(f"   ├── reports/ (Summary reports)")
        print(f"   └── logs/ (Execution logs)")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_complete_pipeline()
    if success:
        print("\n✅ CedarSim Complete Pipeline finished successfully!")
    else:
        print("\n❌ CedarSim Complete Pipeline failed!")
        sys.exit(1)
