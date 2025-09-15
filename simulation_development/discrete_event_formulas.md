# CedarSim Discrete Event Simulation Formulas

## Overview
This document adapts the continuous time formulas from the original model to discrete event simulation format. Instead of using `DT` (delta time) variables, we'll use discrete time steps and event-driven updates.

## Key Differences: Continuous vs Discrete Event

| Aspect | Continuous Time | Discrete Event |
|--------|----------------|----------------|
| **Time Steps** | `DT` (infinitesimal) | Discrete events (weekly) |
| **Updates** | Continuous derivatives | Event-triggered updates |
| **Demand** | `depleting*DT` | Discrete demand events |
| **Lead Time** | Fractional weeks | Integer time steps |
| **Inventory** | Continuous levels | Discrete unit counts |

## 1. Discrete Event Inventory Gap Calculation

### Original (Continuous):
```
Inventory Gap = MAX(0, ((depleting*DT + target_inventory) - (SKUs_in_Shipment + PAR)))
```

### Discrete Event Version:
```python
def calculate_inventory_gap(sku: SKU, current_time: int) -> float:
    """
    Calculate how much inventory to order for a SKU at current time.
    
    Args:
        sku: SKU object with current inventory and target level
        current_time: Current simulation time (week number)
    
    Returns:
        Order quantity needed
    """
    # What we want: target level
    target_inventory = sku.target_level
    
    # What we have: current inventory + pending shipments
    current_inventory = sku.get_current_level()
    pending_shipments = sku.get_pending_shipments(current_time)
    
    # Gap calculation
    inventory_gap = max(0, target_inventory - (current_inventory + pending_shipments))
    
    return inventory_gap
```

## 2. Discrete Event PAR Stockout Calculation

### Original (Continuous):
```
PAR Stockout = (demand_projection - depleting*DT/day)
```

### Discrete Event Version:
```python
def calculate_par_stockout(sku: SKU, demand_event: DemandEvent) -> float:
    """
    Calculate stockout amount when demand exceeds available inventory.
    
    Args:
        sku: PAR SKU object
        demand_event: Discrete demand event for this week
    
    Returns:
        Stockout amount (0 if no stockout)
    """
    available_inventory = sku.get_current_level()
    demand_amount = demand_event.quantity
    
    # Stockout occurs when demand exceeds available inventory
    stockout_amount = max(0, demand_amount - available_inventory)
    
    return stockout_amount

def process_demand_event(sku: SKU, demand_event: DemandEvent):
    """
    Process a discrete demand event for a SKU.
    
    Args:
        sku: SKU object to process demand for
        demand_event: Discrete demand event
    """
    available_inventory = sku.get_current_level()
    demand_amount = demand_event.quantity
    
    if available_inventory >= demand_amount:
        # Normal fulfillment
        sku.set_inventory_level(available_inventory - demand_amount)
        sku.record_fulfilled_demand(demand_amount)
    else:
        # Stockout occurs
        sku.set_inventory_level(0)  # Inventory goes to zero
        stockout_amount = demand_amount - available_inventory
        sku.record_stockout(stockout_amount)
        
        # Trigger emergency replenishment
        sku.trigger_emergency_replenishment(stockout_amount)
```

## 3. Discrete Event Lead Time Processing

### Original (Continuous):
```
Lead Time (weeks) = Lead Time (days) / 7
```

### Discrete Event Version:
```python
def schedule_replenishment_order(sku: SKU, order_quantity: float, current_time: int):
    """
    Schedule a replenishment order with discrete lead time.
    
    Args:
        sku: SKU to order for
        order_quantity: Amount to order
        current_time: Current simulation time (week)
    """
    # Convert lead time from days to discrete weeks
    lead_time_weeks = math.ceil(sku.lead_time_days / 7.0)
    
    # Schedule delivery event
    delivery_time = current_time + lead_time_weeks
    delivery_event = DeliveryEvent(
        sku_id=sku.resource_id,
        quantity=order_quantity,
        delivery_time=delivery_time,
        source="external_supplier"
    )
    
    # Add to pending shipments
    sku.add_pending_shipment(delivery_event)
    
    # Schedule the delivery event
    simulation.schedule_event(delivery_event)
```

## 4. Discrete Event Emergency Replenishment

### Original (Continuous):
```
Perpetual.supplying_PAR = SUM(PAR.PAR_stockouts[itemType,*]) * day/DT
```

### Discrete Event Version:
```python
def process_emergency_replenishment(perpetual_sku: SKU, par_skus: List[SKU], current_time: int):
    """
    Process emergency replenishment from perpetual to PAR locations.
    
    Args:
        perpetual_sku: SKU in perpetual location
        par_skus: List of PAR SKUs of same type
        current_time: Current simulation time
    """
    # Calculate total stockout demand across all PARs
    total_stockout_demand = sum(sku.get_stockout_amount() for sku in par_skus)
    
    if total_stockout_demand > 0 and perpetual_sku.get_current_level() > 0:
        # Allocate emergency supply
        available_supply = perpetual_sku.get_current_level()
        allocated_supply = min(total_stockout_demand, available_supply)
        
        # Distribute among PARs based on priority
        remaining_allocation = allocated_supply
        for par_sku in par_skus:
            if remaining_allocation <= 0:
                break
                
            par_stockout = par_sku.get_stockout_amount()
            if par_stockout > 0:
                # Allocate to this PAR
                allocation_amount = min(par_stockout, remaining_allocation)
                par_sku.add_emergency_supply(allocation_amount)
                remaining_allocation -= allocation_amount
                
                # Record emergency transfer
                record_emergency_transfer(
                    from_sku=perpetual_sku.resource_id,
                    to_sku=par_sku.resource_id,
                    quantity=allocation_amount,
                    time=current_time
                )
        
        # Update perpetual inventory
        perpetual_sku.set_inventory_level(perpetual_sku.get_current_level() - allocated_supply)
```

