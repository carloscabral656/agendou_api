from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from agendou_api.companies.domain.company_settings import CompanySettings


class CompanySettingsPublic(BaseModel):
    id: UUID
    company_id: UUID
    booking_min_notice_minutes: int
    booking_max_days_ahead: int
    cancellation_min_notice_minutes: int
    reschedule_min_notice_minutes: int
    allow_online_booking: bool
    allow_waitlist: bool
    require_payment_advance: bool
    default_slot_interval_minutes: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


def settings_to_public(s: CompanySettings) -> CompanySettingsPublic:
    assert s.id is not None
    return CompanySettingsPublic(
        id=s.id,
        company_id=s.company_id,
        booking_min_notice_minutes=s.booking_min_notice_minutes,
        booking_max_days_ahead=s.booking_max_days_ahead,
        cancellation_min_notice_minutes=s.cancellation_min_notice_minutes,
        reschedule_min_notice_minutes=s.reschedule_min_notice_minutes,
        allow_online_booking=s.allow_online_booking,
        allow_waitlist=s.allow_waitlist,
        require_payment_advance=s.require_payment_advance,
        default_slot_interval_minutes=s.default_slot_interval_minutes,
        created_at=s.created_at,
        updated_at=s.updated_at,
    )


class PatchCompanySettingsBody(BaseModel):
    booking_min_notice_minutes: int | None = Field(default=None, ge=0)
    booking_max_days_ahead: int | None = Field(default=None, ge=1)
    cancellation_min_notice_minutes: int | None = Field(default=None, ge=0)
    reschedule_min_notice_minutes: int | None = Field(default=None, ge=0)
    allow_online_booking: bool | None = None
    allow_waitlist: bool | None = None
    require_payment_advance: bool | None = None
    default_slot_interval_minutes: int | None = Field(default=None, ge=1)
