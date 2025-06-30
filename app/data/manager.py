"""
Data management module for I/O operations.
"""
import json
import os
from typing import List, Dict, Any
import pandas as pd
from app.config import (
    STOCK_SYMBOLS_PATH, 
    METRIC_BOUNDARIES_PATH, 
    COMPANY_INDEXES_OUTPUT_PATH
)


def load_tickers_from_json(file_path: str = None) -> List[str]:
    """
    Load stock tickers from a JSON file.
    
    Args:
        file_path: Path to the JSON file. If None, uses the default from config.
        
    Returns:
        List of stock symbols
    """
    if file_path is None:
        # Try the configured path first, fallback to existing file
        if os.path.exists(STOCK_SYMBOLS_PATH):
            file_path = STOCK_SYMBOLS_PATH
        elif os.path.exists("data/stock_symbols.json"):
            file_path = "data/stock_symbols.json"
        else:
            raise FileNotFoundError(f"No stock symbols file found. Expected: {STOCK_SYMBOLS_PATH}")
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            
        # Handle different JSON structures
        if isinstance(data, list):
            # If it's a list of objects with 'symbol' key
            if data and isinstance(data[0], dict) and 'symbol' in data[0]:
                return [stock["symbol"] for stock in data]
            # If it's a simple list of strings
            elif data and isinstance(data[0], str):
                return data
        elif isinstance(data, dict):
            # If it's a dictionary, try to extract symbols
            if 'symbols' in data:
                return data['symbols']
            elif 'tickers' in data:
                return data['tickers']
        
        raise ValueError(f"Unsupported JSON structure in {file_path}")
        
    except Exception as e:
        raise Exception(f"Error loading tickers from {file_path}: {e}")


def save_dataframe_to_csv(df: pd.DataFrame, file_path: str = None, index: bool = True) -> str:
    """
    Save a DataFrame to a CSV file.
    
    Args:
        df: DataFrame to save
        file_path: Output file path. If None, uses the default from config.
        index: Whether to include the index in the CSV file
        
    Returns:
        Path to the saved file
    """
    if file_path is None:
        file_path = COMPANY_INDEXES_OUTPUT_PATH
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        df.to_csv(file_path, index=index)
        print(f"DataFrame saved to {file_path}")
        return file_path
    except Exception as e:
        raise Exception(f"Error saving DataFrame to {file_path}: {e}")


def load_metric_boundaries(file_path: str = None) -> Dict[str, Dict[str, float]]:
    """
    Load metric boundaries from a JSON file.
    
    Args:
        file_path: Path to the boundaries JSON file. If None, uses the default from config.
        
    Returns:
        Dictionary containing metric boundaries
    """
    if file_path is None:
        file_path = METRIC_BOUNDARIES_PATH
    
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Error loading metric boundaries from {file_path}: {e}")


def save_metric_boundaries(boundaries: Dict[str, Dict[str, float]], file_path: str = None) -> str:
    """
    Save metric boundaries to a JSON file.
    
    Args:
        boundaries: Dictionary containing metric boundaries
        file_path: Output file path. If None, uses the default from config.
        
    Returns:
        Path to the saved file
    """
    if file_path is None:
        file_path = METRIC_BOUNDARIES_PATH
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, "w") as f:
            json.dump(boundaries, f, indent=2)
        print(f"Metric boundaries saved to {file_path}")
        return file_path
    except Exception as e:
        raise Exception(f"Error saving metric boundaries to {file_path}: {e}")


def create_backup_file(file_path: str, backup_suffix: str = "_backup") -> str:
    """
    Create a backup of an existing file.
    
    Args:
        file_path: Path to the file to backup
        backup_suffix: Suffix to add to the backup file name
        
    Returns:
        Path to the backup file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot backup non-existent file: {file_path}")
    
    base_name, ext = os.path.splitext(file_path)
    backup_path = f"{base_name}{backup_suffix}{ext}"
    
    try:
        # Copy the file content
        with open(file_path, 'r') as original:
            with open(backup_path, 'w') as backup:
                backup.write(original.read())
        
        print(f"Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        raise Exception(f"Error creating backup of {file_path}: {e}")


def ensure_data_directory(directory_path: str = "data") -> str:
    """
    Ensure that the data directory exists.
    
    Args:
        directory_path: Path to the data directory
        
    Returns:
        Absolute path to the data directory
    """
    abs_path = os.path.abspath(directory_path)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    if not os.path.exists(file_path):
        return {"exists": False}
    
    stat = os.stat(file_path)
    return {
        "exists": True,
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "modified_time": stat.st_mtime,
        "absolute_path": os.path.abspath(file_path)
    } 