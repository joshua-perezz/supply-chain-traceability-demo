"""
Flask application for traceability demo.

This is the main application file that provides:
- Web UI at GET /
- API endpoint at GET /trace/forward/<lot_id>
"""

import os
from flask import Flask, render_template, jsonify, request
from data import initialize_scenario
from trace import get_forward_trace_result
from models import DataStore

app = Flask(__name__)

# Initialize data store on startup
# Can specify JSON file path via environment variable DATA_JSON_PATH
# If not set, will load from data.json in project directory
json_path = os.getenv('DATA_JSON_PATH', None)
data_store: DataStore = initialize_scenario(json_path=json_path)


@app.route('/')
def index():
    """Render the main web UI."""
    return render_template('index.html')


@app.route('/trace/forward/<lot_id>')
def trace_forward(lot_id: str):
    """
    API endpoint for forward traceability.
    
    Args:
        lot_id: The lot ID to trace from
    
    Returns:
        JSON response with trace results or error
    """
    # Basic validation
    if not lot_id or not lot_id.strip():
        return jsonify({"error": "Invalid lot_id"}), 400
    
    lot_id = lot_id.strip()
    
    # Check if lot exists
    if not data_store.lot_exists(lot_id):
        return jsonify({
            "error": f"Lot '{lot_id}' not found",
            "source_lot": lot_id,
            "affected": []
        }), 404
    
    # Perform forward trace
    try:
        result = get_forward_trace_result(lot_id, data_store)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": f"Error performing trace: {str(e)}",
            "source_lot": lot_id,
            "affected": []
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
