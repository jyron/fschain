from datetime import datetime
from app.integrations.fmp_client import fetch_and_build_ftoken, load_metrics_schema
from app.models.Company import Company
from app.models.FinancialModel import CompanyFinancialMetrics, ReturnOnCapital, CapexAndCostStructure, AssetAndCapitalQuality, CashCycle, Profitability, CashFlowStrength, Efficiency, Liquidity, Solvency, PerShareFundamentals, TaxAndEarningsStructure
from typing import Dict, Optional
from pprint import pprint


metrics_schema = load_metrics_schema("app/specifications/ftoken-metrics.json")
data = fetch_and_build_ftoken("TSLA", metrics_schema=metrics_schema)

finances = CompanyFinancialMetrics(returnOnCapital=ReturnOnCapital(**data.get("ReturnOnCapital")),
    capexAndCostStructure=CapexAndCostStructure(**data.get("CapexAndCostStructure")),
    assetAndCapitalQuality=AssetAndCapitalQuality(**data.get("AssetAndCapitalQuality")),
    cashCycle=CashCycle(**data.get("CashCycle")),
    profitability=Profitability(**data.get("Profitability")),
    cashFlowStrength=CashFlowStrength(**data.get("CashFlowStrength")),
    efficiency=Efficiency(**data.get("Efficiency")),
    liquidity=Liquidity(**data.get("Liquidity")),
    solvency=Solvency(**data.get("Solvency")),
    perShareFundamentals=PerShareFundamentals(**data.get("PerShareFundamentals")),
    taxAndEarningsStructure=TaxAndEarningsStructure(**data.get("TaxAndEarningsStructure"))
)
company = Company(
    ticker=data.get("symbol"),
    industry=None, 
    fiscalYear=str(datetime.utcnow().year),
    financials=finances
)

pprint(company.model_dump())