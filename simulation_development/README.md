# CedarSim Simulation Development Environment

## 🎯 Purpose
This directory contains the **development version** of the CedarSim simulation model. Use this for:
- Building and testing simulation components
- Experimenting with different approaches
- Debugging and development work
- Creating prototypes and proof-of-concepts

## 📁 Directory Structure

### `data/`
- **Input data** for development and testing
- **Sample datasets** for quick testing
- **Test data** for unit testing
- **Development data** (smaller subsets for faster iteration)

### `models/`
- **Simulation model classes** (Location, SKU, etc.)
- **Model prototypes** and experimental versions
- **Model configuration files**
- **Model validation scripts**

### `scripts/`
- **Development scripts** for testing and debugging
- **Data processing utilities** for development
- **Model building scripts**
- **Testing and validation scripts**

### `notebooks/`
- **Jupyter notebooks** for exploration and analysis
- **Model development notebooks**
- **Data analysis notebooks**
- **Prototype testing notebooks**

### `reports/`
- **Development reports** and findings
- **Model performance analysis**
- **Debugging logs** and error reports
- **Development documentation**

### `logs/`
- **Development logs** and debug information
- **Model execution logs**
- **Error logs** and troubleshooting info

## 🚀 Getting Started

1. **Copy input data** from `../data/final/csv_complete/` to `data/`
2. **Start with validation subset** (74 SKUs) for quick testing
3. **Build model components** in `models/`
4. **Test and iterate** using `notebooks/` and `scripts/`
5. **Document findings** in `reports/`

## 📋 Development Workflow

1. **Prototype** → Build initial model components
2. **Test** → Validate with small datasets
3. **Iterate** → Refine and improve
4. **Validate** → Test with validation subset
5. **Document** → Record findings and decisions
6. **Promote** → Move stable components to production

## ⚠️ Important Notes

- **This is for development only** - not for production runs
- **Use small datasets** for faster iteration
- **Experiment freely** - this is your sandbox
- **Document everything** - findings will inform production design
- **Keep it organized** - clean up regularly

## 🔄 Moving to Production

When components are stable and tested:
1. **Copy stable code** to `../simulation_production/`
2. **Update documentation** with final specifications
3. **Create production configuration** files
4. **Test with full dataset** before production use

---
*This development environment is your workspace for building the CedarSim simulation model.*
