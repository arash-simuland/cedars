"""
CedarSim Core Models - Discrete Event Simulation Framework

This module implements the core resource classes and processes for the
CedarSim hospital inventory management discrete event simulation.

Key Classes:
- Resource: Abstract base class for all resources
- Location: Container resource for PARs and Perpetual warehouse with reporting methods
- SKU: Individual medical supplies with discrete event processing capabilities
- SimulationManager: Simplified coordinator for the simulation system
- DiscreteEventSimulation: Event-driven simulation engine

Core Processes:
- SKU.process_demand(): Handle demand events and emergency supply requests
- SKU.place_order(): Order replenishment when inventory gaps occur
- SKU.receive_delivery(): Process incoming deliveries
- Location.get_*(): Reporting and summary methods for contained SKUs
- SimulationManager.run_week(): Execute one week of simulation

Key Features:
- Discrete Event Processing: Events scheduled and processed in chronological order
- Bidirectional SKU Connections: PAR SKUs can request emergency supply from perpetual SKUs
- Negative Inventory Support: Perpetual SKUs can go negative to maintain service levels
- Hospital-Level Stockout Tracking: Records when entire system is under stress
- Event-Driven Architecture: Ready for SimPy integration

Design Patterns:
- Observer Pattern: For inventory change notifications
- Strategy Pattern: For replenishment policies (Order-Up-To-Level)
- Factory Pattern: For resource creation
- Manager Pattern: For system coordination
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
import math
import heapq

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
    
    # Location Get Methods for Reporting and Summaries
    
    def get_inventory_levels(self) -> Dict[str, float]:
        """Get current inventory levels of all SKUs in this location."""
        return {sku_id: sku.get_current_level() for sku_id, sku in self.skus.items()}
    
    def get_demand_summary(self) -> Dict[str, float]:
        """Get demand patterns across all SKUs in this location."""
        return {sku_id: sku.demand_rate for sku_id, sku in self.skus.items()}
    
    def get_stockout_summary(self) -> Dict[str, float]:
        """Get stockout statistics for all SKUs in this location."""
        return {sku_id: sku.get_stockout_amount() for sku_id, sku in self.skus.items()}
    
    def get_replenishment_summary(self) -> Dict[str, int]:
        """Get replenishment activity for all SKUs in this location."""
        return {sku_id: len(sku._pending_shipments) for sku_id, sku in self.skus.items()}
    
    def get_total_inventory(self) -> float:
        """Get sum of all SKU inventory levels in this location."""
        return sum(sku.get_current_level() for sku in self.skus.values())
    
    def get_sku_count(self) -> int:
        """Get number of SKUs in this location."""
        return len(self.skus)
    
    def get_stockout_rate(self) -> float:
        """Get percentage of SKUs experiencing stockouts in this location."""
        if not self.skus:
            return 0.0
        stockout_count = sum(1 for sku in self.skus.values() if sku.get_stockout_amount() > 0)
        return (stockout_count / len(self.skus)) * 100.0
    
    def get_emergency_transfer_count(self) -> int:
        """Get total number of emergency transfers for all SKUs in this location."""
        return sum(sku._total_emergency_transfers for sku in self.skus.values())
    
    def get_average_lead_time(self) -> float:
        """Get average lead time across all SKUs in this location."""
        if not self.skus:
            return 0.0
        total_lead_time = sum(sku.lead_time_weeks for sku in self.skus.values())
        return total_lead_time / len(self.skus)
    
    def get_demand_variance(self) -> float:
        """Get variability in demand across SKUs in this location."""
        if not self.skus:
            return 0.0
        demand_rates = [sku.demand_rate for sku in self.skus.values()]
        if not demand_rates:
            return 0.0
        mean_demand = sum(demand_rates) / len(demand_rates)
        variance = sum((rate - mean_demand) ** 2 for rate in demand_rates) / len(demand_rates)
        return variance ** 0.5  # Standard deviation
    
    def get_sku_by_id(self, sku_id: str) -> Optional['SKU']:
        """Get a specific SKU by ID from this location."""
        return self.skus.get(sku_id)

class SKU(Resource):
    """SKU resource representing individual medical supplies."""
    
    def __init__(self, sku_id: str, location_id: str, target_level: float = 0, 
                 lead_time_days: float = 0, demand_rate: float = 0):
        super().__init__(sku_id, ResourceType.SKU)
        self.location_id = location_id
        self.target_level = target_level
        self.lead_time_days = lead_time_days  # Original lead time in days
        self.lead_time_weeks = lead_time_days / 7.0  # Converted to fractional weeks for precise timing
        self.demand_rate = demand_rate  # Weekly demand rate
        self.connected_par_skus: List['SKU'] = []  # For perpetual SKUs only
        self._connected_perpetual_sku: Optional['SKU'] = None  # For PAR SKUs only
        self._current_inventory_level = 0
        self._pending_shipments: List['DeliveryEvent'] = []  # Discrete event shipments
        self._stockout_amount = 0  # Current stockout amount
        self._total_stockouts = 0  # Cumulative stockouts
        self._total_emergency_transfers = 0  # Cumulative emergency transfers
        logger.debug(f"Created SKU {sku_id} in location {location_id} (lead time: {lead_time_days} days = {self.lead_time_weeks:.3f} weeks)")
    
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
        """Allocate emergency supply to connected PAR SKUs. Can go negative."""
        if not self.connected_par_skus:
            return 0
        
        available = self.get_current_level()
        
        if available >= demand:
            # Normal case - enough inventory
            allocated = demand
            self.set_inventory_level(available - allocated)
        else:
            # Emergency case - go negative but still send the item
            allocated = demand
            self.set_inventory_level(available - allocated)  # This will be negative
            # Record hospital-level stockout
            self._total_stockouts += (demand - available)
            logger.warning(f"Hospital-level stockout for {self.resource_id}: went negative by {demand - available} units")
        
        self._total_emergency_transfers += allocated
        logger.info(f"Allocated {allocated} units of {self.resource_id} for emergency supply")
        
        return allocated
    
    def add_pending_shipment(self, delivery_event: 'DeliveryEvent'):
        """Add a pending shipment to the SKU."""
        self._pending_shipments.append(delivery_event)
        logger.debug(f"Added pending shipment for {self.resource_id}: {delivery_event.quantity} units at time {delivery_event.time}")
    
    def get_pending_shipments(self, current_time: int) -> float:
        """Get total quantity of pending shipments arriving by current time."""
        total_pending = sum(shipment.quantity for shipment in self._pending_shipments 
                           if shipment.time <= current_time)
        return total_pending
    
    def process_delivery_event(self, delivery_event: 'DeliveryEvent'):
        """Process a delivery event and update inventory."""
        if delivery_event in self._pending_shipments:
            self._pending_shipments.remove(delivery_event)
            self.set_inventory_level(self.get_current_level() + delivery_event.quantity)
            logger.info(f"Processed delivery for {self.resource_id}: +{delivery_event.quantity} units")
    
    def process_demand_event(self, demand_event: 'DemandEvent'):
        """Process a discrete demand event."""
        available_inventory = self.get_current_level()
        demand_amount = demand_event.quantity
        
        if available_inventory >= demand_amount:
            # Normal fulfillment
            self.set_inventory_level(available_inventory - demand_amount)
            logger.debug(f"Fulfilled demand for {self.resource_id}: {demand_amount} units")
        else:
            # Stockout occurs - need to find connected perpetual SKU for emergency supply
            self.set_inventory_level(0)
            self._stockout_amount = demand_amount - available_inventory
            self._total_stockouts += self._stockout_amount
            logger.warning(f"Stockout for {self.resource_id}: {self._stockout_amount} units short")
            
            # Find connected perpetual SKU for emergency supply
            perpetual_sku = self._find_connected_perpetual_sku()
            if perpetual_sku:
                # Perpetual SKU will handle emergency supply (may go negative)
                perpetual_sku.process_demand_event(demand_event)
                # Receive emergency supply from perpetual
                emergency_received = perpetual_sku.allocate_emergency_supply(self._stockout_amount)
                if emergency_received > 0:
                    self.set_inventory_level(emergency_received)
                    self._stockout_amount = max(0, self._stockout_amount - emergency_received)
                    logger.info(f"Received emergency supply for {self.resource_id}: {emergency_received} units")
    
    def _find_connected_perpetual_sku(self) -> Optional['SKU']:
        """Find the connected perpetual SKU for this PAR SKU."""
        return self._connected_perpetual_sku
    
    def set_connected_perpetual_sku(self, perpetual_sku: 'SKU'):
        """Set the connected perpetual SKU for this PAR SKU."""
        self._connected_perpetual_sku = perpetual_sku
        logger.debug(f"Connected PAR SKU {self.resource_id} to perpetual SKU {perpetual_sku.resource_id}")
    
    def trigger_emergency_replenishment(self, stockout_amount: float):
        """Trigger emergency replenishment from perpetual location."""
        if self.location_id != "PERPETUAL" and self.connected_par_skus:
            # This is a PAR SKU - request emergency supply from perpetual
            perpetual_sku = self.connected_par_skus[0]  # Get perpetual SKU
            if perpetual_sku and perpetual_sku.can_supply_emergency():
                allocated = perpetual_sku.allocate_emergency_supply(stockout_amount)
                if allocated > 0:
                    self.set_inventory_level(self.get_current_level() + allocated)
                    self._stockout_amount = max(0, self._stockout_amount - allocated)
                    logger.info(f"Emergency replenishment for {self.resource_id}: {allocated} units")
    
    def get_stockout_amount(self) -> float:
        """Get current stockout amount."""
        return self._stockout_amount
    
    def record_stockout(self, amount: float):
        """Record a stockout event."""
        self._stockout_amount = amount
        self._total_stockouts += amount
    
    def add_emergency_supply(self, amount: float):
        """Add emergency supply from perpetual location."""
        self.set_inventory_level(self.get_current_level() + amount)
        self._stockout_amount = max(0, self._stockout_amount - amount)
        logger.info(f"Added emergency supply to {self.resource_id}: {amount} units")
    
    def calculate_inventory_gap(self, current_time: int) -> float:
        """Calculate inventory gap for discrete event simulation."""
        target_inventory = self.target_level
        current_inventory = self.get_current_level()
        pending_shipments = self.get_pending_shipments(current_time)
        
        inventory_gap = max(0, target_inventory - (current_inventory + pending_shipments))
        return inventory_gap

class ResourceFactory:
    """Factory for creating resources."""
    
    @staticmethod
    def create_location(location_id: str, location_type: str, max_capacity: float = float('inf')) -> Location:
        """Create a new location resource."""
        return Location(location_id, location_type, max_capacity)
    
    @staticmethod
    def create_sku(sku_id: str, location_id: str, **kwargs) -> SKU:
        """Create a new SKU resource.
        
        Args:
            sku_id: Unique SKU identifier
            location_id: Location where SKU is stored
            **kwargs: Additional parameters including:
                - target_level: Target inventory level
                - lead_time_days: Lead time in days (converted to weeks automatically)
                - demand_rate: Weekly demand rate
        """
        return SKU(sku_id, location_id, **kwargs)

class SimulationManager:
    """Simplified manager class for coordinating the simulation system."""
    
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
    
    def setup_emergency_connections(self):
        """Set up emergency connections between perpetual and PAR SKUs."""
        for sku_id, sku_list in self.sku_registry.items():
            perpetual_sku = self.get_perpetual_sku(sku_id)
            par_skus = self.get_par_skus(sku_id)
            
            if perpetual_sku and par_skus:
                for par_sku in par_skus:
                    # Set up bidirectional connections
                    perpetual_sku.add_emergency_connection(par_sku)  # Perpetual -> PAR
                    par_sku.set_connected_perpetual_sku(perpetual_sku)  # PAR -> Perpetual
        
        logger.info("Emergency connections established")
    
    def get_perpetual_sku(self, sku_id: str) -> Optional[SKU]:
        """Get a SKU from the perpetual location."""
        perpetual_location = self.locations.get("PERPETUAL")
        return perpetual_location.skus.get(sku_id) if perpetual_location else None
    
    def get_par_skus(self, sku_id: str) -> List[SKU]:
        """Get all PAR SKUs of a given type."""
        return [sku for sku in self.sku_registry.get(sku_id, []) 
                if sku.location_id != "PERPETUAL"]
    
    def run_week(self, week_number: int):
        """Execute one week of simulation - main process."""
        logger.info(f"Running simulation week {week_number}")
        
        # This is where SimPy will call this method
        # The actual event processing will be handled by SimPy
        # This method just coordinates the week's activities
        
        # Update system status
        self._update_system_status()
        
        logger.info(f"Completed simulation week {week_number}")
    
    def _update_system_status(self):
        """Update system status and statistics."""
        # This can be called by SimPy or other processes
        pass
    
    def on_inventory_change(self, resource: Resource, old_level: float, new_level: float):
        """Handle inventory changes at the system level."""
        logger.debug(f"System-level inventory change: {resource.resource_id} {old_level} -> {new_level}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the entire system."""
        status = {
            "total_locations": len(self.locations),
            "total_skus": sum(len(sku_list) for sku_list in self.sku_registry.values()),
            "simulation_time_step": "weekly",
            "lead_time_conversion": "days_to_weeks = days / 7 (fractional for precise timing)",
            "locations": {}
        }
        
        for location_id, location in self.locations.items():
            status["locations"][location_id] = {
                "type": location.location_type,
                "total_inventory": location.get_current_level(),
                "sku_count": len(location.skus)
            }
        
        return status

