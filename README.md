# Supply Chain Traceability Demo

A Flask-based demonstration of forward traceability in supply chains. This application answers the question: **"If a raw material lot is problematic, which downstream batches and customers are affected?"**

## Quick Start (Non-Technical Users)

### Using Docker (Recommended)

1. Make sure Docker is installed on your computer
2. Open a terminal/command prompt in this folder
3. Run: `docker-compose up`
4. Open your browser and go to: `http://localhost:5000`
5. Enter `RAW-LOT-001` in the input field and click "Trace Forward"

That's it! You'll see which batches and customers are affected by the raw material lot.

## Technical Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Local Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to: `http://localhost:5000`

### Docker Setup

1. Build and run with Docker Compose:
   ```bash
   docker-compose up
   ```

2. The application will be available at: `http://localhost:5000`

3. To stop the application, press `Ctrl+C` or run:
   ```bash
   docker-compose down
   ```

## Demo Scenarios

The application comes preloaded with multiple realistic supply chain scenarios:

### Main Scenario (as specified):
```
RAW-LOT-001
   └── BATCH-100 (transform event)
       ├── BATCH-101 (ship event → Customer A)
       └── BATCH-102 (ship event → Customer B)
```

### Additional Test Scenarios:

**RAW-LOT-002**: Blending operation with multiple customers
- Transforms to BATCH-200
- Blends with BATCH-100 to create BATCH-201
- Ships to Customer A and Customer C

**RAW-LOT-003**: Packaging operations
- Transforms to BATCH-300
- Packages into BATCH-301 and BATCH-302
- Ships to Customer B and Customer D

**RAW-LOT-004**: Complex branching with split operations
- Transforms to BATCH-400
- Splits into BATCH-401 and BATCH-402
- Further processes and ships to Customer A and Customer E

**RAW-LOT-005**: Quality control and rework
- Transforms to BATCH-500
- Reworked to BATCH-501
- Ships to Customer F

**RAW-LOT-006**: Direct shipment
- Ships directly to Customer G

**RAW-LOT-007**: Multi-level processing
- Multiple transformations and packaging
- Ships to Customer H

**To test:**
- Enter any lot ID (e.g., `RAW-LOT-001`, `RAW-LOT-004`, `RAW-LOT-007`) in the input field
- Click "Trace Forward"
- View all affected downstream batches and customers

## API Documentation

### Forward Trace Endpoint

**GET** `/trace/forward/<lot_id>`

Performs forward traceability from a given lot ID.

**Parameters:**
- `lot_id` (path parameter): The lot ID to trace from

**Response (Success - 200):**
```json
{
  "source_lot": "RAW-LOT-001",
  "affected": [
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
    {
      "lot": "BATCH-102",
      "event": "ship",
      "customer": "Customer B",
      "depth": 2
    }
  ]
}
```

**Response (Lot Not Found - 404):**
```json
{
  "error": "Lot 'INVALID-LOT' not found",
  "source_lot": "INVALID-LOT",
  "affected": []
}
```

**Response (Invalid Input - 400):**
```json
{
  "error": "Invalid lot_id"
}
```

**Example API Call:**
```bash
curl http://localhost:5000/trace/forward/RAW-LOT-001
```

## Integration Guide

This demo is designed to be easily integrated into existing Flask applications.

### Option 1: Import as Module

```python
from data import initialize_scenario
from trace import get_forward_trace_result
from models import DataStore

# Initialize your data store
data_store = initialize_scenario()

# Use in your routes
@app.route('/your-trace-endpoint/<lot_id>')
def your_trace(lot_id):
    result = get_forward_trace_result(lot_id, data_store)
    return jsonify(result)
```

### Option 2: Convert to Flask Blueprint

1. Create a blueprint in `app.py`:
```python
from flask import Blueprint

trace_bp = Blueprint('trace', __name__, url_prefix='/trace')

@trace_bp.route('/forward/<lot_id>')
def forward(lot_id):
    # Your trace logic here
    pass
```

2. Register in your main app:
```python
from app import trace_bp
app.register_blueprint(trace_bp)
```

### Key Integration Points

- **Data Store**: Replace `initialize_scenario()` with your own data loading logic
- **Models**: The `Event` and `DataStore` classes can be extended with additional fields
- **Trace Algorithm**: The `forward_trace()` function is independent and can be used with any data store structure

## Project Structure

