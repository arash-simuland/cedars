# Data Conversion Utilities

## 📁 Purpose
This directory contains utility scripts for data conversion and integration tasks.

## 📋 Scripts

### **Data Analysis Scripts**
- `analyze_missing_info.py` - Analyze missing information in datasets
- `analyze_new_excel.py` - Analyze new Excel format data
- `check_demand_for_new_items.py` - Check demand data for new items

### **Data Conversion Scripts**
- `convert_new_data.py` - Simple data converter for new Excel format
- `convert_new_data_advanced.py` - Advanced data converter with more options
- `create_complete_input_data.py` - Create complete input dataset for simulation

### **Testing Scripts**
- `test_converter.py` - Test data converter functionality
- `verify_sku_overlap.py` - Verify SKU overlap between datasets

## 🚀 Usage

### **Simple Data Conversion**
```bash
python convert_new_data.py
```

### **Advanced Data Conversion**
```bash
python convert_new_data_advanced.py --include-new-items --default-department "Pharmacy"
```

### **Create Complete Input Dataset**
```bash
python create_complete_input_data.py
```

## 📊 Output

All scripts generate output in the `data/` directory:
- **Converted data** in `data/converted/`
- **Complete datasets** in `data/final/csv_complete/`
- **Logs and reports** in respective directories

## ⚠️ Notes

- These are utility scripts for data processing
- Use the main pipeline scripts in `scripts/data_processing/` for production
- These scripts are for development and testing purposes