# Event Classes for Discrete Event Simulation

@dataclass
class DemandEvent:
    """Discrete demand event for a SKU."""
    sku_id: str
    quantity: float
    time: int
    location_id: str
    
    def __lt__(self, other):
        """For priority queue ordering."""
        return self.time < other.time

@dataclass
class DeliveryEvent:
    """Discrete delivery event for replenishment."""
    sku_id: str
    quantity: float
    time: int
    source: str  # "external_supplier" or "emergency_transfer"
    
    def __lt__(self, other):
        """For priority queue ordering."""
        return self.time < other.time

@dataclass
class ReplenishmentEvent:
    """Discrete replenishment order event."""
    sku_id: str
    order_quantity: float
    time: int
    location_id: str
    
    def __lt__(self, other):
        """For priority queue ordering."""
        return self.time < other.time

class DiscreteEventSimulation:
    """Discrete event simulation manager for CedarSim."""
    
    def __init__(self):
        self.current_time = 0
        self.event_queue = []  # Priority queue for events
        self.skus: Dict[str, SKU] = {}
        self.locations: Dict[str, Location] = {}
        self.simulation_stats = {
            'total_demand': 0,
            'total_stockouts': 0,
            'total_emergency_transfers': 0,
            'total_replenishment_orders': 0
        }
        logger.info("Initialized DiscreteEventSimulation")
    
    def add_sku(self, sku: SKU):
        """Add a SKU to the simulation."""
        self.skus[sku.resource_id] = sku
        logger.debug(f"Added SKU to simulation: {sku.resource_id}")
    
    def add_location(self, location: Location):
        """Add a location to the simulation."""
        self.locations[location.resource_id] = location
        logger.debug(f"Added location to simulation: {location.resource_id}")
    
    def schedule_event(self, event):
        """Schedule an event for future processing."""
        heapq.heappush(self.event_queue, event)
        logger.debug(f"Scheduled event: {type(event).__name__} for {event.sku_id} at time {event.time}")
    
    def run_simulation(self, end_time: int):
        """
        Run discrete event simulation from time 0 to end_time.
        
        Args:
            end_time: Final simulation time (week number)
        """
        logger.info(f"Starting simulation from time 0 to {end_time}")
        
        while self.current_time < end_time and self.event_queue:
            # Get next event
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            
            # Process the event
            if isinstance(event, DemandEvent):
                self.process_demand_event(event)
            elif isinstance(event, DeliveryEvent):
                self.process_delivery_event(event)
            elif isinstance(event, ReplenishmentEvent):
                self.process_replenishment_event(event)
            
            logger.debug(f"Processed {type(event).__name__} at time {self.current_time}")
        
        logger.info(f"Simulation completed at time {self.current_time}")
        self.print_simulation_summary()
    
    def process_demand_event(self, event: DemandEvent):
        """Process a demand event for a specific SKU."""
        if event.sku_id in self.skus:
            sku = self.skus[event.sku_id]
            sku.process_demand_event(event)
            self.simulation_stats['total_demand'] += event.quantity
            
            # Check if we need to place a replenishment order
            inventory_gap = sku.calculate_inventory_gap(self.current_time)
            if inventory_gap > 0:
                self.schedule_replenishment_order(sku, inventory_gap)
    
    def process_delivery_event(self, event: DeliveryEvent):
        """Process a delivery event for a specific SKU."""
        if event.sku_id in self.skus:
            sku = self.skus[event.sku_id]
            sku.process_delivery_event(event)
    
    def process_replenishment_event(self, event: ReplenishmentEvent):
        """Process a replenishment order event."""
        if event.sku_id in self.skus:
            sku = self.skus[event.sku_id]
            self.simulation_stats['total_replenishment_orders'] += 1
            
            # Schedule delivery based on lead time
            delivery_time = self.current_time + sku.lead_time_weeks
            delivery_event = DeliveryEvent(
                sku_id=event.sku_id,
                quantity=event.order_quantity,
                time=delivery_time,
                source="external_supplier"
            )
            
            sku.add_pending_shipment(delivery_event)
            self.schedule_event(delivery_event)
            
            logger.info(f"Scheduled delivery for {event.sku_id}: {event.order_quantity} units at time {delivery_time}")
    
    def schedule_replenishment_order(self, sku: SKU, order_quantity: float):
        """Schedule a replenishment order for a SKU."""
        replenishment_event = ReplenishmentEvent(
            sku_id=sku.resource_id,
            order_quantity=order_quantity,
            time=self.current_time,
            location_id=sku.location_id
        )
        
        self.schedule_event(replenishment_event)
        logger.info(f"Scheduled replenishment order for {sku.resource_id}: {order_quantity} units")
    
    def generate_weekly_demand_events(self, sku_id: str, demand_rate: float, start_time: int, end_time: int):
        """Generate weekly demand events for a SKU."""
        for week in range(start_time, end_time):
            if demand_rate > 0:
                demand_event = DemandEvent(
                    sku_id=sku_id,
                    quantity=demand_rate,
                    time=week,
                    location_id=self.skus[sku_id].location_id
                )
                self.schedule_event(demand_event)
    
    def print_simulation_summary(self):
        """Print simulation statistics summary."""
        print("\n" + "="*50)
        print("SIMULATION SUMMARY")
        print("="*50)
        print(f"Total Demand Processed: {self.simulation_stats['total_demand']:.2f} units")
        print(f"Total Stockouts: {self.simulation_stats['total_stockouts']:.2f} units")
        print(f"Total Emergency Transfers: {self.simulation_stats['total_emergency_transfers']:.2f} units")
        print(f"Total Replenishment Orders: {self.simulation_stats['total_replenishment_orders']}")
        
        # Calculate service level
        if self.simulation_stats['total_demand'] > 0:
            service_level = (self.simulation_stats['total_demand'] - self.simulation_stats['total_stockouts']) / self.simulation_stats['total_demand']
            print(f"Service Level: {service_level:.2%}")
        
        print("="*50)

