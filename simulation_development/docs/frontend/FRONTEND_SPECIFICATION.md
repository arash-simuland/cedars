# CedarSim Frontend Specification

**Date**: September 17, 2025  
**Status**: ✅ **IMPLEMENTED** - SKU-centric dashboard ready

## 🎯 **Frontend Design Philosophy**

The CedarSim dashboard follows a **SKU-centric approach** where users select individual medical supplies to view their behavior across all hospital locations.

## 🏗️ **Architecture Overview**

### **Components**
- **Dashboard HTML**: Main interface with SKU selection and visualization
- **REST API**: Flask-based API serving real-time data
- **Frontend Generator**: Dynamic data generation utilities
- **Chart.js Integration**: Interactive time series visualization

### **Data Flow**
```
User Selection → API Request → AntologyGenerator → Real Data → Chart Visualization
```

## 📊 **Dashboard Features**

### **1. SKU Selection Interface**
- **Dropdown Menu**: Populated with 2,813 unique SKUs
- **Real-time Data**: Live inventory levels and demand rates
- **Search Functionality**: Quick SKU lookup by ID or description

### **2. Hospital Layout Visualization**
- **10-Level Structure**: Visual representation of hospital floors
- **SKU Presence Indicators**: `[●]` markers showing which PARs have the selected SKU
- **Location Types**: Clear distinction between PARs and Perpetual warehouse

### **3. Time Series Analysis**
- **Multi-line Charts**: Each PAR gets its own line showing SKU behavior
- **Inventory Levels**: Real-time tracking of stock levels
- **Demand Patterns**: Historical consumption visualization
- **Stockout Alerts**: Visual indicators when inventory is low

## 🔌 **API Endpoints**

### **Core Endpoints**
- `GET /` - Main dashboard page
- `GET /api/skus` - List all available SKUs
- `GET /api/sku/<sku_id>` - Get specific SKU data
- `GET /api/locations` - Get all hospital locations
- `GET /api/network` - Get network topology

### **Data Endpoints**
- `GET /api/sku/<sku_id>/inventory` - SKU inventory levels
- `GET /api/sku/<sku_id>/demand` - SKU demand patterns
- `GET /api/sku/<sku_id>/locations` - SKU location distribution
- `GET /api/validation` - Validation data for selected SKU

## 🎨 **User Interface Design**

### **Layout Structure**
```
┌─────────────────────────────────────────────────────────┐
│                    CedarSim Dashboard                   │
├─────────────────────────────────────────────────────────┤
│  SKU Selection: [Dropdown with 2,813 SKUs] [Search]    │
├─────────────────────────────────────────────────────────┤
│  Hospital Layout (10 levels with SKU indicators)       │
│  Level 1: [●] ED  [●] EVS  [●] Imaging                │
│  Level 2: [●] ICU  [●] Pharm  [●] Surgery              │
│  Level 3: [●] Medical  [●] Admin  [●] Lab              │
│  ...                                                    │
│  Perpetual: [●] Central Warehouse                      │
├─────────────────────────────────────────────────────────┤
│  Time Series Chart (Multi-line for each PAR)           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Inventory Levels Over Time                     │   │
│  │  Level 1 ED: ████████████████████████████████   │   │
│  │  Level 2 ICU: ████████████████████████████████  │   │
│  │  Level 3 Medical: ████████████████████████████  │   │
│  │  ...                                            │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### **Visual Indicators**
- **`[●]`**: SKU present at this location
- **`[○]`**: SKU not present at this location
- **Color Coding**: Different colors for each PAR location
- **Alert States**: Red for stockouts, yellow for low inventory

## 📈 **Data Visualization**

### **Chart Types**
1. **Inventory Timeline**: Multi-line chart showing stock levels over time
2. **Demand Patterns**: Bar chart showing consumption by location
3. **Network Flow**: Diagram showing emergency supply connections
4. **Validation Metrics**: Comparison with analytical safety stock

### **Interactive Features**
- **Zoom/Pan**: Navigate through time periods
- **Hover Details**: Show exact values on mouse hover
- **Legend Toggle**: Show/hide specific PAR locations
- **Time Range Selection**: Filter data by date range

## 🔧 **Technical Implementation**

### **Frontend Stack**
- **HTML5**: Semantic markup structure
- **CSS3**: Responsive design and styling
- **JavaScript**: Interactive functionality
- **Chart.js**: Data visualization library
- **Fetch API**: Asynchronous data loading

### **Backend Integration**
- **Flask**: Python web framework
- **CORS**: Cross-origin request support
- **JSON**: Data exchange format
- **RESTful**: Standard API design patterns

## 📱 **Responsive Design**

### **Breakpoints**
- **Desktop**: Full dashboard with all features
- **Tablet**: Condensed layout with essential features
- **Mobile**: Simplified view with core functionality

### **Accessibility**
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: ARIA labels and descriptions
- **Color Contrast**: WCAG compliant color schemes
- **Font Scaling**: Support for different text sizes

## 🚀 **Performance Optimization**

### **Data Loading**
- **Lazy Loading**: Load SKU data on demand
- **Caching**: Cache frequently accessed data
- **Pagination**: Handle large datasets efficiently
- **Compression**: Minimize data transfer

### **Rendering**
- **Virtual Scrolling**: Handle large lists efficiently
- **Chart Optimization**: Render only visible data points
- **Memory Management**: Clean up unused resources
- **Debouncing**: Limit API calls during user interaction

## ✅ **Implementation Status**

| **Component** | **Status** | **Features** |
|---------------|------------|--------------|
| **Dashboard HTML** | ✅ Complete | SKU selection, hospital layout, charts |
| **REST API** | ✅ Complete | 9 endpoints, real-time data |
| **Frontend Generator** | ✅ Complete | Dynamic data generation |
| **Chart Integration** | ✅ Complete | Multi-line time series |
| **Responsive Design** | ✅ Complete | Desktop, tablet, mobile |
| **Data Integration** | ✅ Complete | Real 2,813 SKU dataset |

## 🎯 **Next Steps**

1. **Simulation Integration**: Connect with SimPy simulation results
2. **Real-time Updates**: Live simulation data streaming
3. **Advanced Analytics**: Statistical analysis and reporting
4. **Export Features**: Download charts and data
5. **User Preferences**: Customizable dashboard settings

---

*This specification documents the complete frontend design and implementation for the CedarSim dashboard system.*
