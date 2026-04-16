"""
The Huddle - Sports Package
Unified registry for all sport handlers.
"""

import json
from typing import Dict, Any


def format_vapi_response(data: Any) -> str:
    """Format any data as a JSON string for Vapi's LLM to process."""
    if not data:
        return "No data found for this query."
    if isinstance(data, dict) and "error" in data:
        return f"Error retrieving data: {data['error']}"
    return json.dumps(data, indent=2)
