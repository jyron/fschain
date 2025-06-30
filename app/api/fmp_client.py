"""
Financial Modeling Prep API client with caching and rate limiting.
"""
import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
import requests
from app.config import FMP_API_KEY, FMP_RATIOS_TTM_URL, FMP_KEY_METRICS_TTM_URL
from app.utils.schema_loader import load_metrics_schema


class FMPClient:
    """
    A robust FMP API client with caching and parallel processing capabilities.
    """
    
    def __init__(self, api_key: str = None, max_workers: int = 10):
        """
        Initialize the FMP client.
        
        Args:
            api_key: FMP API key. If None, uses the one from config.
            max_workers: Maximum number of concurrent threads for parallel requests.
        """
        self.api_key = api_key or FMP_API_KEY
        self.max_workers = max_workers
        self._cache = {}  # In-memory cache for API responses
        self._session = requests.Session()  # Reuse HTTP connections
        
        if not self.api_key:
            raise ValueError("FMP API key is required")
    
    def _make_request(self, url: str) -> Dict[str, Any]:
        """
        Make a request to the FMP API with retry logic for rate limits.
        
        Args:
            url: The complete API URL
            
        Returns:
            API response data as dictionary
        """
        max_retries = 3
        base_delay = 5  # Start with 5 second delay
        
        for attempt in range(max_retries):
            try:
                response = self._session.get(url, timeout=30)
                # Simple rate limiting: 300 calls per minute = 5 per second
                time.sleep(0.2)  # 200ms between calls
                if response.status_code == 429:  # Rate limit hit
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff
                        logging.warning(f"Rate limit hit, waiting {delay} seconds before retry {attempt + 1}")
                        time.sleep(delay)
                        continue
                    else:
                        logging.error(f"Max retries reached for rate-limited request: {url}")
                        return {}
                
                response.raise_for_status()
                data = response.json()
                return data[0] if data else {}
            except Exception as e:
                if attempt < max_retries - 1:
                    logging.warning(f"Request failed (attempt {attempt + 1}), retrying: {e}")
                    time.sleep(2)
                else:
                    logging.error(f"Request failed after {max_retries} attempts: {e}")
                    return {}
        
        return {}
    
    def _fetch_ratios_ttm(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch TTM ratios for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            TTM ratios data
        """
        cache_key = f"ratios_ttm_{symbol}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        url = f"{FMP_RATIOS_TTM_URL}?symbol={symbol}&apikey={self.api_key}"
        data = self._make_request(url)
        self._cache[cache_key] = data
        return data
    
    def _fetch_key_metrics_ttm(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch TTM key metrics for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            TTM key metrics data
        """
        cache_key = f"key_metrics_ttm_{symbol}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        url = f"{FMP_KEY_METRICS_TTM_URL}?symbol={symbol}&apikey={self.api_key}"
        data = self._make_request(url)
        self._cache[cache_key] = data
        return data
    
    def fetch_financial_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch combined financial data for a single symbol with rate limiting.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Combined financial data (ratios + key metrics)
        """
        ratios_data = self._fetch_ratios_ttm(symbol)
        key_metrics_data = self._fetch_key_metrics_ttm(symbol)
        
        # Combine both datasets
        combined_data = {**ratios_data, **key_metrics_data}
        return combined_data
    
    def fetch_data_for_tickers(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Fetch financial data for multiple tickers with rate limiting.
        FMP allows 300 calls per minute, so we add delays.
        
        Args:
            tickers: List of stock symbols
            
        Returns:
            Dictionary mapping symbols to their financial data
        """
        results = {}
        
        for i, symbol in enumerate(tickers):
            data = self.fetch_financial_data(symbol)
            results[symbol] = data
            logging.info(f"Successfully fetched data for {symbol} ({i+1}/{len(tickers)})")
        
        return results
    
    def build_ftoken_object(self, data: Dict[str, Any], metrics_schema: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Transform raw financial data into structured FToken oracle object.
        
        Args:
            data: Raw financial data from API
            metrics_schema: Schema defining metric categories. If None, loads default.
            
        Returns:
            Structured FToken object
        """
        if metrics_schema is None:
            metrics_schema = load_metrics_schema()
        
        result = {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "symbol": data.get("symbol", ""),
        }
        
        for category, metrics in metrics_schema.items():
            result[category] = {}
            for metric in metrics:
                result[category][metric] = data.get(metric, None)
        
        return result
    
    def fetch_and_build_ftoken(self, symbol: str, metrics_schema: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch financial data and build FToken object for a single symbol.
        
        Args:
            symbol: Stock symbol
            metrics_schema: Schema defining metric categories. If None, loads default.
            
        Returns:
            Structured FToken object
        """
        financial_data = self.fetch_financial_data(symbol)
        return self.build_ftoken_object(financial_data, metrics_schema)
    
    def fetch_and_build_ftokens(self, tickers: List[str], metrics_schema: Dict[str, Any] = None) -> Dict[str, Dict[str, Any]]:
        """
        Fetch financial data and build FToken objects for multiple symbols in parallel.
        
        Args:
            tickers: List of stock symbols
            metrics_schema: Schema defining metric categories. If None, loads default.
            
        Returns:
            Dictionary mapping symbols to their FToken objects
        """
        if metrics_schema is None:
            metrics_schema = load_metrics_schema()
        
        financial_data = self.fetch_data_for_tickers(tickers)
        
        results = {}
        for symbol, data in financial_data.items():
            if data:  # Only process if we have data
                results[symbol] = self.build_ftoken_object(data, metrics_schema)
            else:
                logging.warning(f"No data available for {symbol}")
        
        return results
    
    def clear_cache(self):
        """Clear the internal cache."""
        self._cache.clear()
        logging.info("Cache cleared")
    
    def get_cache_info(self) -> Dict[str, int]:
        """
        Get information about the current cache state.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "cache_size": len(self._cache),
            "cached_symbols": len(set(key.split("_")[-1] for key in self._cache.keys()))
        } 