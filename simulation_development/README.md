# CedarSim Simulation Development

This directory contains the development of the CedarSim hospital inventory management simulation system.

## Current Status: Pre-Simulation Structure Framework Complete

We have implemented the pre-simulation structure framework with the following key components:

**ARCHITECTURE SEPARATION:**
- **This module**: Creates OBJECT STRUCTURE and NETWORK TOPOLOGY
- **SimPy module**: Handles actual SIMULATION EXECUTION (separate)
- **AntologyGenerator**: Pre-simulation setup tool (NOT part of simulator)

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

#### Discrete Event Data Structures
```python
@dataclass
class DeliveryData:
    sku_id: str
    quantity: float
    time: int
    source: str = "external_supplier"

@dataclass
class DemandData:
    sku_id: str
    quantity: float
    time: int
    location_id: str
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
    def fulfill_demand(self, env, delay=0)  # Core process - SimPy generator
    def place_orders(self, env, lead_time)  # Core process - SimPy generator
    def receive_deliveries(self, env, delay=0)  # Core process - SimPy generator
    def _check_reorder(self) -> bool  # Private method
    def _calculate_order_quantity(self) -> float  # Private method
    def _trigger_emergency_replenishment(self, stockout_amount)  # Private method
    def set_connected_perpetual_sku(self, perpetual_sku: SKU)  # For PAR SKUs
    def add_emergency_connection(self, par_sku: SKU)  # For perpetual SKUs
    def allocate_emergency_supply(self, demand: float) -> float  # Can go negative
```

#### `AntologyGenerator` (Pre-Simulation Setup)
```python
class AntologyGenerator:
    def add_location(self, location: Location)
    def add_sku(self, sku: SKU)
    def generate_network_connections(self)  # Generates network topology
    def finalize_network(self)  # Prepares structure for simulation handoff
    def get_network_status(self) -> Dict[str, Any]
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

### Core Components Implemented

The pre-simulation structure framework is now complete with the following components:

1. **SKU Business Logic**:
   - Inventory management and stockout handling
   - Emergency supply allocation (can go negative for perpetual SKUs)
   - Lead time conversion (days to fractional weeks)
   - Bidirectional connection management

2. **Location Reporting Methods**:
   - `get_*()` methods for comprehensive reporting and analytics
   - Passive container approach with rich data access
   - Network topology reporting

3. **AntologyGenerator Pre-Simulation Setup**:
   - `generate_network_connections()`: Creates PAR-perpetual network topology
   - `finalize_network()`: Prepares structure for simulation handoff
   - **Note**: This class is NOT part of the simulator - it creates the structure

4. **Key Features**:
   - **Object Structure Creation**: Locations, SKUs, and their relationships
   - **Network Topology**: Bidirectional PAR-perpetual connections for emergency supply
   - **Negative Inventory Support**: Perpetual SKUs can go negative to maintain service levels
   - **Hospital-Level Stockout Tracking**: Records when entire system is under stress
   - **Pre-Simulation Setup**: Prepares structure for SimPy simulation handoff

### Data Integration (Pre-Simulation Setup)

The AntologyGenerator will load data from the following sources to create the object structure:
- `../data/final/csv_complete/Complete_Input_Dataset_20250913_220808.csv` (5,941 SKUs)
- `../data/final/csv_complete/Validation_Input_Subset_20250913_220808.csv` (74 SKUs)
- `../data/final/csv_complete/02_Demand_Data_Clean_Complete.csv` (Historical demand)

**Note**: This data loading happens during PRE-SIMULATION setup, not during simulation execution.

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```python
from core_models import AntologyGenerator, ResourceFactory

# STEP 1: Create network structure (Pre-Simulation)
antology = AntologyGenerator()

# Create locations and SKUs
perpetual = ResourceFactory.create_location("PERPETUAL", "Perpetual")
ed_location = ResourceFactory.create_location("ED", "PAR")

# Add to network
antology.add_location(perpetual)
antology.add_location(ed_location)

# Generate network topology
antology.generate_network_connections()

# Finalize structure for simulation handoff
antology.finalize_network()

# STEP 2: SimPy simulation runs on top of this structure
# The simulation uses the established network connections
```

### Development Status

- ✅ **Object-Oriented Design**: Core classes implemented
- ✅ **Design Patterns**: Observer, Strategy, Factory, Manager patterns
- ✅ **Resource Hierarchy**: Location and SKU inheritance from Resource
- ✅ **Data Validation**: Confirmed 99.5% coverage of original demand data
- ✅ **Pre-Simulation Structure**: Object structure and network topology complete
- ✅ **Mathematical Model**: Business logic formulas implemented
- ✅ **Network Topology**: PAR-perpetual connections established
- ✅ **AntologyGenerator**: Pre-simulation setup tool complete
- ✅ **Bidirectional Connections**: PAR-perpetual SKU communication implemented
- ✅ **Negative Inventory Support**: Perpetual SKUs can go negative for emergency supply
- ⏳ **Data Integration**: Pending - CSV loading into AntologyGenerator
- ⏳ **SimPy Integration**: Ready to implement process-based simulation (separate module)
- ⏳ **SimPy Generators**: Pending - Create SKU process generators for simulation execution
- ⏳ **Validation Framework**: Pending - Comparison with analytical solution

### Key Features

- **Object Structure Creation**: Locations, SKUs, and their relationships
- **Network Topology**: Bidirectional PAR-perpetual connections for emergency supply
- **Lead Time Conversion**: Automatic conversion from days to fractional weeks (days/7) for precise timing
- **Two-Tier Safety System**: Normal replenishment + emergency backup
- **Order-Up-To-Level Policy**: Deterministic replenishment strategy
- **Emergency Connections**: SKU-level connections between perpetual and PARs
- **Inventory Tracking**: Real-time inventory level monitoring
- **Pre-Simulation Setup**: Prepares structure for SimPy simulation handoff
- **Observer Pattern**: Loose coupling for inventory change notifications
- **Extensible Design**: Easy to add new resource types and strategies
- **Architecture Separation**: Clear separation between structure creation and simulation execution

### Business Value

This simulation will help Cedars-Sinai Marina del Rey Hospital:
- Optimize inventory levels across 18 PAR locations
- Minimize stockouts while reducing holding costs
- Test emergency scenarios and preparedness
- Make data-driven inventory management decisions