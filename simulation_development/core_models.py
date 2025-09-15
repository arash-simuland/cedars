"""
CedarSim Core Models - Object-Oriented Simulation Framework

This module implements the core resource classes and design patterns for the
CedarSim hospital inventory management simulation.

Key Classes:
- Resource: Abstract base class for all resources
- Location: Container resource for PARs and Perpetual warehouse
- SKU: Nested resource representing individual medical supplies
- SimulationManager: Coordinates the entire simulation system

Design Patterns:
- Observer Pattern: For inventory change notifications
- Strategy Pattern: For replenishment policies
- Factory Pattern: For resource creation
- Manager Pattern: For system coordination
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResourceType(Enum):
    """Enumeration of resource types in the simulation."""
    LOCATION = "location"
    SKU = "sku"

@dataclass
class ResourceState:
    """State information for a resource."""
    current_level: float
    capacity: float
    last_updated: float

class InventoryObserver(ABC):
    """Abstract observer for inventory changes."""
    
    @abstractmethod
    def on_inventory_change(self, resource: 'Resource', old_level: float, new_level: float):
        """Called when a resource's inventory level changes."""
        pass

class Resource(ABC):
    """Abstract base class for all resources in the simulation."""
    
    def __init__(self, resource_id: str, resource_type: ResourceType):
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.state = ResourceState(0, 0, 0)
        self.observers: List[InventoryObserver] = []
        logger.debug(f"Created {resource_type.value} resource: {resource_id}")
    
    @abstractmethod
    def get_capacity(self) -> float:
        """Get the capacity of this resource."""
        pass
    
    @abstractmethod
    def get_current_level(self) -> float:
        """Get the current level of this resource."""
        pass
    
    def add_observer(self, observer: InventoryObserver):
        """Add an observer for inventory changes."""
        self.observers.append(observer)
        logger.debug(f"Added observer to {self.resource_id}")
    
    def notify_observers(self, old_level: float, new_level: float):
        """Notify all observers of inventory changes."""
        for observer in self.observers:
            observer.on_inventory_change(self, old_level, new_level)

class ReplenishmentStrategy(ABC):
    """Abstract strategy for replenishment policies."""
    
    @abstractmethod
    def should_reorder(self, sku: 'SKU') -> bool:
        """Determine if a SKU should be reordered."""
        pass
    
    @abstractmethod
    def calculate_order_quantity(self, sku: 'SKU') -> float:
        """Calculate how much to order for a SKU."""
        pass

class OrderUpToLevelStrategy(ReplenishmentStrategy):
    """Order-up-to-level replenishment strategy."""
    
    def should_reorder(self, sku: 'SKU') -> bool:
        """Reorder when inventory drops below target level."""
        return sku.get_current_level() < sku.target_level
    
    def calculate_order_quantity(self, sku: 'SKU') -> float:
        """Order up to target level."""
        return max(0, sku.target_level - sku.get_current_level())

class Location(Resource):
    """Location resource representing PARs and Perpetual warehouse."""
    
    def __init__(self, location_id: str, location_type: str, max_capacity: float = float('inf')):
        super().__init__(location_id, ResourceType.LOCATION)
        self.location_type = location_type  # "PAR" or "Perpetual"
        self.max_capacity = max_capacity
        self.skus: Dict[str, SKU] = {}
        self.replenishment_strategy: ReplenishmentStrategy = OrderUpToLevelStrategy()
        logger.info(f"Created {location_type} location: {location_id}")
    
    def add_sku(self, sku: 'SKU'):
        """Add a SKU to this location."""
        self.skus[sku.resource_id] = sku
        sku.add_observer(self)
        logger.debug(f"Added SKU {sku.resource_id} to location {self.resource_id}")
    
    def get_sku(self, sku_id: str) -> Optional['SKU']:
        """Get a SKU by ID from this location."""
        return self.skus.get(sku_id)
    
    def get_capacity(self) -> float:
        """Get the maximum capacity of this location."""
        return self.max_capacity
    
    def get_current_level(self) -> float:
        """Get the total current inventory level of all SKUs in this location."""
        return sum(sku.get_current_level() for sku in self.skus.values())
    
    def on_inventory_change(self, resource: Resource, old_level: float, new_level: float):
        """React to inventory changes in contained SKUs."""
        # Location can react to SKU inventory changes
        self.state.current_level = self.get_current_level()
        self.notify_observers(self.get_current_level(), self.get_current_level())

