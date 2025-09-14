# CedarSim Complete Pipeline

This folder contains the complete CedarSim pipeline that processes raw data and creates 3D visualizations.

## 📁 Files

- **`run_complete_pipeline.py`** - Main pipeline runner (calls both data processing + visualization)
- **`cedarsim_complete_pipeline.py`** - Data processing pipeline (raw data → clean data)
- **`cedarsim_3d_viz.py`** - 3D visualization pipeline (clean data → HTML visualizations)
- **`requirements_3d_viz.txt`** - Python dependencies

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements_3d_viz.txt

# Run complete pipeline
python run_complete_pipeline.py
```

## 📊 Pipeline Steps

1. **Data Processing**: Raw Excel files → Clean simulation-ready data
2. **3D Visualization**: Clean data → Interactive HTML visualizations
3. **Output Organization**: All results saved to timestamped folder

## 📁 Output Structure

Each run creates an organized timestamped folder: `runs/run_YYYYMMDD_HHMMSS/`

```
runs/run_20250911_143022/
├── data/                           # Clean simulation data
│   ├── CedarSim_Simulation_Ready_Data_Final.xlsx
│   ├── phase1_missing_lead_times_removal.csv
│   └── phase2_unmapped_skus_removal.csv
├── visualizations/                 # Interactive 3D HTML files
│   ├── cedarsim_combined_visualization.html
│   └── cedarsim_network.html
├── reports/                        # Summary reports
│   ├── cedarsim_visualization_report.md
│   └── run_summary.md
└── logs/                          # Execution logs (future)
```

**All runs are preserved** with timestamps for easy comparison and rollback.

## 🎯 What It Does

- **Processes 6,372 raw SKUs** → **5,941 clean SKUs**
- **Creates 18 hospital locations** across 9 hierarchy levels
- **Generates 1,554 emergency replenishment connections**
- **Produces interactive 3D visualizations** of the entire system

---
*Complete end-to-end pipeline from raw data to 3D visualizations*
