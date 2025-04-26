"""
Data models for traceability system.

This module defines the data structures for lots and events,
and provides an in-memory data store for the demo.
"""

from typing import Dict, List, Optional


class Event:
    """Represents an event that consumes a source lot and produces a target lot."""
    
    def __init__(
        self,
        event_id: str,
        event_type: str,
        source_lot_id: Optional[str],
        target_lot_id: str,
        customer: Optional[str] = None
    ):
        self.event_id = event_id
        self.event_type = event_type
        self.source_lot_id = source_lot_id
        self.target_lot_id = target_lot_id
        self.customer = customer
    
    def to_dict(self) -> dict:
        """Convert event to dictionary for JSON serialization."""
        result = {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "target_lot_id": self.target_lot_id
        }
        if self.source_lot_id:
            result["source_lot_id"] = self.source_lot_id
        if self.customer:
            result["customer"] = self.customer
        return result


class DataStore:
    """In-memory data store for lots and events."""
    
    def __init__(self):
        # Maps source_lot_id -> list of events that consume it
        self.events_by_source: Dict[str, List[Event]] = {}
        # Maps target_lot_id -> list of events that produce it
        self.events_by_target: Dict[str, List[Event]] = {}
        # Set of all lot IDs (for validation)
        self.all_lots: set = set()
    
    def add_event(self, event: Event) -> None:
        """Add an event to the data store."""
        # Add to source mapping
        if event.source_lot_id:
            if event.source_lot_id not in self.events_by_source:
                self.events_by_source[event.source_lot_id] = []
            self.events_by_source[event.source_lot_id].append(event)
            self.all_lots.add(event.source_lot_id)
        
        # Add to target mapping
        if event.target_lot_id not in self.events_by_target:
            self.events_by_target[event.target_lot_id] = []
        self.events_by_target[event.target_lot_id].append(event)
        self.all_lots.add(event.target_lot_id)
    
    def get_downstream_events(self, lot_id: str) -> List[Event]:
        """Get all events that consume the given lot (forward trace)."""
        return self.events_by_source.get(lot_id, [])
    
    def lot_exists(self, lot_id: str) -> bool:
        """Check if a lot exists in the data store."""
        return lot_id in self.all_lots
