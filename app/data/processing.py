"""
Data processing module for transforming financial data.
"""
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
from app.models.Company import Company
from app.models.financial_models import (
    CompanyFinancialMetrics, ReturnOnCapital, CapexAndCostStructure, 
    AssetAndCapitalQuality, CashCycle, Profitability, CashFlowStrength, 
    Efficiency, Liquidity, Solvency, PerShareFundamentals, TaxAndEarningsStructure
)
from app.api.fmp_client import FMPClient
from app.utils.schema_loader import load_metrics_schema


def create_financial_metrics_object(data: Dict[str, Any]) -> CompanyFinancialMetrics:
    """
    Create a CompanyFinancialMetrics object from structured financial data.
    
    Args:
        data: Structured financial data dictionary with categorized metrics
        
    Returns:
        CompanyFinancialMetrics object
    """
    return CompanyFinancialMetrics(
        returnOnCapital=ReturnOnCapital(**data.get("ReturnOnCapital", {})),
        capexAndCostStructure=CapexAndCostStructure(**data.get("CapexAndCostStructure", {})),
        assetAndCapitalQuality=AssetAndCapitalQuality(**data.get("AssetAndCapitalQuality", {})),
        cashCycle=CashCycle(**data.get("CashCycle", {})),
        profitability=Profitability(**data.get("Profitability", {})),
        cashFlowStrength=CashFlowStrength(**data.get("CashFlowStrength", {})),
        efficiency=Efficiency(**data.get("Efficiency", {})),
        liquidity=Liquidity(**data.get("Liquidity", {})),
        solvency=Solvency(**data.get("Solvency", {})),
        perShareFundamentals=PerShareFundamentals(**data.get("PerShareFundamentals", {})),
        taxAndEarningsStructure=TaxAndEarningsStructure(**data.get("TaxAndEarningsStructure", {}))
    )


def create_company_objects(tickers: List[str], fmp_client: FMPClient = None) -> List[Company]:
    """
    Create Company objects from a list of tickers using the FMP API client.
    
    Args:
        tickers: List of stock symbols
        fmp_client: FMP API client instance. If None, creates a new one.
        
    Returns:
        List of Company objects
    """
    if fmp_client is None:
        fmp_client = FMPClient()
    
    companies = []
    metrics_schema = load_metrics_schema()
    
    # Fetch data for all tickers in parallel
    ftokens_data = fmp_client.fetch_and_build_ftokens(tickers, metrics_schema)
    
    for ticker in tickers:
        if ticker in ftokens_data:
            ftoken_data = ftokens_data[ticker]
            company = Company(
                ticker=ftoken_data.get("symbol", ticker),
                fiscalYear=str(datetime.utcnow().year),
                financials=create_financial_metrics_object(ftoken_data)
            )
            companies.append(company)
            print(f"Created company for {ticker}")
        else:
            print(f"No data available for {ticker}")
    
    return companies


def extract_all_metrics_dataframe(companies: List[Company]) -> pd.DataFrame:
    """
    Extract all metrics from Company objects into a flat DataFrame.
    
    Args:
        companies: List of Company objects
    
    Returns:
        DataFrame where rows are companies and columns are individual metrics
    """
    data_dict = []
    
    for company in companies:
        # Dictionary to store flattened metrics for this company
        flat_metrics = {'ticker': company.ticker, 'fiscalYear': company.fiscalYear}
        
        # Extract metrics from each category
        metrics_categories = [
            ('returnOnCapital', company.financials.returnOnCapital),
            ('capexAndCostStructure', company.financials.capexAndCostStructure),
            ('assetAndCapitalQuality', company.financials.assetAndCapitalQuality),
            ('cashCycle', company.financials.cashCycle),
            ('profitability', company.financials.profitability),
            ('cashFlowStrength', company.financials.cashFlowStrength),
            ('efficiency', company.financials.efficiency),
            ('liquidity', company.financials.liquidity),
            ('solvency', company.financials.solvency),
            ('perShareFundamentals', company.financials.perShareFundamentals),
            ('taxAndEarningsStructure', company.financials.taxAndEarningsStructure)
        ]
        
        for category_name, category_obj in metrics_categories:
            category_dict = category_obj.model_dump()
            for metric_name, value in category_dict.items():
                flat_metrics[metric_name] = value
        
        data_dict.append(flat_metrics)
    
    df = pd.DataFrame(data_dict)
    
    if 'ticker' in df.columns:
        df.set_index('ticker', inplace=True)
    
    return df


def transform_financial_data(raw_data: Dict[str, Dict[str, Any]], metrics_schema: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Transform raw financial data from the API into a structured DataFrame.
    
    Args:
        raw_data: Dictionary mapping symbols to their raw financial data
        metrics_schema: Schema defining metric categories. If None, loads default.
        
    Returns:
        DataFrame with processed financial metrics
    """
    if metrics_schema is None:
        metrics_schema = load_metrics_schema()
    
    # Create FMP client instance for building FToken objects
    fmp_client = FMPClient()
    
    # Transform raw data to FToken objects
    companies = []
    for symbol, data in raw_data.items():
        ftoken_data = fmp_client.build_ftoken_object(data, metrics_schema)
        company = Company(
            ticker=symbol,
            fiscalYear=str(datetime.utcnow().year),
            financials=create_financial_metrics_object(ftoken_data)
        )
        companies.append(company)
    
    return extract_all_metrics_dataframe(companies) 