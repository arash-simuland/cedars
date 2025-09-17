# CedarSim Simulation Development

This directory contains the CedarSim simulation development environment with a **SKU-centric dashboard interface** for hospital inventory management visualization.

## 🎯 **Current Status: FRONTEND SPECIFICATION COMPLETE** ✅

The frontend specification has been updated to reflect a **SKU-centric approach** where users select a single SKU and view its behavior across all PARs and Perpetual locations in the hospital system.

## 📁 Directory Structure

### `core/`
Core simulation models and business logic
- `core_models.py` - Main simulation models and algorithms
- `discrete_event_formulas.md` - Mathematical formulas and equations

### `frontend/`
Dashboard and user interface components
- `FRONTEND_SPECIFICATION.md` - **UPDATED** SKU-centric frontend design specifications
- `dashboard_api.py` - **IMPLEMENTED** API endpoints for the dashboard
- `dashboard.html` - **IMPLEMENTED** Main dashboard interface with SKU-centric design
- `frontend_generator.py` - **IMPLEMENTED** Dynamic frontend generation utilities

### `data/`
Input data, configuration, and requirements
- `input_data/` - Simulation input datasets
  - `historical_demand_data.csv` - Historical demand patterns
  - `sku_inventory_data.csv` - SKU inventory information
  - `validation_subset_data.csv` - Validation test data
  - `load_input_data.py` - Data loading utilities
  - `simulation_config.py` - Simulation configuration
  - `README.md` - Data documentation
- `requirements.txt` - Python dependencies
- `requirements_dashboard.txt` - Dashboard-specific dependencies

### `docs/`
Documentation and specifications
- `ARCHITECTURE.md` - System architecture documentation
- `README.md` - This file

## 🚀 Getting Started

1. **Install Dependencies**: Navigate to the `data/` folder and install requirements
2. **Configure Data**: Review and update `data/input_data/simulation_config.py`
3. **Run Simulation**: Execute core models from the `core/` directory
4. **View Dashboard**: Open `frontend/dashboard.html` in a web browser (✅ **IMPLEMENTED**)

## 🎨 **Frontend Design Philosophy**

The dashboard follows a **SKU-centric approach**:

- **Primary Selection**: Users select ONE SKU from a dropdown
- **Hospital Visualization**: Shows which PARs have that SKU (with `[●]` indicators)
- **Time Series Analysis**: Displays the SKU's inventory levels across ALL connected PARs over time
- **Interactive Layout**: 9-level hospital layout with visual indicators for SKU presence
- **Multi-line Charts**: Each PAR gets its own line showing the SKU's behavior

## 📋 Development Workflow

- **Core Development**: Work in `core/` for simulation logic
- **Frontend Development**: Work in `frontend/` for SKU-centric dashboard features
- **Data Management**: Work in `data/` for input data and configuration
- **Documentation**: Update files in `docs/` as needed

## 🔧 Maintenance

This structure provides clear separation of concerns and makes the codebase easier to navigate, maintain, and extend.
