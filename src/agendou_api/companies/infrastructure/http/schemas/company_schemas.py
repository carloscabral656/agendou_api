from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from agendou_api.companies.domain.company import Company
from agendou_api.companies.domain.enums import CompanyStatus


class CompanyPublic(BaseModel):
    id: UUID
    legal_name: str
    trade_name: str | None
    document_number: str | None
    email: str | None
    phone: str | None
    website: str | None
    timezone: str
    currency: str
    status: CompanyStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


def company_to_public(c: Company) -> CompanyPublic:
    assert c.id is not None
    return CompanyPublic(
        id=c.id,
        legal_name=c.legal_name,
        trade_name=c.trade_name,
        document_number=c.document_number,
        email=c.email,
        phone=c.phone,
        website=c.website,
        timezone=c.timezone,
        currency=c.currency,
        status=c.status,
        created_at=c.created_at,
        updated_at=c.updated_at,
    )


class PatchCompanyBody(BaseModel):
    legal_name: str | None = Field(default=None, min_length=1, max_length=180)
    trade_name: str | None = Field(default=None, max_length=180)
    document_number: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    website: str | None = Field(default=None, max_length=180)
    timezone: str | None = Field(default=None, max_length=80)
    currency: str | None = Field(default=None, max_length=10)
    status: CompanyStatus | None = None


class OnboardCompanyBody(BaseModel):
    legal_name: str = Field(..., min_length=1, max_length=180)
    trade_name: str | None = Field(default=None, max_length=180)
    document_number: str | None = Field(default=None, max_length=30)
    company_email: EmailStr | None = None
    company_phone: str | None = Field(default=None, max_length=30)
    website: str | None = Field(default=None, max_length=180)
    timezone: str = Field(default="America/Sao_Paulo", max_length=80)
    currency: str = Field(default="BRL", max_length=10)
    admin_full_name: str = Field(..., min_length=1, max_length=180)
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8, max_length=128)
