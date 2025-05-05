from app.services.create_company import createCompany
from app.services.data_collection import fetch_and_create_companies, extract_all_metrics_dataframe
from app.services.calculate_min_max import calculate_metric_boundaries, save_metric_boundaries, load_metric_boundaries

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

# companies = fetch_and_create_companies(tickers)
# df  = extract_all_metrics_dataframe(companies)
# boundaries = calculate_metric_boundaries(df)
# save_metric_boundaries(boundaries)
loaded_boundaries = load_metric_boundaries()
print("\nSample metric boundaries:")
for metric in list(loaded_boundaries.keys()):
    min_val, max_val = loaded_boundaries[metric]
    print(f"{metric}: ({min_val:.4f}, {max_val:.4f})")