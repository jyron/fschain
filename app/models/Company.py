from typing import Optional
from pydantic import BaseModel
from app.models.financial_models import CompanyFinancialMetrics


class Company(BaseModel):
    ticker: Optional[str]
    fiscalYear: Optional[str]
    financials: CompanyFinancialMetrics
