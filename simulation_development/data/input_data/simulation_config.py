#!/usr/bin/env python3
"""
CedarSim Simulation Configuration

This file contains configuration parameters for the CedarSim simulation.
"""

# Simulation Parameters
SIMULATION_CONFIG = {
    # Time Parameters
    'time_horizon_days': 365,  # 1 year simulation
    'time_step_days': 1,       # Daily simulation cycles
    'warmup_days': 30,         # Warmup period before data collection
    
    # Service Level Parameters
    'target_service_level': 0.98,  # 98% service level
    'z_score': 2.05,               # Z-score for 98% service level
    
    # Inventory Parameters
    'initial_inventory_factor': 1.0,  # Initial inventory as multiple of target
    'safety_stock_factor': 1.0,       # Safety stock multiplier
    
    # Replenishment Parameters
    'replenishment_policy': 'order_up_to_level',  # Order-Up-To-Level policy
    'order_frequency_days': 1,        # Check for orders daily
    'emergency_replenishment': True,   # Enable emergency supply from perpetual
    
    # Performance Tracking
    'track_stockouts': True,
    'track_emergency_transfers': True,
    'track_inventory_levels': True,
    'track_order_frequency': True,
    
    # Output Parameters
    'output_frequency_days': 7,       # Weekly output reports
    'detailed_logging': False,        # Enable detailed simulation logs
}

# Data File Paths (relative to simulation_development directory)
DATA_PATHS = {
    'sku_inventory': 'data/input_data/sku_inventory_data.csv',
    'historical_demand': 'data/input_data/historical_demand_data.csv',
    'validation_subset': 'data/input_data/validation_subset_data.csv',
}

# Location Configuration
LOCATION_CONFIG = {
    'perpetual_location': 'PERPETUAL',
    'par_locations': [
        'Level 1 Perpetual_1400',
        'Level 1 Facilities/Biomed_1232',
        'Level 1 EVS_1321',
        'Level 1 ED_1229',
        'Level 1 Imaging_1329',
        'Level 2 Pharm_2500',
        'Level 2 Surgery/Procedures/PACU_2209_2321_2323_2450_2200B_2450A',
        'Level 3 Sterile Processing_3307_3309',
        'Level 3 Food Service',
        'Level 3 Admin',
        'Level 3 Central Lab_3411',
        'Respiratory Therapy',
        'Level 5 Observation, Medical Tele & Non-Tele_5206',
        'Level 6 Telemetry, Cardiac & Stroke',
        'Level 7 PCU',
        'Level 7 ICU',
        'Level 8 M/S Overflow, VIP & Int\'l Med',
        'Level 9 Surgical, Non-Infectious'
    ]
}

# Validation Parameters
VALIDATION_CONFIG = {
    'use_validation_subset': True,    # Start with validation subset
    'validation_skus': 74,           # Number of validation SKUs
    'compare_with_analytical': True,  # Compare with pre-calculated safety stock
    'tolerance_percentage': 5.0,      # 5% tolerance for validation
}

# Output Configuration
OUTPUT_CONFIG = {
    'results_directory': 'simulation_results',
    'reports_directory': 'simulation_reports',
    'logs_directory': 'simulation_logs',
    'create_directories': True,
    'save_detailed_results': True,
    'generate_visualizations': True,
}

def get_config():
    """Get the complete simulation configuration."""
    return {
        'simulation': SIMULATION_CONFIG,
        'data_paths': DATA_PATHS,
        'locations': LOCATION_CONFIG,
        'validation': VALIDATION_CONFIG,
        'output': OUTPUT_CONFIG
    }

def print_config():
    """Print the current configuration."""
    config = get_config()
    
    print("=" * 60)
    print("CEDARSIM SIMULATION CONFIGURATION")
    print("=" * 60)
    
    print(f"\n📅 Time Parameters:")
    print(f"   Simulation Horizon: {config['simulation']['time_horizon_days']} days")
    print(f"   Time Step: {config['simulation']['time_step_days']} day(s)")
    print(f"   Warmup Period: {config['simulation']['warmup_days']} days")
    
    print(f"\n🎯 Service Level:")
    print(f"   Target Service Level: {config['simulation']['target_service_level']*100}%")
    print(f"   Z-Score: {config['simulation']['z_score']}")
    
    print(f"\n📦 Inventory Policy:")
    print(f"   Replenishment Policy: {config['simulation']['replenishment_policy']}")
    print(f"   Emergency Replenishment: {config['simulation']['emergency_replenishment']}")
    
    print(f"\n📊 Data Files:")
    for name, path in config['data_paths'].items():
        print(f"   {name}: {path}")
    
    print(f"\n🏥 Locations:")
    print(f"   Perpetual: {config['locations']['perpetual_location']}")
    print(f"   PAR Locations: {len(config['locations']['par_locations'])}")
    
    print(f"\n✅ Validation:")
    print(f"   Use Validation Subset: {config['validation']['use_validation_subset']}")
    print(f"   Validation SKUs: {config['validation']['validation_skus']}")
    
    print("=" * 60)

if __name__ == "__main__":
    print_config()
