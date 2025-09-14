# CedarSim Simulation Folder Structure

## 🎯 Overview
Created two separate environments for simulation development and production:

## 📁 **simulation_development/** - Development Environment
**Purpose**: Build, test, and iterate on simulation components

### Structure:
```
simulation_development/
├── data/                           # Development data
│   ├── Complete_Input_Dataset_20250913_220808.csv    # Full dataset (5,941 SKUs)
│   ├── Validation_Input_Subset_20250913_220808.csv   # Validation subset (74 SKUs)
│   └── 02_Demand_Data_Clean_Complete.csv             # Historical demand data
├── models/                         # Simulation model classes
├── scripts/                        # Development scripts
├── notebooks/                      # Jupyter notebooks for exploration
├── reports/                        # Development reports
├── logs/                          # Development logs
├── requirements.txt               # Python dependencies
└── README.md                      # Development guidelines
```

### Use For:
- ✅ **Building simulation components** (Location, SKU, SimulationEngine classes)
- ✅ **Testing with small datasets** (validation subset)
- ✅ **Experimenting and prototyping**
- ✅ **Debugging and development**
- ✅ **Jupyter notebook exploration**

## 📁 **simulation_production/** - Production Environment
**Purpose**: Final, tested simulation models for client use

### Structure:
```
simulation_production/
├── data/                          # Production data (empty - ready for full dataset)
├── models/                        # Production model classes
├── scripts/                       # Production simulation scripts
├── reports/                       # Client deliverables
├── logs/                         # Production execution logs
├── config/                       # Configuration files
└── README.md                     # Production guidelines
```

### Use For:
- ✅ **Final simulation runs** with full dataset
- ✅ **Client deliverables** and reports
- ✅ **Production-ready code** only
- ✅ **Performance monitoring**
- ✅ **Stable, documented models**

## 🚀 **Next Steps**

### **1. Start Development** (in `simulation_development/`)
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Start with validation subset** (74 SKUs) for quick testing
3. **Build model components** in `models/` folder
4. **Use notebooks** for exploration and testing
5. **Test and iterate** until components are stable

### **2. Move to Production** (in `simulation_production/`)
1. **Copy stable code** from development
2. **Copy full dataset** to production data folder
3. **Run full simulation** (5,941 SKUs)
4. **Generate client reports**
5. **Monitor performance**

## 📊 **Data Available**

### **Development Data** (Ready to Use)
- **Complete Dataset**: 5,941 SKUs with updated burn rates, lead times, UOM
- **Validation Subset**: 74 SKUs with pre-calculated safety stock levels
- **Demand Data**: Historical demand patterns for simulation

### **Production Data** (To Be Copied)
- Will copy full dataset when ready for production runs

## 🔄 **Workflow**

```
Development → Test → Validate → Promote → Production
     ↓           ↓        ↓         ↓         ↓
  Build      Debug    Validate   Stable   Client Use
```

## ⚠️ **Important Notes**

- **Development folder**: Your sandbox for experimentation
- **Production folder**: Only stable, tested code
- **Start small**: Use validation subset (74 SKUs) first
- **Document everything**: Findings inform production design
- **Keep organized**: Clean up development folder regularly

---
**Ready to start building your CedarSim simulation model!**
