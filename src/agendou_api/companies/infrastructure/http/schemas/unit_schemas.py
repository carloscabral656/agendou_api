from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from agendou_api.companies.domain.enums import UnitStatus
from agendou_api.companies.domain.unit import Unit


class UnitPublic(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    email: str | None
    phone: str | None
    status: UnitStatus
    zip_code: str | None
    state: str | None
    city: str | None
    district: str | None
    street: str | None
    number: str | None
    complement: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


def unit_to_public(u: Unit) -> UnitPublic:
    assert u.id is not None
    return UnitPublic(
        id=u.id,
        company_id=u.company_id,
        name=u.name,
        email=u.email,
        phone=u.phone,
        status=u.status,
        zip_code=u.zip_code,
        state=u.state,
        city=u.city,
        district=u.district,
        street=u.street,
        number=u.number,
        complement=u.complement,
        latitude=u.latitude,
        longitude=u.longitude,
        created_at=u.created_at,
        updated_at=u.updated_at,
    )


class CreateUnitBody(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    status: UnitStatus | None = None
    zip_code: str | None = Field(default=None, max_length=20)
    state: str | None = Field(default=None, max_length=80)
    city: str | None = Field(default=None, max_length=120)
    district: str | None = Field(default=None, max_length=120)
    street: str | None = Field(default=None, max_length=180)
    number: str | None = Field(default=None, max_length=30)
    complement: str | None = Field(default=None, max_length=120)
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class PatchUnitBody(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    status: UnitStatus | None = None
    zip_code: str | None = Field(default=None, max_length=20)
    state: str | None = Field(default=None, max_length=80)
    city: str | None = Field(default=None, max_length=120)
    district: str | None = Field(default=None, max_length=120)
    street: str | None = Field(default=None, max_length=180)
    number: str | None = Field(default=None, max_length=30)
    complement: str | None = Field(default=None, max_length=120)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
