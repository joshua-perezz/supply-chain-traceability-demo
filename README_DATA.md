# Data Source Guide

## Understanding Data Types

### Demo/Test Data vs Real-World Data

**Current `data.json` - Demo/Test Data:**
- Contains **predefined scenarios** designed to demonstrate specific traceability paths
- Example: RAW-LOT-001 is intentionally structured to show a specific result (BATCH-100 → BATCH-101/102)
- Purpose: Testing, demos, development, and showcasing the feature
- Not production data - it's designed to get predictable results for demonstrations

**Real-World Production Data:**
- Would contain actual supply chain events from your production system
- Real lot IDs, actual customer names, genuine event timestamps
- Purpose: Actual traceability queries for real business operations
- Format: Same JSON structure, but with real data

## When to Use Each

### Use Demo Data When:
- ✅ Demonstrating the feature to clients/stakeholders
- ✅ Testing the application functionality
- ✅ Development and debugging
- ✅ Creating video demos
- ✅ Job application portfolios

### Use Real-World Data When:
- ✅ Production deployment
- ✅ Actual supply chain traceability queries
- ✅ Integration with existing systems
- ✅ Real customer-facing applications

## Data Format

Both demo and real-world data use the same JSON format:

```json
{
  "events": [
    {
      "event_id": "EVT-001",
      "event_type": "transform",
      "source_lot_id": "RAW-LOT-001",
      "target_lot_id": "BATCH-100",
      "customer": null
    }
  ]
}
```

## Migrating to Real-World Data

1. **Export your production data** in the required JSON format
2. **Replace `data.json`** with your real data file
3. **Or use environment variable** to point to your production data:
   ```bash
   $env:DATA_JSON_PATH="production_data.json"
   python app.py
   ```

The application works identically with both - the only difference is the source of the data.
