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
