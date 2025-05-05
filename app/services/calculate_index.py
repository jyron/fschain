import numpy as np
import pandas as pd

# Metric and pillar weights clearly defined as constants
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

# Normalization function clearly defined
def normalize_metric(value, min_val, max_val, inverse=False):
    if max_val == min_val:
        return 0.0
    normalized = (value - min_val) / (max_val - min_val)
    return 1 - normalized if inverse else normalized

# Function to normalize an entire set of metrics for a single company
def normalize_company_metrics(company_metrics, metric_min_max):
    normalized_metrics = {}
    for metric, value in company_metrics.items():
        min_val, max_val = metric_min_max.get(metric, (0, 1))
        inverse = metric in INVERSE_METRICS
        normalized_metrics[metric] = normalize_metric(value, min_val, max_val, inverse)
    return normalized_metrics

# Function to calculate pillar scores for one company
def calculate_pillar_scores(normalized_metrics):
    pillar_scores = {}
    for pillar, metrics in METRIC_WEIGHTS.items():
        pillar_score = sum(normalized_metrics[metric] * weight for metric, weight in metrics.items())
        pillar_scores[pillar] = pillar_score
    return pillar_scores

# Main function to calculate financial index for a single company
def calculate_financial_index(company_metrics, metric_min_max):
    normalized_metrics = normalize_company_metrics(company_metrics, metric_min_max)
    pillar_scores = calculate_pillar_scores(normalized_metrics)
    financial_index = sum(pillar_scores[pillar] * weight for pillar, weight in PILLAR_WEIGHTS.items())
    return financial_index

# Wrapper function to calculate indices for all companies in a dataset
def calculate_indices_for_companies(companies_df):
    metric_min_max = {
        metric: (companies_df[metric].min(), companies_df[metric].max())
        for metric in companies_df.columns
    }
    indices = companies_df.apply(lambda metrics: calculate_financial_index(metrics, metric_min_max), axis=1)
    return indices

# Usage example
# indices_result = calculate_indices_for_companies(df_companies)
# print(indices_result)

# For convenience in displaying results explicitly
def get_indices_dataframe(companies_df):
    indices = calculate_indices_for_companies(companies_df)
    return pd.DataFrame(indices, columns=['Custom Weighted Financial Index'])

