from typing import Optional
from pydantic import BaseModel
from app.models.financial_models import CompanyFinancialMetrics


class CompanyMetadata(BaseModel):
    symbol: Optional[str]
    companyName: Optional[str]
    price: Optional[float]
    marketCap: Optional[float]
    sector: Optional[str]
    industry: Optional[str]
    country: Optional[str]

class Company(BaseModel):
    ticker: Optional[str]
    fiscalYear: Optional[str]
    financials: CompanyFinancialMetrics
