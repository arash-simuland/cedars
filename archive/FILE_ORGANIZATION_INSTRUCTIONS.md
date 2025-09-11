# File Organization Instructions for CedarSim Project

## Current Situation
The repository has files scattered in the root directory. We need to organize them into a clean structure.

## Current Files to Organize
```
Root Directory:
├── 2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx
├── 2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx
├── item_00136_clean.xlsx
├── CedarSim_pipeline.docx
├── model.md
├── excel_data_review.ipynb
├── CONTINUATION_INSTRUCTIONS.md
├── README.md
├── presentation.md
├── compact_prep.md
├── analyze_excel.py
├── examine_excel_simple.py
├── examine_excel.py
├── mapping_analysis_final.py
├── mapping_analysis.py
├── sku_analysis.py
├── python.bat
├── output.txt
└── Directories: data/, analysis/, scripts/, docs/, archive/
```

## Target File Structure
```
CedarSim/
├── data/                          # Raw data files
│   ├── 2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx
│   ├── 2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx
│   └── item_00136_clean.xlsx
├── analysis/                      # Analysis notebooks and scripts
│   ├── excel_data_review.ipynb
│   ├── mapping_analysis_final.py
│   └── sku_analysis.py
├── scripts/                       # Utility scripts
│   ├── analyze_excel.py
│   ├── examine_excel_simple.py
│   ├── examine_excel.py
│   └── mapping_analysis.py
├── docs/                         # Documentation
│   ├── CedarSim_pipeline.docx
│   ├── model.md
│   ├── CONTINUATION_INSTRUCTIONS.md
│   ├── presentation.md
│   └── compact_prep.md
├── archive/                      # Old/redundant files
│   ├── python.bat
│   └── output.txt
└── README.md                     # Main project README
```

## Step-by-Step Instructions

### 1. Move Data Files
```bash
move "2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx" data\
move "2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx" data\
move "item_00136_clean.xlsx" data\
```

### 2. Move Analysis Files
```bash
move excel_data_review.ipynb analysis\
move mapping_analysis_final.py analysis\
move sku_analysis.py analysis\
```

### 3. Move Scripts
```bash
move analyze_excel.py scripts\
move examine_excel_simple.py scripts\
move examine_excel.py scripts\
move mapping_analysis.py scripts\
```

### 4. Move Documentation
```bash
move CedarSim_pipeline.docx docs\
move model.md docs\
move CONTINUATION_INSTRUCTIONS.md docs\
move presentation.md docs\
move compact_prep.md docs\
```

### 5. Archive Old Files
```bash
move python.bat archive\
move output.txt archive\
```

### 6. Update File Paths
After moving files, update any hardcoded paths in the scripts:
- Update Excel file paths in analysis scripts
- Update import paths if needed
- Update README.md with new structure

## Verification Commands
```bash
# Check final structure
tree /f

# Verify data files are accessible
dir data\
dir analysis\
dir scripts\
dir docs\
dir archive\
```

## Expected Final Structure
```
CedarSim/
├── data/ (3 Excel files)
├── analysis/ (3 Python files + 1 notebook)
├── scripts/ (4 Python files)
├── docs/ (5 documentation files)
├── archive/ (2 old files)
└── README.md
```

## Next Steps After Organization
1. Update README.md with new file structure
2. Test that all scripts still work with new paths
3. Update any hardcoded file paths in the code
4. Continue with the mapping analysis

## Quick Start for New Chat
**Message to start with:**
> "Please organize the CedarSim project files into a clean directory structure. Move data files to data/, analysis files to analysis/, scripts to scripts/, docs to docs/, and old files to archive/."

---
*Created: [Current Date]*
*Purpose: Clean up repository structure for better organization*
