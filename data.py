"""
Data loading module for the traceability demo.

Loads events from JSON file for flexible testing and configuration.
"""

import json
import os
from pathlib import Path
from typing import Optional
from models import DataStore, Event


def load_from_json(json_path: Optional[str] = None) -> Optional[DataStore]:
    """
    Load events from a JSON file.
    
    JSON format:
    {
      "events": [
        {
          "event_id": "EVT-001",
          "event_type": "transform",
          "source_lot_id": "RAW-LOT-001",
          "target_lot_id": "BATCH-100",
          "customer": null
        },
        ...
      ]
    }
    
    Args:
        json_path: Path to JSON file. If None, tries 'data.json' in current directory.
    
    Returns:
        DataStore if JSON file exists and is valid, None otherwise
    """
    if json_path is None:
        json_path = os.path.join(os.path.dirname(__file__), "data.json")
    
    json_path = Path(json_path)
    
    if not json_path.exists():
        return None
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        store = DataStore()
        
        if "events" not in data:
            raise ValueError("JSON must contain 'events' array")
        
        for event_data in data["events"]:
            event = Event(
                event_id=event_data.get("event_id", ""),
                event_type=event_data.get("event_type", ""),
                source_lot_id=event_data.get("source_lot_id"),
                target_lot_id=event_data.get("target_lot_id", ""),
                customer=event_data.get("customer")
            )
            store.add_event(event)
        
        return store
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Warning: Failed to load JSON data from {json_path}: {e}")
        return None


def initialize_scenario(json_path: Optional[str] = None) -> DataStore:
    """
    Initialize the data store by loading events from JSON file.
    
    Args:
        json_path: Optional path to JSON file. If None, tries 'data.json' in current directory.
    
    Returns:
        DataStore: Initialized data store with events from JSON file
    
    Raises:
        FileNotFoundError: If JSON file is not found
        ValueError: If JSON file is invalid or missing required fields
    """
    store = load_from_json(json_path)
    
    if store is None:
        if json_path is None:
            json_path = os.path.join(os.path.dirname(__file__), "data.json")
        raise FileNotFoundError(
            f"Data file not found: {json_path}. "
            f"Please ensure data.json exists in the project directory."
        )
    
    return store