class SKU(Resource):
    """SKU resource representing individual medical supplies."""
    
    def __init__(self, sku_id: str, location_id: str, target_level: float = 0, 
                 lead_time: float = 0, demand_rate: float = 0):
        super().__init__(sku_id, ResourceType.SKU)
        self.location_id = location_id
        self.target_level = target_level
        self.lead_time = lead_time
        self.demand_rate = demand_rate
        self.connected_par_skus: List['SKU'] = []  # For perpetual SKUs only
        self._current_inventory_level = 0
        logger.debug(f"Created SKU {sku_id} in location {location_id}")
    
    def get_capacity(self) -> float:
        """Get the target level (capacity) of this SKU."""
        return self.target_level
    
    def get_current_level(self) -> float:
        """Get the current inventory level of this SKU."""
        return self._current_inventory_level
    
    def set_inventory_level(self, new_level: float):
        """Set the inventory level and notify observers."""
        old_level = self._current_inventory_level
        self._current_inventory_level = max(0, new_level)  # Prevent negative
        self.state.current_level = self._current_inventory_level
        self.state.last_updated = 0  # Will be updated by simulation time
        self.notify_observers(old_level, self._current_inventory_level)
        logger.debug(f"SKU {self.resource_id} inventory changed: {old_level} -> {self._current_inventory_level}")
    
    def add_emergency_connection(self, par_sku: 'SKU'):
        """Add an emergency connection to a PAR SKU (for perpetual SKUs only)."""
        self.connected_par_skus.append(par_sku)
        logger.debug(f"Added emergency connection from {self.resource_id} to {par_sku.resource_id}")
    
    def can_supply_emergency(self) -> bool:
        """Check if this SKU can supply emergency replenishment."""
        return len(self.connected_par_skus) > 0 and self.get_current_level() > 0
    
    def allocate_emergency_supply(self, demand: float) -> float:
        """Allocate emergency supply to connected PAR SKUs."""
        if not self.can_supply_emergency():
            return 0
        
        available = self.get_current_level()
        allocated = min(demand, available)
        
        if allocated > 0:
            self.set_inventory_level(available - allocated)
            logger.info(f"Allocated {allocated} units of {self.resource_id} for emergency supply")
        
        return allocated

class ResourceFactory:
    """Factory for creating resources."""
    
    @staticmethod
    def create_location(location_id: str, location_type: str, max_capacity: float = float('inf')) -> Location:
        """Create a new location resource."""
        return Location(location_id, location_type, max_capacity)
    
    @staticmethod
    def create_sku(sku_id: str, location_id: str, **kwargs) -> SKU:
        """Create a new SKU resource."""
        return SKU(sku_id, location_id, **kwargs)

class SimulationManager:
    """Manager class for coordinating the simulation system."""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.sku_registry: Dict[str, List[SKU]] = {}  # SKU ID -> List of SKU objects
        self.observers: List[InventoryObserver] = []
        logger.info("Initialized SimulationManager")
    
    def add_location(self, location: Location):
        """Add a location to the simulation."""
        self.locations[location.resource_id] = location
        location.add_observer(self)
        logger.info(f"Added location: {location.resource_id}")
    
    def add_sku(self, sku: SKU):
        """Add a SKU to the simulation."""
        if sku.resource_id not in self.sku_registry:
            self.sku_registry[sku.resource_id] = []
        self.sku_registry[sku.resource_id].append(sku)
        sku.add_observer(self)
        logger.debug(f"Added SKU: {sku.resource_id}")
    
    def get_perpetual_sku(self, sku_id: str) -> Optional[SKU]:
        """Get a SKU from the perpetual location."""
        perpetual_location = self.locations.get("PERPETUAL")
        return perpetual_location.skus.get(sku_id) if perpetual_location else None
    
    def get_par_skus(self, sku_id: str) -> List[SKU]:
        """Get all PAR SKUs of a given type."""
        return [sku for sku in self.sku_registry.get(sku_id, []) 
                if sku.location_id != "PERPETUAL"]
    
    def setup_emergency_connections(self):
        """Set up emergency connections between perpetual and PAR SKUs."""
        for sku_id, sku_list in self.sku_registry.items():
            perpetual_sku = self.get_perpetual_sku(sku_id)
            par_skus = self.get_par_skus(sku_id)
            
            if perpetual_sku and par_skus:
                for par_sku in par_skus:
                    perpetual_sku.add_emergency_connection(par_sku)
        
        logger.info("Emergency connections established")
    
    def on_inventory_change(self, resource: Resource, old_level: float, new_level: float):
        """Handle inventory changes at the system level."""
        logger.debug(f"System-level inventory change: {resource.resource_id} {old_level} -> {new_level}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the entire system."""
        status = {
            "total_locations": len(self.locations),
            "total_skus": sum(len(sku_list) for sku_list in self.sku_registry.values()),
            "locations": {}
        }
        
        for location_id, location in self.locations.items():
            status["locations"][location_id] = {
                "type": location.location_type,
                "total_inventory": location.get_current_level(),
                "sku_count": len(location.skus)
            }
        
        return status

# Example usage and testing
if __name__ == "__main__":
    # Create simulation manager
    manager = SimulationManager()
    
    # Create locations
    perpetual = ResourceFactory.create_location("PERPETUAL", "Perpetual", max_capacity=10000)
    ed_location = ResourceFactory.create_location("ED", "PAR", max_capacity=1000)
    
    manager.add_location(perpetual)
    manager.add_location(ed_location)
    
    # Create SKUs
    sku_001_perpetual = ResourceFactory.create_sku("SKU_001", "PERPETUAL", 
                                                   target_level=100, lead_time=2.0)
    sku_001_ed = ResourceFactory.create_sku("SKU_001", "ED", 
                                           target_level=50, lead_time=1.5)
    
    manager.add_sku(sku_001_perpetual)
    manager.add_sku(sku_001_ed)
    
    # Add SKUs to locations
    perpetual.add_sku(sku_001_perpetual)
    ed_location.add_sku(sku_001_ed)
    
    # Set up emergency connections
    manager.setup_emergency_connections()
    
    # Test inventory changes
    sku_001_ed.set_inventory_level(25)
    sku_001_perpetual.set_inventory_level(75)
    
    # Print system status
    print("System Status:")
    import json
    print(json.dumps(manager.get_system_status(), indent=2))
