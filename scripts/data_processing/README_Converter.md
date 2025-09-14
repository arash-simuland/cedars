# CedarSim New Excel Data Converter

## Overview
This converter transforms new Excel data format into CedarSim format by merging with existing data and preserving all operational context.

## What It Does

### ✅ **Preserves All Critical Data**
- **Level Mapping**: All 17 level columns from existing data
- **Department Info**: Department Name & Number
- **Supplier Info**: Supplier Name
- **PAR Status**: On-PAR or Special Request
- **Medline Status**: Medline item? Y/N

### 🔄 **Updates From New Data**
- **Burn Rates**: `burn_rate` → `Avg Daily Burn Rate`
- **Lead Times**: `lead_time` → `Avg_Lead Time`
- **UOM**: `unit_of_measure` → `UOM`

### 🆕 **Handles New Items**
- Creates new items with default values
- Preserves all existing items
- Maintains data integrity

## Usage

### **Simple Usage**
```bash
python convert_new_data.py
```

### **Advanced Usage**
```bash
python scripts/data_processing/new_excel_converter.py \
    --input data/archive/original/2025-09-12_MDRH_Item_List.xlsx \
    --output CedarSim_Converted_Data.xlsx \
    --handle-new-items \
    --default-department "Unknown" \
    --default-supplier "Unknown"
```

### **Programmatic Usage**
```python
from scripts.data_processing.new_excel_converter import CedarSimDataConverter

# Create converter
converter = CedarSimDataConverter('data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv')

# Convert data
merged_data = converter.convert_new_data(
    'data/archive/original/2025-09-12_MDRH_Item_List.xlsx',
    handle_new_items=True,
    default_department="Unknown",
    default_supplier="Unknown"
)

# Save result
output_path = converter.save_converted_data(merged_data, 'CedarSim_Converted_Data.xlsx')
```

## Input/Output

### **Input Files**
- **New Excel File**: `2025-09-12_MDRH_Item_List.xlsx`
- **Existing Data**: `data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv`

### **Output Files**
- **Converted Data**: `CedarSim_Converted_Data.xlsx`
- **Conversion Report**: `data/converted/conversion_report.json`
- **Log File**: `data/converted/converter.log`

## Column Mapping

| **New Format** | **CedarSim Format** | **Action** |
|----------------|---------------------|------------|
| `Oracle Item Number` | `Oracle Item Number` | ✅ Keep |
| `Item Description` | `Item Description` | ✅ Keep |
| `unit_of_measure` | `UOM` | 🔄 Rename |
| `lead_time` | `Avg_Lead Time` | 🔄 Rename |
| `burn_rate` | `Avg Daily Burn Rate` | 🔄 Rename |
| `Deliver To` | `Deliver To` | ✅ Keep (reference) |
| `Stock Units Analytical` | `Stock Units Analytical` | ✅ Keep (reference) |

## Data Processing Logic

### **1. For Overlapping Items (93.4%)**
- Keep all existing operational data (departments, suppliers, PAR status, level mapping)
- Update burn rates, lead times, and UOM from new data
- Preserve data integrity

### **2. For New Items (6.6%)**
- Create new records with default values
- Set default department and supplier
- Clear level mappings (needs manual assignment)
- Use new burn rates, lead times, and UOM

### **3. For Existing-Only Items**
- Keep unchanged (no updates needed)

## Output Structure

### **Excel File (2 Sheets)**
1. **SKU_Inventory_Data**: Complete merged dataset
2. **Conversion_Summary**: Statistics and metrics

### **JSON Report**
```json
{
  "conversion_date": "2025-01-XX XX:XX:XX",
  "original_new_data_shape": [5313, 7],
  "converted_new_data_shape": [3086, 7],
  "existing_data_shape": [5941, 28],
  "final_merged_data_shape": [5941, 28],
  "overlapping_items": 2883,
  "new_items_only": 203,
  "existing_items_only": 3058
}
```

## Benefits

### ✅ **Reusable**
- Can be used for any future data in the same format
- Handles different file names and locations
- Configurable parameters

### ✅ **Safe**
- Preserves all existing operational context
- Creates backups and logs
- Validates data integrity

### ✅ **Complete**
- Handles all data scenarios
- Generates comprehensive reports
- Maintains audit trail

## Example Output

```
🔄 Converting new Excel data to CedarSim format...

============================================================
CONVERSION SUMMARY
============================================================
Original new data: (5313, 7)
Converted new data: (3086, 7)
Existing data: (5941, 28)
Final merged data: (5941, 28)
Overlapping items: 2883
New items only: 203
Existing items only: 3058
============================================================

✅ Conversion complete!
📁 Output saved to: data/converted/CedarSim_Converted_Data.xlsx
📊 Final data shape: (5941, 28)
```

## Next Steps

1. **Review converted data** for accuracy
2. **Manually assign departments** for new items if needed
3. **Update level mappings** for new items
4. **Run CedarSim pipeline** with converted data
5. **Validate results** against existing data

## Troubleshooting

### **Common Issues**
- **File not found**: Check file paths
- **Column mismatch**: Verify Excel file format
- **Memory issues**: Process in smaller batches
- **Data type errors**: Check numeric columns

### **Logs**
- Check `data/converted/converter.log` for detailed logs
- Review `data/converted/conversion_report.json` for statistics
- Use verbose mode for debugging

## Support

For issues or questions:
1. Check the log files
2. Review the conversion report
3. Verify input file formats
4. Test with sample data first
