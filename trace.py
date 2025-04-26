"""
Forward traceability algorithm.

This module implements the forward trace functionality:
given a lot_id, find all downstream lots and customers affected.
"""

from typing import List, Dict, Set, Optional
from models import DataStore, Event


def forward_trace(
    lot_id: str,
    data_store: DataStore,
    visited: Optional[Set[str]] = None,
    depth: int = 0
) -> List[Dict]:
    """
    Perform forward traceability from a given lot.
    
    Traverses the event graph forward to find all downstream lots
    and customers that are affected by the source lot.
    
    Args:
        lot_id: The source lot ID to trace from
        data_store: The data store containing events
        visited: Set of already visited lot IDs (for loop prevention)
        depth: Current depth in the trace hierarchy
    
    Returns:
        List of dictionaries containing affected lot information:
        [
            {
                "lot": "BATCH-100",
                "event": "transform",
                "depth": 1
            },
            {
                "lot": "BATCH-101",
                "event": "ship",
                "customer": "Customer A",
                "depth": 2
            },
            ...
        ]
    """
    if visited is None:
        visited = set()
    
    # Prevent infinite loops
    if lot_id in visited:
        return []
    
    visited.add(lot_id)
    results = []
    
    # Get all events that consume this lot (forward direction)
    downstream_events = data_store.get_downstream_events(lot_id)
    
    for event in downstream_events:
        # Create result entry for this affected lot
        result_entry = {
            "lot": event.target_lot_id,
            "event": event.event_type,
            "depth": depth + 1
        }
        
        # Add customer if present
        if event.customer:
            result_entry["customer"] = event.customer
        
        results.append(result_entry)
        
        # Recursively trace the target lot
        downstream_results = forward_trace(
            event.target_lot_id,
            data_store,
            visited.copy(),  # Pass copy to allow different branches
            depth + 1
        )
        results.extend(downstream_results)
    
    return results


def get_forward_trace_result(lot_id: str, data_store: DataStore) -> Dict:
    """
    Get the complete forward trace result for a lot.
    
    Args:
        lot_id: The source lot ID
        data_store: The data store containing events
    
    Returns:
        Dictionary with source_lot and affected list:
        {
            "source_lot": "RAW-LOT-001",
            "affected": [...]
        }
    """
    if not data_store.lot_exists(lot_id):
        return {
            "source_lot": lot_id,
            "affected": []
        }
    
    affected = forward_trace(lot_id, data_store)
    
    return {
        "source_lot": lot_id,
        "affected": affected
    }
