# CedarSim Dashboard Frontend Specification

## 🎯 **Project Overview**
A minimalistic, elegant dashboard for visualizing hospital inventory management simulation with SKU-specific analysis capabilities.

## **Design Philosophy**
- **Minimalistic & Elegant**: Clean, professional interface
- **Hospital-Centric**: Vertical 2D layout showing hospital levels
- **SKU-Focused**: Deep dive into individual SKU behavior across PARs
- **Interactive**: Real-time selection and analysis

## **Main Dashboard Layout**

### **Header Section**
```
┌─────────────────────────────────────────────────────────────┐
│  🏥 CEDARSIM INVENTORY DASHBOARD                           │
│  [PAR Dropdown ▼] [SKU Dropdown ▼] [Time: 1-52] [▶️ Run]  │
└─────────────────────────────────────────────────────────────┘
```

### **Two-Panel Layout**

#### **Left Panel: Vertical Hospital Layout (60% width)**
```
┌─────────────────────────────────────────────────────────────┐
│                    HOSPITAL LEVELS                         │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 9: ICU, PCU, Telemetry                       │   │
│  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                   │   │
│  │ │ ICU │ │ PCU │ │Tele │ │Obs │                   │   │
│  │ └─────┘ └─────┘ └─────┘ └─────┘                   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 8: Observation, Medical Tele                 │   │
│  │ ┌─────┐ ┌─────┐ ┌─────┐                           │   │
│  │ │Obs │ │Med │ │Tele │                           │   │
│  │ └─────┘ └─────┘ └─────┘                           │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 7: ICU                                       │   │
│  │ ┌─────┐                                             │   │
│  │ │ ICU │                                             │   │
│  │ └─────┘                                             │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 6: M/S Overflow                              │   │
│  │ ┌─────┐                                             │   │
│  │ │ M/S │                                             │   │
│  │ └─────┘                                             │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 5: Observation, Medical Tele                 │   │
│  │ ┌─────┐ ┌─────┐                                   │   │
│  │ │Obs │ │Med │                                   │   │
│  │ └─────┘ └─────┘                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 4: Respiratory Therapy                       │   │
│  │ ┌─────┐                                             │   │
│  │ │Resp │                                             │   │
│  │ └─────┘                                             │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 3: Central Lab, Sterile Processing           │   │
│  │ ┌─────┐ ┌─────┐ ┌─────┐                           │   │
│  │ │Lab │ │Ster │ │Food │                           │   │
│  │ └─────┘ └─────┘ └─────┘                           │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 2: Pharmacy, Surgery/PACU                    │   │
│  │ ┌─────┐ ┌─────┐ ┌─────┐                           │   │
│  │ │Pharm│ │Surg │ │PACU │                           │   │
│  │ └─────┘ └─────┘ └─────┘                           │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 1: ED, Imaging, EVS, Facilities              │   │
│  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                   │   │
│  │ │ ED │ │Img │ │EVS │ │Fac │                   │   │
│  │ └─────┘ └─────┘ └─────┘ └─────┘                   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Level 0: PERPETUAL (Safety Stock)                  │   │
│  │ ┌─────────────────────────────────────────────────┐ │   │
│  │ │              PERPETUAL                          │ │   │
│  │ └─────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### **Right Panel: SKU Analysis (40% width)**
```
┌─────────────────────────────────────────────────────────────┐
│                    SKU ANALYSIS                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Selected: ED → SKU_001 - Bandages                  │   │
│  │ Connected PARs: 3 locations                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         INVENTORY LEVELS OVER TIME                  │   │
│  │                                                     │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ 100 ┤                                     │   │   │
│  │  │  80 ┤     ●───●───●───●───●───●───●      │   │   │
│  │  │  60 ┤   ●─●   ●─●   ●─●   ●─●   ●─●      │   │   │
│  │  │  40 ┤ ●─●       ●─●       ●─●       ●─●  │   │   │
│  │  │  20 ┤●─●           ●─●       ●─●       ●─●│   │   │
│  │  │   0 └─────────────────────────────────────┘   │   │
│  │  │     0   5  10  15  20  25  30  35  40        │   │
│  │  │           Weeks                              │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                                                     │   │
│  │  Legend:                                           │   │
│  │  ●─── Perpetual (Safety Stock)                     │   │
│  │  ●─── ED (Emergency Department)                    │   │
│  │  ●─── Surgery (Operating Room)                     │   │
│  │  ●─── ICU (Intensive Care)                         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## **Interactive Features**

