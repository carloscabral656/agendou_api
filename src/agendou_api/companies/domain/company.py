from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from agendou_api.companies.domain.enums import CompanyStatus


@dataclass
class Company:
    legal_name: str
    id: UUID | None = None
    trade_name: str | None = None
    document_number: str | None = None
    email: str | None = None
    phone: str | None = None
    website: str | None = None
    timezone: str = "America/Sao_Paulo"
    currency: str = "BRL"
    status: CompanyStatus = CompanyStatus.active
    created_at: datetime | None = None
    updated_at: datetime | None = None
