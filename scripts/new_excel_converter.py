#!/usr/bin/env python3
"""
CedarSim New Excel Data Converter
================================

This script converts new Excel data format to CedarSim format by:
1. Loading new Excel data
2. Merging with existing CedarSim data using Oracle Item Number as key
3. Updating burn rates, lead times, and UOM from new data
4. Preserving all existing operational context (departments, suppliers, PAR status, level mapping)
5. Handling new items that don't exist in existing data

Usage:
    python new_excel_converter.py --input new_file.xlsx --output converted_file.xlsx
    python new_excel_converter.py --input new_file.xlsx --output converted_file.xlsx --handle-new-items
"""

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CedarSimDataConverter:
    """Converts new Excel format to CedarSim format"""
    
    def __init__(self, existing_data_path, output_dir="data/converted"):
        self.existing_data_path = Path(existing_data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'converter.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load existing data
        self.existing_data = self._load_existing_data()
        
    def _load_existing_data(self):
        """Load existing CedarSim data"""
        try:
            existing_data = pd.read_csv(self.existing_data_path)
            self.logger.info(f"Loaded existing data: {existing_data.shape}")
            return existing_data
        except Exception as e:
            self.logger.error(f"Failed to load existing data: {e}")
            raise
    
    def convert_new_data(self, new_file_path, handle_new_items=False, default_department="Unknown", default_supplier="Unknown", exclude_new_items=True):
        """
        Convert new Excel data to CedarSim format
        
        Args:
            new_file_path: Path to new Excel file
            handle_new_items: Whether to handle new items not in existing data
            default_department: Default department for new items
            default_supplier: Default supplier for new items
            exclude_new_items: Whether to exclude new items from simulation (recommended)
        """
        self.logger.info(f"Starting conversion of {new_file_path}")
        
        # Load new data
        new_data = self._load_new_data(new_file_path)
        
        # Create mapping for column names
        column_mapping = self._create_column_mapping()
        
        # Convert new data to CedarSim format
        converted_new_data = self._convert_columns(new_data, column_mapping)
        
        # Merge with existing data
        merged_data = self._merge_data(converted_new_data, handle_new_items, default_department, default_supplier, exclude_new_items)
        
        # Generate report
        self._generate_conversion_report(new_data, converted_new_data, merged_data)
        
        return merged_data
    
    def _load_new_data(self, new_file_path):
        """Load new Excel data"""
        try:
            excel_file = pd.ExcelFile(new_file_path)
            self.logger.info(f"Available sheets: {excel_file.sheet_names}")
            
            # Load first sheet (assuming single sheet for now)
            sheet_name = excel_file.sheet_names[0]
            new_data = pd.read_excel(new_file_path, sheet_name=sheet_name)
            self.logger.info(f"Loaded new data: {new_data.shape}")
            return new_data
        except Exception as e:
            self.logger.error(f"Failed to load new data: {e}")
            raise
    
    def _create_column_mapping(self):
        """Create mapping from new column names to CedarSim column names"""
        return {
            'Oracle Item Number': 'Oracle Item Number',
            'Item Description': 'Item Description',
            'unit_of_measure': 'UOM',
            'lead_time': 'Avg_Lead Time',
            'burn_rate': 'Avg Daily Burn Rate',
            'Deliver To': 'Deliver To',  # Keep as is for reference
            'Stock Units Analytical': 'Stock Units Analytical'  # Keep as is for reference
        }
    
    def _convert_columns(self, new_data, column_mapping):
        """Convert column names and data types"""
        converted_data = new_data.copy()
        
        # Rename columns
        converted_data = converted_data.rename(columns=column_mapping)
        
        # Convert data types
        if 'Avg_Lead Time' in converted_data.columns:
            converted_data['Avg_Lead Time'] = pd.to_numeric(converted_data['Avg_Lead Time'], errors='coerce')
        
        if 'Avg Daily Burn Rate' in converted_data.columns:
            converted_data['Avg Daily Burn Rate'] = pd.to_numeric(converted_data['Avg Daily Burn Rate'], errors='coerce')
        
        # Remove duplicates based on Oracle Item Number
        converted_data = converted_data.drop_duplicates(subset=['Oracle Item Number'], keep='first')
        
        self.logger.info(f"Converted data shape: {converted_data.shape}")
        return converted_data
    
    def _merge_data(self, converted_new_data, handle_new_items=False, default_department="Unknown", default_supplier="Unknown", exclude_new_items=True):
        """Merge new data with existing data"""
        
        # Find overlapping items
        existing_items = set(self.existing_data['Oracle Item Number'])
        new_items = set(converted_new_data['Oracle Item Number'])
        overlapping_items = existing_items & new_items
        new_only_items = new_items - existing_items
        existing_only_items = existing_items - new_items
        
        self.logger.info(f"Overlapping items: {len(overlapping_items)}")
        self.logger.info(f"New items only: {len(new_only_items)}")
        self.logger.info(f"Existing items only: {len(existing_only_items)}")
        
        # Log new items that will be excluded
        if exclude_new_items and len(new_only_items) > 0:
            self.logger.info(f"EXCLUDING {len(new_only_items)} new items from simulation (no demand data)")
            self.logger.info(f"Excluded items: {sorted(list(new_only_items))}")
            
            # Create detailed log of excluded items
            excluded_items_data = converted_new_data[converted_new_data['Oracle Item Number'].isin(new_only_items)]
            excluded_items_list = []
            for _, item in excluded_items_data.iterrows():
                excluded_items_list.append({
                    'Oracle Item Number': item['Oracle Item Number'],
                    'Item Description': item['Item Description'],
                    'Burn Rate': item['Avg Daily Burn Rate'],
                    'Lead Time': item['Avg_Lead Time'],
                    'UOM': item['UOM'],
                    'Reason': 'No historical demand data available'
                })
            
            # Save excluded items to CSV for reference
            excluded_df = pd.DataFrame(excluded_items_list)
            excluded_file = self.output_dir / 'excluded_new_items.csv'
            excluded_df.to_csv(excluded_file, index=False)
            self.logger.info(f"Excluded items details saved to: {excluded_file}")
        
        # Start with existing data
        merged_data = self.existing_data.copy()
        
        # Update overlapping items with new data
        for item in overlapping_items:
            # Get new data for this item
            new_item_data = converted_new_data[converted_new_data['Oracle Item Number'] == item].iloc[0]
            
            # Update existing data
            mask = merged_data['Oracle Item Number'] == item
            merged_data.loc[mask, 'Avg Daily Burn Rate'] = new_item_data['Avg Daily Burn Rate']
            merged_data.loc[mask, 'Avg_Lead Time'] = new_item_data['Avg_Lead Time']
            merged_data.loc[mask, 'UOM'] = new_item_data['UOM']
        
        # Handle new items if requested and not excluding
        if handle_new_items and not exclude_new_items and len(new_only_items) > 0:
            self.logger.info(f"Handling {len(new_only_items)} new items")
            new_items_data = self._create_new_items_data(converted_new_data, new_only_items, default_department, default_supplier)
            merged_data = pd.concat([merged_data, new_items_data], ignore_index=True)
        
        self.logger.info(f"Final merged data shape: {merged_data.shape}")
        return merged_data
    
    def _create_new_items_data(self, converted_new_data, new_only_items, default_department, default_supplier):
        """Create data for new items not in existing data"""
        
        # Get new items data
        new_items_data = converted_new_data[converted_new_data['Oracle Item Number'].isin(new_only_items)].copy()
        
        # Create template row from existing data
        template_row = self.existing_data.iloc[0].copy()
        
        # Fill with default values
        template_row['Department Name'] = default_department
        template_row['Department Number'] = 0
        template_row['Supplier Name'] = default_supplier
        template_row['On-PAR or Special Request'] = 'On-PAR'  # Default to On-PAR
        template_row['Medline item? Y/N'] = 'N'  # Default to non-Medline
        
        # Clear all level mappings (set to null)
        level_columns = [col for col in template_row.index if 'level' in col.lower()]
        for col in level_columns:
            template_row[col] = np.nan
        
        # Create rows for new items
        new_rows = []
        for _, new_item in new_items_data.iterrows():
            row = template_row.copy()
            row['Oracle Item Number'] = new_item['Oracle Item Number']
            row['Item Description'] = new_item['Item Description']
            row['UOM'] = new_item['UOM']
            row['Avg Daily Burn Rate'] = new_item['Avg Daily Burn Rate']
            row['Avg_Lead Time'] = new_item['Avg_Lead Time']
            new_rows.append(row)
        
        return pd.DataFrame(new_rows)
    
    def _generate_conversion_report(self, original_new_data, converted_new_data, merged_data):
        """Generate conversion report"""
        
        report = {
            'conversion_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'original_new_data_shape': original_new_data.shape,
            'converted_new_data_shape': converted_new_data.shape,
            'existing_data_shape': self.existing_data.shape,
            'final_merged_data_shape': merged_data.shape,
            'overlapping_items': len(set(original_new_data['Oracle Item Number']) & set(self.existing_data['Oracle Item Number'])),
            'new_items_only': len(set(original_new_data['Oracle Item Number']) - set(self.existing_data['Oracle Item Number'])),
            'existing_items_only': len(set(self.existing_data['Oracle Item Number']) - set(original_new_data['Oracle Item Number']))
        }
        
        # Save report
        report_file = self.output_dir / 'conversion_report.json'
        import json
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Conversion report saved to: {report_file}")
        
        # Print summary
        print("\n" + "="*60)
        print("CONVERSION SUMMARY")
        print("="*60)
        print(f"Original new data: {report['original_new_data_shape']}")
        print(f"Converted new data: {report['converted_new_data_shape']}")
        print(f"Existing data: {report['existing_data_shape']}")
        print(f"Final merged data: {report['final_merged_data_shape']}")
        print(f"Overlapping items: {report['overlapping_items']}")
        print(f"New items only: {report['new_items_only']}")
        print(f"Existing items only: {report['existing_items_only']}")
        print("="*60)
    
    def save_converted_data(self, merged_data, output_file):
        """Save converted data to Excel file"""
        try:
            # Create output file path
            output_path = self.output_dir / output_file
            
            # Save to Excel
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Main data sheet
                merged_data.to_excel(writer, sheet_name='SKU_Inventory_Data', index=False)
                
                # Create summary sheet
                summary_data = {
                    'Metric': ['Total SKUs', 'Overlapping Items', 'New Items Only', 'Existing Items Only'],
                    'Count': [
                        len(merged_data),
                        len(set(merged_data['Oracle Item Number']) & set(self.existing_data['Oracle Item Number'])),
                        len(set(merged_data['Oracle Item Number']) - set(self.existing_data['Oracle Item Number'])),
                        len(set(self.existing_data['Oracle Item Number']) - set(merged_data['Oracle Item Number']))
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Conversion_Summary', index=False)
            
            self.logger.info(f"Converted data saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to save converted data: {e}")
            raise

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='Convert new Excel data to CedarSim format')
    parser.add_argument('--input', required=True, help='Path to new Excel file')
    parser.add_argument('--output', required=True, help='Output filename')
    parser.add_argument('--existing-data', default='data/final/csv_complete/01_SKU_Inventory_Final_Complete.csv', 
                       help='Path to existing CedarSim data')
    parser.add_argument('--handle-new-items', action='store_true', 
                       help='Handle new items not in existing data')
    parser.add_argument('--default-department', default='Unknown', 
                       help='Default department for new items')
    parser.add_argument('--default-supplier', default='Unknown', 
                       help='Default supplier for new items')
    
    args = parser.parse_args()
    
    # Create converter
    converter = CedarSimDataConverter(args.existing_data)
    
    # Convert data
    merged_data = converter.convert_new_data(
        args.input, 
        handle_new_items=args.handle_new_items,
        default_department=args.default_department,
        default_supplier=args.default_supplier
    )
    
    # Save converted data
    output_path = converter.save_converted_data(merged_data, args.output)
    print(f"\n✅ Conversion complete! Output saved to: {output_path}")

if __name__ == "__main__":
    main()
