import os
from datetime import datetime
from pprint import pprint
from typing import Any, Dict
import requests
from dotenv import load_dotenv
load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")

def fetchFMP_RATIOS_TTMData(symbol: str) -> Dict[str, Any]:
    """
    Fetch financial data for a given symbol from Financial Modeling Prep API.
    Returns only the most recent data point.
    """
    url = f"https://financialmodelingprep.com/stable/ratios-ttm?symbol={symbol}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else {}

def fetchFMP_KEY_Metrics_TTMData(symbol: str) -> Dict[str, Any]:
    """
    Fetch financial data for a given symbol from Financial Modeling Prep API.
    Returns only the most recent data point.
    """
    url = f"https://financialmodelingprep.com/stable/key-metrics-ttm?symbol={symbol}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else {}

apple_ttm = fetchFMP_RATIOS_TTMData(symbol="AAPL")
meta_ttm = fetchFMP_RATIOS_TTMData(symbol="META")
apple_metrics = fetchFMP_KEY_Metrics_TTMData(symbol="AAPL")
meta_metrics = fetchFMP_KEY_Metrics_TTMData(symbol="META")

print("----------------------")
print("----------------------")
print("Function: fetchFMP_RATIOS_TTM(apple)")
print("----------------------")
print("----------------------")
pprint(fetchFMP_KEY_Metrics_TTMData(symbol="AAPL"))
print("----------------------")
print("----------------------")
print("Function: fetchFMP_KEY_METRICS_TTM(META)")
pprint(fetchFMP_RATIOS_TTMData(symbol="META"))
print("----------------------")
print("----------------------")



def build_ftoken_object(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform raw financial data into structured FToken oracle object.
    """
    metric_categories = {
        "Profitability": [
            "grossProfitMarginTTM",
            "operatingProfitMarginTTM",
            "ebitMarginTTM",
            "ebitdaMarginTTM",
            "pretaxProfitMarginTTM",
            "netProfitMarginTTM",
            "bottomLineProfitMarginTTM",
            "continuousOperationsProfitMarginTTM"
        ],
        "CashFlowStrength": [
            "operatingCashFlowRatioTTM",
            "operatingCashFlowSalesRatioTTM",
            "freeCashFlowOperatingCashFlowRatioTTM",
            "capitalExpenditureCoverageRatioTTM",
            "dividendPaidAndCapexCoverageRatioTTM",
            "operatingCashFlowCoverageRatioTTM",
            "shortTermOperatingCashFlowCoverageRatioTTM"
        ],
        "Efficiency": [
            "receivablesTurnoverTTM",
            "payablesTurnoverTTM",
            "inventoryTurnoverTTM",
            "fixedAssetTurnoverTTM",
            "assetTurnoverTTM",
            "workingCapitalTurnoverRatioTTM"
        ],
        "Liquidity": [
            "currentRatioTTM",
            "quickRatioTTM",
            "cashRatioTTM"
        ],
        "Solvency": [
            "debtToEquityRatioTTM",
            "debtToAssetsRatioTTM",
            "debtToCapitalRatioTTM",
            "longTermDebtToCapitalRatioTTM",
            "financialLeverageRatioTTM",
            "solvencyRatioTTM",
            "debtServiceCoverageRatioTTM",
            "interestCoverageRatioTTM"
        ],
        "PerShareFundamentals": [
            "revenuePerShareTTM",
            "netIncomePerShareTTM",
            "cashPerShareTTM",
            "bookValuePerShareTTM",
            "tangibleBookValuePerShareTTM",
            "shareholdersEquityPerShareTTM",
            "operatingCashFlowPerShareTTM",
            "capexPerShareTTM",
            "freeCashFlowPerShareTTM",
            "interestDebtPerShareTTM"
        ],
        "TaxAndEarningsStructure": [
            "effectiveTaxRateTTM",
            "netIncomePerEBTTTM",
            "ebtPerEbitTTM"
        ]
    }
    
    result = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "symbol": data.get("symbol", ""),
        "FTokenMetricsTTM": {}
    }
    
    for category, metrics in metric_categories.items():
        result["FTokenMetricsTTM"][category] = {}
        
        for metric in metrics:
            result["FTokenMetricsTTM"][category][metric] = data.get(metric, None)
    
    return result


print("FTOKEN DATAS APPLE)")
apple_data = build_ftoken_object(data=apple_ttm)
print("----------------------")
print("----------------------")
print("Function: build_ftoken_object(data=apple_ttm)")
print("----------------------")
pprint(apple_data)
print("FTOKEN DATA META")
META_Data = build_ftoken_object(data=meta_ttm)
print("----------------------")
print("----------------------")
print("Function: build_ftoken_object(data=meta_ttm)")
print("----------------------")
pprint(META_Data)