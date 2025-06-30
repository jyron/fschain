"""
Schema loading utilities for financial metrics.
"""
import json
from typing import Any, Dict
from app.config import METRICS_SCHEMA_PATH


def load_metrics_schema(file_path: str = None) -> Dict[str, Any]:
    """
    Load the metric schema from a JSON file.
    
    Args:
        file_path: Path to the metrics schema JSON file. 
                  If None, uses the default from config.
    
    Returns:
        Dictionary containing the metrics schema
    """
    if file_path is None:
        file_path = METRICS_SCHEMA_PATH
        
    with open(file_path) as f:
        return json.load(f) 