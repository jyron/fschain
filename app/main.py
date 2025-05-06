from app.services.create_company import createCompany
from app.services.data_collection import fetch_and_create_companies, extract_all_metrics_dataframe
from app.services.calculate_min_max import calculate_metric_boundaries, save_metric_boundaries, load_metric_boundaries
from app.services.calculate_index import calculate_all_companies_indexes
import time
import pandas as pd

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

def recalculate_and_save_boundaries():
    """Fetch data, calculate boundaries, and save them"""
    companies = fetch_and_create_companies(tickers)
    df = extract_all_metrics_dataframe(companies)
    boundaries = calculate_metric_boundaries(df)
    save_metric_boundaries(boundaries)
    return df, boundaries

def calculate_indexes_demo(num_companies=5):
    """Calculate indexes for a subset of companies"""

    boundaries = load_metric_boundaries()
    
    subset_tickers = tickers[:num_companies]
    companies = fetch_and_create_companies(subset_tickers)
    companies_df = extract_all_metrics_dataframe(companies)
    
    
    indexes_df = calculate_all_companies_indexes(companies_df, boundaries)
    
    print(f"\nFinancial Indexes for {num_companies} companies:")
    print(indexes_df)
    
    
    return companies_df, indexes_df

def calculate_index_for_specific_company(ticker):
    """Calculate index for a specific company"""
   
    boundaries = load_metric_boundaries()
    
   
    company = createCompany(ticker)
    company_df = extract_all_metrics_dataframe([company])
    

    index_df = calculate_all_companies_indexes(company_df, boundaries)
    

    print(f"\nFinancial Index for {ticker}:")
    print(index_df)
    
    return company_df, index_df

def calculate_and_save_all_company_indexes(output_file="company_financial_indexes.csv"):
    """
    Calculate financial indexes for all companies in the tickers list 
    and save the results to a CSV file.
    
    Args:
        output_file: Path to save the CSV file
    
    Returns:
        DataFrame with all company index scores
    """
    print(f"Calculating financial indexes for {len(tickers)} companies...")
    
    boundaries = load_metric_boundaries()
    
    batch_size = 10
    all_company_data = []
    
    for i in range(0, len(tickers), batch_size):
        batch_tickers = tickers[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(tickers) + batch_size - 1)//batch_size}: {batch_tickers}")
        
        try:
            companies = fetch_and_create_companies(batch_tickers)
            companies_df = extract_all_metrics_dataframe(companies)
            all_company_data.append(companies_df)
            

            time.sleep(2)
        except Exception as e:
            print(f"Error processing batch: {e}")
    
    if all_company_data:
        combined_df = pd.concat(all_company_data)
        
        indexes_df = calculate_all_companies_indexes(combined_df, boundaries)

        indexes_df.to_csv(output_file, index=False)
        print(f"Financial indexes saved to {output_file}")

        print("\nTop 10 companies by financial index:")
        top_companies = indexes_df.sort_values('index_score', ascending=False).head(10)
        print(top_companies)
        
        return indexes_df
    else:
        print("No company data collected. Check for errors.")
        return None

if __name__ == "__main__":
    # Uncomment the analysis you want to run
    
    # Recalculate boundaries from scratch
    # recalculate_and_save_boundaries()
    
    # Calculate indexes for 5 companies
    # calculate_indexes_demo(num_companies=5)
    
    # Calculate index for a specific company
    # calculate_index_for_specific_company("AAPL")
    
    # Calculate indexes for all companies and save to CSV
    calculate_and_save_all_company_indexes("data/company_financial_indexes.csv")