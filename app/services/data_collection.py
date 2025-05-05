import time
from typing import List
import pandas as pd
from app.models.Company import Company
from app.models.FinancialModel import CompanyFinancialMetrics
from app.services.create_company import createCompany

tickers = [
    "AAPL", "TSLA", "AMZN", "MSFT", "NVDA", "GOOGL", "META", "NFLX", "JPM", "V",
    "BAC", "AMD", "PYPL", "DIS", "T", "PFE", "COST", "INTC", "KO", "TGT", 
    "NKE", "SPY", "BA", "BABA", "XOM", "WMT", "GE", "CSCO", "VZ", "JNJ",
    "CVX", "PLTR", "SQ", "SHOP", "SBUX", "SOFI", "HOOD", "RBLX", "SNAP", "UBER",
    "FDX", "ABBV", "ETSY", "MRNA", "LMT", "GM", "F", "RIVN", "LCID", "CCL",
    "DAL", "UAL", "AAL", "TSM", "SONY", "ET", "NOK", "MRO", "COIN", "SIRI",
    "RIOT", "CPRX", "VWO", "SPYG", "ROKU", "VIAC", "ATVI", "BIDU", "DOCU", "ZM",
    "PINS", "TLRY", "WBA", "MGM", "NIO", "C", "GS", "WFC", "ADBE", "PEP",
    "UNH", "CARR", "FUBO", "HCA", "TWTR", "BILI", "RKT"
]

def fetch_and_create_companies(tickers) ->list[Company]:
    """
    Fetch and create Company objects for the given tickers.
    """
    companies = []
    for ticker in tickers[:5]:
        try:
            company = createCompany(ticker)
            companies.append(company)
            time.sleep(.5)  # To avoid hitting API rate limits
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

# print("Fetching and creating companies...")
# companies = fetch_and_create_companies(tickers[10:13])
# dataframe = extract_all_metrics_dataframe(companies)
# print("DataFrame created:")
# print(dataframe.head())