"""
Main orchestration module for the financial analysis workflow.

This module provides a clean, step-by-step orchestration of:
1. Loading stock tickers
2. Fetching financial data
3. Creating company objects
4. Calculating metric boundaries
5. Computing financial indexes
6. Saving results
"""

import logging
import time
import pandas as pd
from typing import List

# Import from new modular structure
from app.config import DEFAULT_BATCH_SIZE, COMPANY_INDEXES_OUTPUT_PATH
from app.api.fmp_client import FMPClient
from app.data.manager import load_tickers_from_json, save_dataframe_to_csv, save_metric_boundaries, load_metric_boundaries
from app.data.processing import create_company_objects, extract_all_metrics_dataframe
from app.core.calculations import calculate_metric_boundaries
from app.core.scoring import calculate_all_companies_indexes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_stock_tickers() -> List[str]:
    """
    Load stock tickers from the configured JSON file.
    
    Returns:
        List of stock ticker symbols
    """
    logger.info("Loading stock tickers...")
    try:
        tickers = load_tickers_from_json()
        logger.info(f"Successfully loaded {len(tickers)} tickers")
        return tickers
    except Exception as e:
        logger.error(f"Failed to load tickers: {e}")
        raise


def fetch_financial_data(tickers: List[str], batch_size: int = DEFAULT_BATCH_SIZE) -> List:
    """
    Fetch financial data and create company objects in batches.
    
    Args:
        tickers: List of stock symbols
        batch_size: Number of tickers to process in each batch
        
    Returns:
        List of Company objects
    """
    logger.info(f"Fetching financial data for {len(tickers)} companies in batches of {batch_size}...")
    
    fmp_client = FMPClient()
    all_companies = []
    
    # Process tickers in batches
    for i in range(0, len(tickers), batch_size):
        batch_tickers = tickers[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(tickers) + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches}: {len(batch_tickers)} tickers")
        
        batch_companies = create_company_objects(batch_tickers, fmp_client)
        all_companies.extend(batch_companies)
        logger.info(f"Successfully processed {len(batch_companies)} companies in batch {batch_num}")
    
    logger.info(f"Total companies created: {len(all_companies)}")
    return all_companies


def create_metrics_dataframe(companies: List) -> pd.DataFrame:
    """
    Extract all metrics from company objects into a DataFrame.
    
    Args:
        companies: List of Company objects
        
    Returns:
        DataFrame with metrics for all companies
    """
    logger.info("Creating metrics DataFrame...")
    df = extract_all_metrics_dataframe(companies)
    logger.info(f"Created DataFrame with {len(df)} companies and {len(df.columns)} metrics")
    return df


def calculate_and_save_boundaries(metrics_df: pd.DataFrame) -> dict:
    """
    Calculate metric boundaries and save them to file.
    
    Args:
        metrics_df: DataFrame with company metrics
        
    Returns:
        Dictionary of calculated boundaries
    """
    logger.info("Calculating metric boundaries...")
    boundaries = calculate_metric_boundaries(metrics_df)
    save_metric_boundaries(boundaries)
    logger.info(f"Calculated boundaries for {len(boundaries)} metrics")
    return boundaries


def calculate_financial_indexes(metrics_df: pd.DataFrame, boundaries: dict) -> pd.DataFrame:
    """
    Calculate financial indexes for all companies.
    
    Args:
        metrics_df: DataFrame with company metrics
        boundaries: Dictionary of metric boundaries
        
    Returns:
        DataFrame with calculated financial indexes
    """
    logger.info("Calculating financial indexes...")
    indexes_df = calculate_all_companies_indexes(metrics_df, boundaries)
    logger.info(f"Calculated indexes for {len(indexes_df)} companies")
    return indexes_df


def save_results(indexes_df: pd.DataFrame, output_path: str = None) -> str:
    """
    Save the financial indexes to a CSV file.
    
    Args:
        indexes_df: DataFrame with financial indexes
        output_path: Path to save the results file
        
    Returns:
        Path to the saved file
    """
    if output_path is None:
        output_path = COMPANY_INDEXES_OUTPUT_PATH
        
    logger.info(f"Saving results to {output_path}...")
    saved_path = save_dataframe_to_csv(indexes_df, output_path, index=False)
    logger.info(f"Results successfully saved to {saved_path}")
    return saved_path


