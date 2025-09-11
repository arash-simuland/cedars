# CedarSim - Cedars-Sinai Marina del Rey Hospital
## Medical Supply Inventory Optimization Project

This repository contains the CedarSim project for optimizing medical supply inventory management at Cedars-Sinai's Marina del Rey hospital using digital twin simulation.

## Project Overview

**Confidential Core** has partnered with **Cedars-Sinai Health System** to develop a simulation-based solution for optimizing medical supply inventory at their new Marina del Rey hospital facility.

## Key Objectives

- Optimize cycle inventory targets (PAR levels) for each department
- Determine safety inventory targets for centralized perpetual location
- Minimize stockouts and emergency replenishment needs
- Reduce inventory holding costs while maintaining patient safety

## Repository Structure

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
└── README.md                     # This file
```

## Key Technical Features

- **Daily simulation capability** - Processes daily demand patterns
- **Three core dynamics** - PAR replenishment, perpetual replenishment, emergency replenishment
- **Monte Carlo engines** - Demand patterns and lead time variability
- **Multi-hospital scalability** - Star-shaped network architecture

## Getting Started

1. **Data Analysis**: Start with `analysis/excel_data_review.ipynb` to explore the inventory data
2. **Mapping Analysis**: Run `analysis/mapping_analysis_final.py` for SKU mapping
3. **Documentation**: Review `docs/presentation.md` for project overview and `docs/CONTINUATION_INSTRUCTIONS.md` for next steps

## Data Files

- **Storage Burn Rates**: `data/2025-07-14_MDRH_Inventory_Storage_Burn_Rates_V3.xlsx`
- **Safety Stock Sample**: `data/2025-08-04_MDRH_Inventory_Safety_Stock_Sample_Items.xlsx`
- **Clean Item Data**: `data/item_00136_clean.xlsx`

## Analysis Scripts

- **Excel Data Review**: `analysis/excel_data_review.ipynb` - Jupyter notebook for data exploration
- **Mapping Analysis**: `analysis/mapping_analysis_final.py` - Final SKU mapping analysis
- **SKU Analysis**: `analysis/sku_analysis.py` - SKU-specific analysis tools

## Documentation

- **Main Presentation**: `docs/presentation.md` - Project presentation content
- **Pipeline Documentation**: `docs/CedarSim_pipeline.docx` - Technical pipeline details
- **Model Documentation**: `docs/model.md` - Simulation model specifications
- **Continuation Instructions**: `docs/CONTINUATION_INSTRUCTIONS.md` - Next steps and workflow
- **Compact Prep**: `docs/compact_prep.md` - Preparation guidelines

## Future Enhancements

See the "Future Enhancements & Considerations" section in the presentation for planned improvements including timeline information, success metrics, ROI analysis, and multi-hospital expansion capabilities.

---

*Confidential Core - Healthcare Operations Optimization*
