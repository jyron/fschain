from typing import Optional
from pydantic import BaseModel


# Return on Capital
class ReturnOnCapital(BaseModel):
    returnOnAssetsTTM: Optional[float]
    operatingReturnOnAssetsTTM: Optional[float]
    returnOnTangibleAssetsTTM: Optional[float]
    returnOnEquityTTM: Optional[float]
    returnOnInvestedCapitalTTM: Optional[float]
    returnOnCapitalEmployedTTM: Optional[float]


# Capex and Cost Structure
class CapexAndCostStructure(BaseModel):
    capexToOperatingCashFlowTTM: Optional[float]
    capexToDepreciationTTM: Optional[float]
    capexToRevenueTTM: Optional[float]
    salesGeneralAndAdministrativeToRevenueTTM: Optional[float]
    researchAndDevelopementToRevenueTTM: Optional[float]
    stockBasedCompensationToRevenueTTM: Optional[float]


# Asset and Capital Quality
class AssetAndCapitalQuality(BaseModel):
    intangiblesToTotalAssetsTTM: Optional[float]
    workingCapitalTTM: Optional[float]
    investedCapitalTTM: Optional[float]
    netCurrentAssetValueTTM: Optional[float]
    tangibleAssetValueTTM: Optional[float]


# Cash Cycle
class CashCycle(BaseModel):
    daysOfSalesOutstandingTTM: Optional[float]
    daysOfPayablesOutstandingTTM: Optional[float]
    daysOfInventoryOutstandingTTM: Optional[float]
    operatingCycleTTM: Optional[float]
    cashConversionCycleTTM: Optional[float]


# Profitability
class Profitability(BaseModel):
    grossProfitMarginTTM: Optional[float]
    operatingProfitMarginTTM: Optional[float]
    ebitMarginTTM: Optional[float]
    ebitdaMarginTTM: Optional[float]
    pretaxProfitMarginTTM: Optional[float]
    netProfitMarginTTM: Optional[float]
    bottomLineProfitMarginTTM: Optional[float]
    continuousOperationsProfitMarginTTM: Optional[float]


# Cash Flow Strength
class CashFlowStrength(BaseModel):
    operatingCashFlowRatioTTM: Optional[float]
    operatingCashFlowSalesRatioTTM: Optional[float]
    freeCashFlowOperatingCashFlowRatioTTM: Optional[float]
    capitalExpenditureCoverageRatioTTM: Optional[float]
    dividendPaidAndCapexCoverageRatioTTM: Optional[float]
    operatingCashFlowCoverageRatioTTM: Optional[float]
    shortTermOperatingCashFlowCoverageRatioTTM: Optional[float]


# Efficiency
class Efficiency(BaseModel):
    receivablesTurnoverTTM: Optional[float]
    payablesTurnoverTTM: Optional[float]
    inventoryTurnoverTTM: Optional[float]
    fixedAssetTurnoverTTM: Optional[float]
    assetTurnoverTTM: Optional[float]
    workingCapitalTurnoverRatioTTM: Optional[float]


# Liquidity
class Liquidity(BaseModel):
    currentRatioTTM: Optional[float]
    quickRatioTTM: Optional[float]
    cashRatioTTM: Optional[float]


# Solvency
class Solvency(BaseModel):
    debtToEquityRatioTTM: Optional[float]
    debtToAssetsRatioTTM: Optional[float]
    debtToCapitalRatioTTM: Optional[float]
    longTermDebtToCapitalRatioTTM: Optional[float]
    financialLeverageRatioTTM: Optional[float]
    solvencyRatioTTM: Optional[float]
    debtServiceCoverageRatioTTM: Optional[float]
    interestCoverageRatioTTM: Optional[float]


# Per Share Fundamentals
class PerShareFundamentals(BaseModel):
    revenuePerShareTTM: Optional[float]
    netIncomePerShareTTM: Optional[float]
    cashPerShareTTM: Optional[float]
    bookValuePerShareTTM: Optional[float]
    tangibleBookValuePerShareTTM: Optional[float]
    shareholdersEquityPerShareTTM: Optional[float]
    operatingCashFlowPerShareTTM: Optional[float]
    capexPerShareTTM: Optional[float]
    freeCashFlowPerShareTTM: Optional[float]
    interestDebtPerShareTTM: Optional[float]


# Tax and Earnings Structure
class TaxAndEarningsStructure(BaseModel):
    effectiveTaxRateTTM: Optional[float]
    netIncomePerEBTTTM: Optional[float]
    ebtPerEbitTTM: Optional[float]


# Root company model
class CompanyFinancialMetrics(BaseModel):
    returnOnCapital: ReturnOnCapital
    capexAndCostStructure: CapexAndCostStructure
    assetAndCapitalQuality: AssetAndCapitalQuality
    cashCycle: CashCycle
    profitability: Profitability
    cashFlowStrength: CashFlowStrength
    efficiency: Efficiency
    liquidity: Liquidity
    solvency: Solvency
    perShareFundamentals: PerShareFundamentals
    taxAndEarningsStructure: TaxAndEarningsStructure