def display_top_companies(indexes_df: pd.DataFrame, top_n: int = 10):
    """
    Display the top performing companies by financial index.
    
    Args:
        indexes_df: DataFrame with financial indexes
        top_n: Number of top companies to display
    """
    logger.info(f"Displaying top {top_n} companies by financial index...")
    top_companies = indexes_df.sort_values('index_score', ascending=False).head(top_n)
    print(f"\nTop {top_n} companies by financial index:")
    print(top_companies[['ticker', 'index_score']].to_string(index=False))
    print(f"\nFull results saved to: {COMPANY_INDEXES_OUTPUT_PATH}")


def main():
    """
    Main orchestration function that runs the complete financial analysis workflow.
    
    The workflow consists of:
    1. Load stock tickers from configuration file
    2. Fetch financial data from API and create company objects
    3. Extract metrics into a DataFrame
    4. Calculate metric boundaries (10th and 90th percentiles)
    5. Calculate financial indexes for all companies
    6. Save results and display top performers
    """
    start_time = time.time()
    logger.info("Starting financial analysis workflow...")
    
    try:
        # Step 1: Load stock tickers
        tickers = load_stock_tickers()
        
        # Step 2: Fetch financial data and create company objects
        companies = fetch_financial_data(tickers)
        
        if not companies:
            logger.error("No companies were created. Exiting workflow.")
            return
        
        # Step 3: Create metrics DataFrame
        metrics_df = create_metrics_dataframe(companies)
        
        # Step 4: Calculate and save metric boundaries
        boundaries = calculate_and_save_boundaries(metrics_df)
        
        # Step 5: Calculate financial indexes
        indexes_df = calculate_financial_indexes(metrics_df, boundaries)
        
        # Step 6: Save results
        saved_path = save_results(indexes_df)
        
        # Step 7: Display summary
        display_top_companies(indexes_df)
        
        # Workflow summary
        elapsed_time = time.time() - start_time
        logger.info(f"Workflow completed successfully in {elapsed_time:.2f} seconds")
        logger.info(f"Processed {len(companies)} companies")
        logger.info(f"Results saved to: {saved_path}")
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        raise


def recalculate_boundaries_only():
    """
    Utility function to only recalculate metric boundaries.
    Useful when you want to update boundaries without recalculating all indexes.
    """
    logger.info("Recalculating metric boundaries only...")
    
    try:
        # Load tickers and fetch data
        tickers = load_stock_tickers()
        companies = fetch_financial_data(tickers)
        metrics_df = create_metrics_dataframe(companies)
        
        # Calculate and save new boundaries
        boundaries = calculate_and_save_boundaries(metrics_df)
        
        logger.info("Boundary recalculation completed successfully")
        return boundaries
        
    except Exception as e:
        logger.error(f"Boundary recalculation failed: {e}")
        raise


def calculate_indexes_from_existing_boundaries():
    """
    Utility function to calculate indexes using existing boundaries.
    Useful when boundaries are already calculated and you just want to recalculate indexes.
    """
    logger.info("Calculating indexes using existing boundaries...")
    
    try:
        # Load existing boundaries
        boundaries = load_metric_boundaries()
        
        # Load tickers and fetch data
        tickers = load_stock_tickers()
        companies = fetch_financial_data(tickers)
        metrics_df = create_metrics_dataframe(companies)
        
        # Calculate indexes and save results
        indexes_df = calculate_financial_indexes(metrics_df, boundaries)
        saved_path = save_results(indexes_df)
        display_top_companies(indexes_df)
        
        logger.info("Index calculation completed successfully")
        return indexes_df
        
    except Exception as e:
        logger.error(f"Index calculation failed: {e}")
        raise


if __name__ == "__main__":
    # Run the complete workflow
    main()
    
    # Alternative workflows (uncomment as needed):
    
    # Only recalculate boundaries:
    # recalculate_boundaries_only()
    
    # Only calculate indexes using existing boundaries:
    # calculate_indexes_from_existing_boundaries()