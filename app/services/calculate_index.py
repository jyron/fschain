import numpy as np
import pandas as pd

PILLAR_WEIGHTS = {
    'Profitability': 0.25,
    'Liquidity': 0.20,
    'Efficiency': 0.15,
    'Solvency': 0.15,
    'AssetQuality': 0.10,
    'InvestmentCost': 0.10,
    'PerShareFundamentals': 0.05
}

METRIC_WEIGHTS = {
    'Profitability': {
        'returnOnInvestedCapitalTTM': 0.25,
        'returnOnEquityTTM': 0.20,
        'operatingProfitMarginTTM': 0.20,
        'netProfitMarginTTM': 0.20,
        'ebitdaMarginTTM': 0.15
    },
    'Liquidity': {
        'operatingCashFlowCoverageRatioTTM': 0.30,
        'freeCashFlowOperatingCashFlowRatioTTM': 0.20,
        'currentRatioTTM': 0.20,
        'quickRatioTTM': 0.15,
        'cashRatioTTM': 0.15
    },
    'Efficiency': {
        'assetTurnoverTTM': 0.30,
        'inventoryTurnoverTTM': 0.25,
        'receivablesTurnoverTTM': 0.20,
        'fixedAssetTurnoverTTM': 0.15,
        'workingCapitalTurnoverRatioTTM': 0.10
    },
    'Solvency': {
        'debtToEquityRatioTTM': 0.30,
        'interestCoverageRatioTTM': 0.30,
        'debtToAssetsRatioTTM': 0.20,
        'financialLeverageRatioTTM': 0.20
    },
    'AssetQuality': {
        'intangiblesToTotalAssetsTTM': 0.40,
        'workingCapitalTTM': 0.30,
        'returnOnCapitalEmployedTTM': 0.30
    },
    'InvestmentCost': {
        'capexToRevenueTTM': 0.30,
        'researchAndDevelopementToRevenueTTM': 0.25,
        'capexToOperatingCashFlowTTM': 0.20,
        'capexToDepreciationTTM': 0.15,
        'stockBasedCompensationToRevenueTTM': 0.10
    },
    'PerShareFundamentals': {
        'operatingCashFlowPerShareTTM': 0.30,
        'bookValuePerShareTTM': 0.30,
        'freeCashFlowPerShareTTM': 0.20,
        'netIncomePerShareTTM': 0.20
    }
}

INVERSE_METRICS = [
    'capexToOperatingCashFlowTTM', 'capexToDepreciationTTM', 'capexToRevenueTTM',
    'stockBasedCompensationToRevenueTTM', 'intangiblesToTotalAssetsTTM',
    'debtToEquityRatioTTM', 'debtToAssetsRatioTTM', 'debtToCapitalRatioTTM',
    'financialLeverageRatioTTM', 'effectiveTaxRateTTM', 'cashConversionCycleTTM',
    'daysOfInventoryOutstandingTTM', 'daysOfSalesOutstandingTTM',
    'salesGeneralAndAdministrativeToRevenueTTM'
]

def normalize_metric(value, min_val, max_val, is_inverse=False):
    """
    Normalize a metric value between 0 and 1 using min-max scaling.
    
    Args:
        value: The raw metric value
        min_val: Minimum value (10th percentile)
        max_val: Maximum value (90th percentile)
        is_inverse: If True, lower values are better (e.g., debt ratios)
        
    Returns:
        Normalized value between 0 and 1
    """
    if value is None or pd.isna(value):
        return 0.0
        
    if value < min_val:
        value = min_val
    elif value > max_val:
        value = max_val
    
    if min_val == max_val:
        return 0.5

    normalized = (value - min_val) / (max_val - min_val)

    if is_inverse:
        normalized = 1.0 - normalized
        
    return normalized

def calculate_pillar_score(company_data, boundaries, pillar_name, metrics_weights):
    """
    Calculate score for a single pillar (category) of metrics.
    
    Args:
        company_data: Dictionary or Series containing company metrics
        boundaries: Dictionary of metric boundaries (min, max)
        pillar_name: Name of the pillar to calculate
        metrics_weights: Dictionary of metric weights within the pillar
        
    Returns:
        Pillar score between 0 and 1
    """
    pillar_score = 0.0
    total_weight = 0.0
    
    for metric, weight in metrics_weights.items():
        if metric in company_data and metric in boundaries:
            value = company_data[metric]
            min_val, max_val = boundaries[metric]
            
            is_inverse = metric in INVERSE_METRICS

            norm_value = normalize_metric(value, min_val, max_val, is_inverse)

            pillar_score += norm_value * weight
            total_weight += weight

    return pillar_score / total_weight if total_weight > 0 else 0.0

def calculate_company_index(company_data, boundaries, pillar_weights=PILLAR_WEIGHTS, metric_weights=METRIC_WEIGHTS):
    """
    Calculate the overall financial index for a company.
    
    Args:
        company_data: Dictionary or Series containing company metrics
        boundaries: Dictionary of metric boundaries
        pillar_weights: Dictionary of weights for each pillar
        metric_weights: Dictionary of metric weights within each pillar
        
    Returns:
        Financial index score between 0 and 1
    """
    company_score = 0.0
    total_weight = 0.0
    pillar_scores = {}
    
    for pillar, weight in pillar_weights.items():
        if pillar in metric_weights:
            pillar_score = calculate_pillar_score(
                company_data, 
                boundaries, 
                pillar, 
                metric_weights[pillar]
            )
            
            pillar_scores[pillar] = pillar_score
            
            company_score += pillar_score * weight
            total_weight += weight
    
    final_score = company_score / total_weight if total_weight > 0 else 0.0
    return {
        'index_score': final_score,
        'pillar_scores': pillar_scores
    }

def calculate_all_companies_indexes(companies_data, boundaries):
    """
    Calculate financial indexes for multiple companies.
    
    Args:
        companies_data: DataFrame where rows are companies and columns are metrics
        boundaries: Dictionary of metric boundaries
        
    Returns:
        DataFrame with company tickers and their index scores
    """
    results = []
    
    for ticker, company_data in companies_data.iterrows():
        try:
            index_result = calculate_company_index(company_data, boundaries)
            
            results.append({
                'ticker': ticker,
                'index_score': index_result['index_score'],
                **{f'{pillar}_score': score for pillar, score in index_result['pillar_scores'].items()}
            })
        except Exception as e:
            print(f"Error calculating index for {ticker}: {e}")

    return pd.DataFrame(results)
