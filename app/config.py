"""
Application configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
FMP_API_KEY = os.getenv("FMP_API_KEY")

# File Paths
METRICS_SCHEMA_PATH = "app/specifications/ftoken-metrics.json"
STOCK_SYMBOLS_PATH = "data/stock_symbols.json"
METRIC_BOUNDARIES_PATH = "data/metric_boundaries.json"
COMPANY_INDEXES_OUTPUT_PATH = "data/company_financial_indexes.csv"

# API URLs
FMP_BASE_URL = "https://financialmodelingprep.com/stable"
FMP_RATIOS_TTM_URL = f"{FMP_BASE_URL}/ratios-ttm"
FMP_KEY_METRICS_TTM_URL = f"{FMP_BASE_URL}/key-metrics-ttm"
FMP_COMPANY_PROFILE_URL = f"{FMP_BASE_URL}/profile"

# Processing Configuration
DEFAULT_BATCH_SIZE = 10 