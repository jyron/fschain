import pandas as pd
from typing import Dict, Tuple
import json
from pathlib import Path

def calculate_metric_boundaries(df: pd.DataFrame) -> Dict[str, Tuple[float, float]]:
    """
    Calculate the 10th and 90th percentiles for each metric across all companies.
    
    Args:
        df: DataFrame where rows are companies and columns are metrics
        
    Returns:
        Dictionary where keys are metric names and values are tuples of (10th_percentile, 90th_percentile)
    """
    metric_boundaries = {}
    

    for column in df.columns:
        if column in ['fiscalYear']:
            continue
            

        column_data = df[column].dropna()


        if len(column_data) > 0:
            tenth_percentile = column_data.quantile(0.10)
            ninetieth_percentile = column_data.quantile(0.90)
            metric_boundaries[column] = (tenth_percentile, ninetieth_percentile)
        else:
            metric_boundaries[column] = (0.0, 1.0)
            print(f"Warning: No valid data for metric {column}, using default bounds")
    
    return metric_boundaries



def save_metric_boundaries(boundaries: Dict[str, Tuple[float, float]], filepath: str = "data/metric_boundaries.json"):
    """
    Save metric boundaries to a JSON file.
    
    Args:
        boundaries: Dictionary of metric boundaries
        filepath: Path to save the JSON file
    """

    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    boundaries_json = {k: list(v) for k, v in boundaries.items()}
    
    with open(filepath, 'w') as f:
        json.dump(boundaries_json, f, indent=4)
    
    print(f"Metric boundaries saved to {filepath}")

def load_metric_boundaries(filepath: str = "data/metric_boundaries.json") -> Dict[str, Tuple[float, float]]:
    """
    Load metric boundaries from a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary where keys are metric names and values are tuples of (min_value, max_value)
    """
    try:
        with open(filepath, 'r') as f:
            boundaries_json = json.load(f)

        boundaries = {k: tuple(v) for k, v in boundaries_json.items()}
        print(f"Metric boundaries loaded from {filepath}")
        return boundaries
    except FileNotFoundError:
        print(f"Warning: File {filepath} not found. Returning empty dictionary.")
        return {}