### **1. Two-Level SKU Selection**
- **Step 1**: Select PAR (location) from dropdown
  - Options: All 18 PARs + Perpetual
  - Search functionality for PAR names
- **Step 2**: Select SKU from that PAR
  - Options: Only SKUs available in selected PAR
  - Search functionality for SKU names/IDs
- **Alternative**: Direct SKU search with PAR context shown

### **2. Hospital Layout Interactions**
- **Hover Effects**: Show PAR details on hover
- **Click Selection**: Click PAR to filter SKUs
- **Highlight Mode**: When SKU selected, highlight connected PARs
- **Connection Lines**: Show emergency supply paths between Perpetual and PARs

### **3. Time Series Chart**
- **Interactive Timeline**: Hover to see exact values
- **Zoom/Pan**: Navigate through time periods
- **Legend Toggle**: Show/hide specific PARs
- **Export**: Download chart as PNG/PDF

### **4. Simulation Controls**
- **Run Button**: Start simulation with current parameters
- **Time Range**: Select simulation duration (weeks 1-52)
- **Speed Control**: Fast/Medium/Slow simulation speed
- **Pause/Resume**: Control simulation execution

## **Technical Stack**

### **Frontend**
- **Framework**: React.js or Vue.js
- **Charts**: Chart.js or D3.js
- **Styling**: CSS3 with Flexbox/Grid
- **Icons**: Font Awesome or Material Icons

### **Backend**
- **API**: Python Flask
- **Data Processing**: Pandas
- **Data Source**: CSV files only (no database)
- **File Structure**: 
  - `data/final/csv_complete/Complete_Input_Dataset_20250913_220808.csv`
  - `data/final/csv_complete/Validation_Input_Subset_20250913_220808.csv`
  - `data/final/csv_complete/02_Demand_Data_Clean_Complete.csv`

### **Data Flow**
```
Frontend (React/Vue) ←→ Flask API ←→ Pandas ←→ CSV Files
```

## **Data Requirements**

### **CSV Data Structure**
- **SKU Inventory**: SKU ID, PAR locations, target levels, lead times
- **Demand Data**: Historical demand patterns by SKU and week
- **PAR Mapping**: Which SKUs are available in which PARs
- **Validation Data**: Pre-calculated safety stock levels

### **API Endpoints**
- `GET /api/pars` - List all PARs
- `GET /api/skus?par_id=<par_id>` - Get SKUs for specific PAR
- `GET /api/sku/<sku_id>/inventory` - Get inventory levels over time
- `GET /api/sku/<sku_id>/connections` - Get connected PARs
- `POST /api/simulation/run` - Run simulation with parameters

## **Visual Design Elements**

### **Color Scheme**
- **Primary**: Hospital blue (#2E86AB)
- **Secondary**: Medical green (#A23B72)
- **Accent**: Warning orange (#F18F01)
- **Background**: Clean white (#FFFFFF)
- **Text**: Dark gray (#2C3E50)

### **Typography**
- **Headers**: Bold, clean sans-serif
- **Body**: Readable sans-serif
- **Code**: Monospace for SKU IDs

### **Layout Principles**
- **Grid System**: Consistent spacing and alignment
- **Card Design**: Information grouped in clean cards
- **Responsive**: Adapts to different screen sizes
- **Minimalist**: Clean, uncluttered interface

## **Implementation Phases**

### **Phase 1: Basic Structure**
1. HTML/CSS layout with hospital levels
2. PAR/SKU dropdown selection
3. Basic Flask API with CSV data loading

### **Phase 2: Interactive Features**
1. Hospital layout interactions
2. Time series chart implementation
3. SKU connection visualization

### **Phase 3: Simulation Integration**
1. SimPy integration
2. Real-time simulation updates
3. Export functionality

## **File Structure**
```
frontend/
├── index.html
├── css/
│   ├── main.css
│   └── hospital-layout.css
├── js/
│   ├── main.js
│   ├── hospital-layout.js
│   └── chart.js
└── api/
    ├── app.py (Flask backend)
    ├── data_loader.py (Pandas CSV processing)
    └── simulation_runner.py (SimPy integration)
```

This specification provides a complete blueprint for building the CedarSim dashboard frontend with the two-level SKU selection and CSV-based data management you requested.
