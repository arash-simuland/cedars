# CedarSim Simulation Development

This directory contains the development of the CedarSim hospital inventory management simulation system.

## Current Status: Discrete Event Simulation Implementation

We have implemented a discrete event simulation framework with the following key components:

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
    def __init__(self, sku_id: str, location_id: str, target_level: float, lead_time_days: float)
    def process_demand_event(self, demand_event: DemandEvent)  # Core process
    def place_order(self)  # Core process  
    def receive_delivery(self, quantity: float)  # Core process
    def set_connected_perpetual_sku(self, perpetual_sku: SKU)  # For PAR SKUs
    def add_emergency_connection(self, par_sku: SKU)  # For perpetual SKUs
    def allocate_emergency_supply(self, demand: float) -> float  # Can go negative
```

#### `SimulationManager`
```python
class SimulationManager:
    def add_location(self, location: Location)
    def add_sku(self, sku: SKU)
    def setup_emergency_connections(self)  # Sets up bidirectional connections
    def run_week(self, week_number: int)  # Core process
    def get_system_status(self) -> Dict[str, Any]
```

#### `Location` (Reporting Methods)
```python
class Location(Resource):
    def get_inventory_levels(self) -> Dict[str, float]
    def get_demand_summary(self) -> Dict[str, float]
    def get_stockout_summary(self) -> Dict[str, float]
    def get_total_inventory(self) -> float
    def get_sku_count(self) -> int
    def get_stockout_rate(self) -> float
    def get_emergency_transfer_count(self) -> int
    def get_average_lead_time(self) -> float
    def get_demand_variance(self) -> float
```

### Core Processes Implemented

The discrete event simulation framework is now complete with the following core processes:

1. **SKU Core Processes**:
   - `process_demand_event()`: Handle demand and trigger emergency supply when needed
   - `place_order()`: Order replenishment when inventory gaps occur
   - `receive_delivery()`: Process incoming deliveries

2. **Location Reporting Methods**:
   - `get_*()` methods for comprehensive reporting and analytics
   - Passive container approach with rich data access

3. **SimulationManager Core Process**:
   - `run_week()`: Execute one week of simulation (ready for SimPy integration)

4. **Key Features**:
   - **Bidirectional SKU Connections**: PAR SKUs can request emergency supply from perpetual SKUs
   - **Negative Inventory Support**: Perpetual SKUs can go negative to maintain service levels
   - **Hospital-Level Stockout Tracking**: Records when entire system is under stress
   - **Event-Driven Architecture**: Ready for SimPy integration

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
- ✅ **Discrete Event Simulation**: Event classes and simulation engine implemented
- ✅ **Mathematical Model**: Discrete event formulas implemented
- ✅ **Event Processing**: Demand, delivery, and replenishment event handling
- ✅ **Core Processes**: SKU processes, Location reporting, SimulationManager coordination
- ✅ **Bidirectional Connections**: PAR-perpetual SKU communication implemented
- ✅ **Negative Inventory Support**: Perpetual SKUs can go negative for emergency supply
- ⏳ **Data Integration**: Pending - CSV loading and validation
- ⏳ **SimPy Integration**: Ready to implement process-based approach
- ⏳ **Validation Framework**: Pending - Comparison with analytical solution

### Key Features

- **Discrete Event Processing**: Events scheduled and processed in chronological order
- **Weekly Time Step**: Simulation runs on weekly cycles matching historical data
- **Lead Time Conversion**: Automatic conversion from days to fractional weeks (days/7) for precise timing
- **Two-Tier Safety System**: Normal replenishment + emergency backup
- **Order-Up-To-Level Policy**: Deterministic replenishment strategy
- **Emergency Connections**: SKU-level connections between perpetual and PARs
- **Inventory Tracking**: Real-time inventory level monitoring
- **Event-Driven Architecture**: Demand, delivery, and replenishment events
- **Priority Queue**: Efficient event scheduling using heapq
- **Observer Pattern**: Loose coupling for inventory change notifications
- **Extensible Design**: Easy to add new resource types and strategies

### Business Value

This simulation will help Cedars-Sinai Marina del Rey Hospital:
- Optimize inventory levels across 18 PAR locations
- Minimize stockouts while reducing holding costs
- Test emergency scenarios and preparedness
- Make data-driven inventory management decisions