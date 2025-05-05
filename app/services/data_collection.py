import time
from typing import List
import pandas as pd
from app.models.Company import Company
from app.services.create_company import createCompany


def fetch_and_create_companies(tickers) ->list[Company]:
    """
    Fetch and create Company objects for the given tickers.
    """
    companies = []
    for ticker in tickers:
        try:
            company = createCompany(ticker)
            companies.append(company)
            time.sleep(.5)
        except Exception as e:
            print(f"Error creating company for {ticker}: {e}")
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