```
supply_trace/
├── app.py                 # Main Flask application
├── models.py              # Data models (Event, DataStore)
├── trace.py               # Forward trace algorithm
├── data.py                # Preloaded scenario data
├── templates/
│   └── index.html         # Web UI
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker containerization
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## Features

- ✅ Forward traceability algorithm with loop prevention
- ✅ RESTful API endpoint
- ✅ Interactive web UI with JavaScript
- ✅ Docker support for easy deployment
- ✅ Integration-ready modular architecture
- ✅ Preloaded demo scenario

## Data Sources

The application loads all data from JSON files. The included `data.json` contains **demo/test data** with predefined scenarios designed to demonstrate the traceability feature. For production use, you would replace this with your real-world supply chain data.

### Data Types

**Demo/Test Data (Current)**
- `data.json` contains predefined scenarios for demonstration
- Designed to show specific traceability paths and results
- Perfect for demos, testing, and development

**Real-World Data (Production)**
- Replace `data.json` with your actual supply chain event data
- Same JSON format - just use your real lot IDs, events, and customers
- The system works identically with any valid JSON data

### Using JSON Data Source

1. **Default behavior**: The app automatically loads from `data.json` in the project root. The file must exist and be valid.

2. **Custom JSON file**: Set the `DATA_JSON_PATH` environment variable:
   ```bash
   # Windows PowerShell
   $env:DATA_JSON_PATH="path/to/your/data.json"
   python app.py
   
   # Linux/Mac
   export DATA_JSON_PATH="path/to/your/data.json"
   python app.py
   ```

3. **For production**: Replace `data.json` with your real supply chain data following the same format.

### JSON File Format

The JSON file should follow this structure:

```json
{
  "events": [
    {
      "event_id": "EVT-001",
      "event_type": "transform",
      "source_lot_id": "RAW-LOT-001",
      "target_lot_id": "BATCH-100",
      "customer": null
    },
    {
      "event_id": "EVT-002",
      "event_type": "ship",
      "source_lot_id": "BATCH-100",
      "target_lot_id": "BATCH-101",
      "customer": "Customer A"
    }
  ]
}
```

**Field descriptions:**
- `event_id` (required): Unique identifier for the event
- `event_type` (required): Type of event (e.g., "transform", "ship", "blend", "package", "split", "rework")
- `source_lot_id` (optional): Input lot ID. Can be null for root events
- `target_lot_id` (required): Output lot ID
- `customer` (optional): Customer name for shipment events. Use null for non-shipment events

**Example: Creating your own test data**

1. Copy `data.json` (or `data.example.json`) to `my_test_data.json`
2. Modify the events array with your test scenarios
3. Run: 
   ```bash
   # Windows PowerShell
   $env:DATA_JSON_PATH="my_test_data.json"
   python app.py
   
   # Linux/Mac
   export DATA_JSON_PATH="my_test_data.json"
   python app.py
   ```

**Note**: The `_comment` and `_format` fields in example files are ignored - they're just for documentation.

### Demo Data vs Real-World Data

**Important**: The included `data.json` contains **demo/test data** with predefined scenarios designed to demonstrate specific traceability results. This is intentional for demos and testing.

For production use:
- Replace `data.json` with your real supply chain event data
- Use the same JSON format
- The system works identically with real-world data

See `README_DATA.md` for more details on data types and migration.

## Technical Details

### Algorithm

The forward trace uses a depth-first search (DFS) approach:
1. Start from the source lot
2. Find all events that consume the lot
3. For each event, add the target lot to results
4. Recursively trace each target lot
5. Track visited lots to prevent infinite loops
6. Track depth for hierarchy display

### Data Model

- **Event**: Represents a transformation or shipment
  - `event_id`: Unique identifier
  - `event_type`: Type (e.g., "transform", "ship")
  - `source_lot_id`: Input lot (optional)
  - `target_lot_id`: Output lot
  - `customer`: Customer name (optional, for shipments)

- **DataStore**: In-memory data structure
  - `events_by_source`: Maps lot_id → events that consume it
  - `events_by_target`: Maps lot_id → events that produce it
  - `all_lots`: Set of all lot IDs for validation

## Limitations (Demo Only)

This is a demonstration application with the following limitations:
- In-memory data (no database persistence)
- No authentication
- No pagination
- Single preloaded scenario
- Basic error handling

For production use, these would need to be addressed.

## License

This is a demo project for evaluation purposes.
