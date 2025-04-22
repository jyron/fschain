import json
import os
from datetime import datetime
from pprint import pprint
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


FMP_API_KEY = os.getenv("FMP_API_KEY")

def fetchFMP_RATIOS_TTM(symbol: str) -> Dict[str, Any]:
    """
    Fetch TTM ratios from Financial Modeling Prep API.
    """
    url = f"https://financialmodelingprep.com/stable/ratios-ttm?symbol={symbol}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else {}


def fetchFMP_KEY_Metrics_TTM(symbol: str) -> Dict[str, Any]:
    """
    Fetch TTM key metrics from Financial Modeling Prep API.
    """
    url = f"https://financialmodelingprep.com/stable/key-metrics-ttm?symbol={symbol}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else {}


def build_ftoken_object(data: Dict[str, Any], metrics_schema) -> Dict[str, Any]:
    """
    Transform raw financial data into structured FToken oracle object.
    """ 
    result = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "symbol": data.get("symbol", ""),
        "FTokenMetricsTTM": {}
    }
    for category, metrics in metrics_schema.items():
        result["FTokenMetricsTTM"][category] = {}
        for metric in metrics:
            result["FTokenMetricsTTM"][category][metric] = data.get(metric, None)
    
    return result


def fetch_and_build_ftoken(symbol: str, metrics_schema) -> Dict[str, Any]:
    """
    Fetch financial data and build FToken object.
    """
    TTM_ratios = fetchFMP_RATIOS_TTM(symbol)
    TTM_key_metrics = fetchFMP_KEY_Metrics_TTM(symbol)

    combined_TTM = {**TTM_ratios, **TTM_key_metrics}
    core_ftoken_data = build_ftoken_object(combined_TTM, metrics_schema)
    
    return core_ftoken_data


def load_metrics_schema(file_path: str) -> Dict[str, Any]:
    """
    Load the metric schema from a JSON file.
    """
    with open(file_path) as f:
        return json.load(f)


def print_metrics(data: Dict[str, Any]):
    '''
    Print the metrics in a structured format.
    '''
    print(f"Symbol: {data['symbol']}")
    print(f"Date: {data['date']}")
    print("=" * 50)

    for category, metrics in data["FTokenMetricsTTM"].items():
        print(f"\n📘 {category}")
        print("-" * 50)
        for metric, value in metrics.items():
            print(f"{metric:<40} : {value}")
# example usage (uncomment to run):
# metrics_schema = load_metrics_schema("specifications/ftoken-metrics.json")
# symbol = "TSLA"
# ftoken_data = fetch_and_build_ftoken(symbol, metrics_schema)
# print(ftoken_data)