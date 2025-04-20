import os
from dotenv import load_dotenv
from pprint import pprint
import requests
from datetime import datetime
from typing import Dict, Any

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")


def fetch_ratiosTTM_data(symbol: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch financial ratios data for a given symbol from Financial Modeling Prep API.
    Returns only the most recent data point.
    """
    url = (f"https://financialmodelingprep.com/stable/ratios-ttm?symbol={symbol}&apikey={FMP_API_KEY}")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else {}


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


data = fetch_ratiosTTM_data("META", FMP_API_KEY)
ftoken_object = build_ftoken_object(data)
pprint(ftoken_object)