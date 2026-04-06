from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from agendou_api.companies.domain.enums import UnitStatus


@dataclass
class Unit:
    company_id: UUID
    name: str
    id: UUID | None = None
    email: str | None = None
    phone: str | None = None
    status: UnitStatus = UnitStatus.active
    zip_code: str | None = None
    state: str | None = None
    city: str | None = None
    district: str | None = None
    street: str | None = None
    number: str | None = None
    complement: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