# Example usage and testing
if __name__ == "__main__":
    # Create discrete event simulation
    sim = DiscreteEventSimulation()
    
    # Create locations
    perpetual = ResourceFactory.create_location("PERPETUAL", "Perpetual", max_capacity=10000)
    ed_location = ResourceFactory.create_location("ED", "PAR", max_capacity=1000)
    
    sim.add_location(perpetual)
    sim.add_location(ed_location)
    
    # Create SKUs (lead times in days, automatically converted to discrete weeks)
    sku_001_perpetual = ResourceFactory.create_sku("SKU_001", "PERPETUAL", 
                                                   target_level=100, lead_time_days=2.0, demand_rate=0)
    sku_001_ed = ResourceFactory.create_sku("SKU_001", "ED", 
                                           target_level=50, lead_time_days=1.5, demand_rate=10.0)
    
    sim.add_sku(sku_001_perpetual)
    sim.add_sku(sku_001_ed)
    
    # Add SKUs to locations
    perpetual.add_sku(sku_001_perpetual)
    ed_location.add_sku(sku_001_ed)
    
    # Set up emergency connections
    sku_001_perpetual.add_emergency_connection(sku_001_ed)
    
    # Initialize inventory levels
    sku_001_ed.set_inventory_level(25)
    sku_001_perpetual.set_inventory_level(75)
    
    # Generate demand events for 10 weeks
    sim.generate_weekly_demand_events("SKU_001", 10.0, 0, 10)
    
    # Run simulation
    print("Starting Discrete Event Simulation...")
    sim.run_simulation(10)
    
    # Print final system status
    print("\nFinal System Status:")
    print(f"ED SKU Inventory: {sku_001_ed.get_current_level()}")
    print(f"Perpetual SKU Inventory: {sku_001_perpetual.get_current_level()}")
    print(f"ED SKU Stockouts: {sku_001_ed.get_stockout_amount()}")
    print(f"ED SKU Total Stockouts: {sku_001_ed._total_stockouts}")
    print(f"Perpetual SKU Emergency Transfers: {sku_001_perpetual._total_emergency_transfers}")
