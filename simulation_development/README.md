# CedarSim Simulation Development

This directory contains the development of the CedarSim hospital inventory management simulation system.

## Current Status: Model Building Phase

We are implementing an object-oriented simulation framework with the following key components:

### Core Architecture

#### Resource Hierarchy
- **Resource** (Abstract Base Class): All simulation entities inherit from this
- **Location** (Resource): Container for PARs and Perpetual warehouse
- **SKU** (Resource): Individual medical supplies nested within locations

#### Design Patterns Implemented
- **Observer Pattern**: Inventory change notifications
- **Strategy Pattern**: Replenishment policies (Order-Up-To-Level)
- **Factory Pattern**: Resource creation
- **Manager Pattern**: System coordination

### Key Classes

#### `Resource` (Abstract Base Class)
```python
class Resource(ABC):
    def __init__(self, resource_id: str, resource_type: ResourceType)
    def get_capacity(self) -> float
    def get_current_level(self) -> float
    def add_observer(self, observer: InventoryObserver)
    def notify_observers(self, old_level: float, new_level: float)
```

#### `Location` (Inherits from Resource)
```python
class Location(Resource):
    def __init__(self, location_id: str, location_type: str, max_capacity: float)
    def add_sku(self, sku: SKU)
    def get_sku(self, sku_id: str) -> Optional[SKU]
```

#### `SKU` (Inherits from Resource)
```python
class SKU(Resource):
    def __init__(self, sku_id: str, location_id: str, target_level: float, lead_time: float)
    def set_inventory_level(self, new_level: float)
    def add_emergency_connection(self, par_sku: SKU)
    def allocate_emergency_supply(self, demand: float) -> float
```

#### `SimulationManager`
```python
class SimulationManager:
    def add_location(self, location: Location)
    def add_sku(self, sku: SKU)
    def setup_emergency_connections(self)
    def get_system_status(self) -> Dict[str, Any]
```

### Next Steps: SimPy Integration

The current object-oriented design will be adapted to work with SimPy's process-based simulation approach. Key adaptations needed:

1. **Process-Based Simulation**: Convert daily time-step logic to SimPy processes
2. **Event-Driven Architecture**: Use SimPy events for demand, replenishment, and emergency transfers
3. **Resource Management**: Integrate with SimPy's resource management capabilities
4. **Time Management**: Use SimPy's time system for lead times and scheduling

### Data Integration

The simulation will integrate with the following data sources:
- `../data/final/csv_complete/Complete_Input_Dataset_20250913_220808.csv` (5,941 SKUs)
- `../data/final/csv_complete/Validation_Input_Subset_20250913_220808.csv` (74 SKUs)
- `../data/final/csv_complete/02_Demand_Data_Clean_Complete.csv` (Historical demand)

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```python
from core_models import SimulationManager, ResourceFactory

# Create simulation manager
manager = SimulationManager()

# Create locations and SKUs
perpetual = ResourceFactory.create_location("PERPETUAL", "Perpetual")
ed_location = ResourceFactory.create_location("ED", "PAR")

# Add to simulation
manager.add_location(perpetual)
manager.add_location(ed_location)

# Set up emergency connections
manager.setup_emergency_connections()
```

### Development Status

- ✅ **Object-Oriented Design**: Core classes implemented
- ✅ **Design Patterns**: Observer, Strategy, Factory, Manager patterns
- ✅ **Resource Hierarchy**: Location and SKU inheritance from Resource
- ✅ **Data Validation**: Confirmed 99.5% coverage of original demand data
- 🚧 **SimPy Integration**: Ready to implement process-based approach
- ⏳ **Data Integration**: Pending - CSV loading and validation
- ⏳ **Simulation Engine**: Pending - Weekly time-step processing
- ⏳ **Mathematical Model**: Pending - Core equations implementation
- ⏳ **Validation Framework**: Pending - Comparison with analytical solution

### Key Features

- **Weekly Time Step**: Simulation runs on weekly cycles matching historical data
- **Lead Time Conversion**: Automatic conversion from days to weeks (days/7)
- **Two-Tier Safety System**: Normal replenishment + emergency backup
- **Order-Up-To-Level Policy**: Deterministic replenishment strategy
- **Emergency Connections**: SKU-level connections between perpetual and PARs
- **Inventory Tracking**: Real-time inventory level monitoring
- **Observer Pattern**: Loose coupling for inventory change notifications
- **Extensible Design**: Easy to add new resource types and strategies

### Business Value

This simulation will help Cedars-Sinai Marina del Rey Hospital:
- Optimize inventory levels across 18 PAR locations
- Minimize stockouts while reducing holding costs
- Test emergency scenarios and preparedness
- Make data-driven inventory management decisions