## 5. Discrete Event Allocation Function

### Original (Continuous):
```
Supplying from Perpetual = ALLOCATE(
    Perpetual.supplying_PAR[itemType]*DT/day,
    PARInventory,
    PAR_stockouts[itemType,*],
    PAR_priority[itemType,*],
    0
)
```

### Discrete Event Version:
```python
def allocate_emergency_supply(perpetual_sku: SKU, par_skus: List[SKU], 
                            allocation_quantity: float) -> Dict[str, float]:
    """
    Allocate emergency supply from perpetual to PAR locations.
    
    Args:
        perpetual_sku: Source SKU in perpetual location
        par_skus: List of destination PAR SKUs
        allocation_quantity: Total quantity to allocate
    
    Returns:
        Dictionary of SKU ID -> allocated quantity
    """
    # Sort PARs by priority (all have priority = 1, so by index)
    sorted_par_skus = sorted(par_skus, key=lambda x: x.resource_id)
    
    allocations = {}
    remaining_quantity = allocation_quantity
    
    for par_sku in sorted_par_skus:
        if remaining_quantity <= 0:
            break
            
        # Calculate how much this PAR needs
        par_stockout = par_sku.get_stockout_amount()
        if par_stockout > 0:
            # Allocate based on need and availability
            allocation = min(par_stockout, remaining_quantity)
            allocations[par_sku.resource_id] = allocation
            remaining_quantity -= allocation
    
    return allocations
```

## 6. Discrete Event Simulation Loop

```python
class DiscreteEventSimulation:
    def __init__(self):
        self.current_time = 0
        self.event_queue = []
        self.skus = {}
        self.locations = {}
    
    def run_simulation(self, end_time: int):
        """
        Run discrete event simulation from time 0 to end_time.
        
        Args:
            end_time: Final simulation time (week number)
        """
        while self.current_time < end_time:
            # Process all events at current time
            self.process_events_at_current_time()
            
            # Advance to next event time
            if self.event_queue:
                self.current_time = min(event.time for event in self.event_queue)
            else:
                self.current_time += 1  # Advance one week if no events
    
    def process_events_at_current_time(self):
        """Process all events scheduled for current time."""
        current_events = [e for e in self.event_queue if e.time == self.current_time]
        
        for event in current_events:
            if isinstance(event, DemandEvent):
                self.process_demand_event(event)
            elif isinstance(event, DeliveryEvent):
                self.process_delivery_event(event)
            elif isinstance(event, ReplenishmentEvent):
                self.process_replenishment_event(event)
            
            # Remove processed event
            self.event_queue.remove(event)
    
    def process_demand_event(self, event: DemandEvent):
        """Process a demand event for a specific SKU."""
        sku = self.skus[event.sku_id]
        
        # Check if SKU has enough inventory
        if sku.get_current_level() >= event.quantity:
            # Normal fulfillment
            sku.set_inventory_level(sku.get_current_level() - event.quantity)
        else:
            # Stockout - trigger emergency replenishment
            stockout_amount = event.quantity - sku.get_current_level()
            sku.set_inventory_level(0)
            sku.record_stockout(stockout_amount)
            
            # Schedule emergency replenishment
            self.schedule_emergency_replenishment(sku, stockout_amount)
```

## 7. Event Classes

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class DemandEvent:
    """Discrete demand event for a SKU."""
    sku_id: str
    quantity: float
    time: int
    location_id: str

@dataclass
class DeliveryEvent:
    """Discrete delivery event for replenishment."""
    sku_id: str
    quantity: float
    time: int
    source: str  # "external_supplier" or "emergency_transfer"

@dataclass
class ReplenishmentEvent:
    """Discrete replenishment order event."""
    sku_id: str
    order_quantity: float
    time: int
    location_id: str
```

## Key Benefits of Discrete Event Approach

1. **Realistic Modeling**: Events happen at specific times, not continuously
2. **Efficient Processing**: Only process events when they occur
3. **Clear Logic**: Easy to understand and debug
4. **Flexible Scheduling**: Can handle complex timing relationships
5. **Event Tracking**: Easy to record and analyze specific events

## Implementation Notes

- **Time Units**: All times in fractional weeks for precise timing
- **Lead Times**: Converted to fractional weeks using `days/7` (SimPy handles intra-week events)
- **Inventory**: Discrete unit counts (no fractional units)
- **Events**: Scheduled and processed in chronological order by SimPy
- **State Updates**: Only when events occur, not continuously

This discrete event approach will be much more suitable for SimPy integration and will provide more realistic simulation behavior for the hospital inventory system.
