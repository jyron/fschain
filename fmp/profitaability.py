import json
import os
from urllib.request import urlopen

import certifi
from dotenv import load_dotenv


def get_profitability_cluster(symbol, limit=5):
    """
    Retrieves the profitability cluster metrics for a given stock symbol.
    
    Parameters:
    symbol (str): Stock ticker symbol (e.g., 'AAPL')
    limit (int): Number of periods to retrieve
    
    Returns:
    list: List of dictionaries containing profitability metrics for recent periods
    """
    # Load environment variables and get API key
    load_dotenv()
    api_key = os.getenv("FMP_API_KEY")
    
    # Base URL for FMP Stable API
    url = f"https://financialmodelingprep.com/stable/ratios?symbol={symbol}&apikey={api_key}"
    
    try:
        # Get financial ratios data
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        ratios_data = json.loads(data)
        
        # Extract only the profitability metrics we need
        profitability_metrics = []
        
        for period in ratios_data[:limit]:
            metrics = {
                "date": period.get("date"),
                "fiscalYear": period.get("fiscalYear"),
                "period": period.get("period"),
                
                # Profitability metrics
                "grossProfitMargin": period.get("grossProfitMargin"),
                "operatingProfitMargin": period.get("operatingProfitMargin"),
                "netProfitMargin": period.get("netProfitMargin"),
                "returnOnEquity": period.get("returnOnEquity") if "returnOnEquity" in period else None,  # This field might be missing
                "returnOnAssets": period.get("assetTurnover") * period.get("netProfitMargin") if period.get("assetTurnover") and period.get("netProfitMargin") else None,
                "returnOnCapitalEmployed": period.get("returnOnCapitalEmployed") if "returnOnCapitalEmployed" in period else None,
                
                # Important efficiency metrics that affect profitability
                "assetTurnover": period.get("assetTurnover"),
                "inventoryTurnover": period.get("inventoryTurnover"),
                
                # Context metrics
                "effectiveTaxRate": period.get("effectiveTaxRate")
            }
            profitability_metrics.append(metrics)
        
        return profitability_metrics
        
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    metrics = get_profitability_cluster("AAPL")
    for period in metrics:
        print(f"Period: {period['date']} - FY{period['fiscalYear']}")
        print(f"  Net Profit Margin: {period['netProfitMargin']:.2%}")
        print(f"  Operating Margin: {period['operatingProfitMargin']:.2%}")
        print(f"  Gross Margin: {period['grossProfitMargin']:.2%}")
        print(f"  Return on Assets: {period['returnOnAssets']:.2%}" if period['returnOnAssets'] else "  Return on Assets: N/A")
        print("  ---")