from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CompanySettings:
    company_id: UUID
    id: UUID | None = None
    booking_min_notice_minutes: int = 60
    booking_max_days_ahead: int = 60
    cancellation_min_notice_minutes: int = 1440
    reschedule_min_notice_minutes: int = 1440
    allow_online_booking: bool = True
    allow_waitlist: bool = True
    require_payment_advance: bool = False
    default_slot_interval_minutes: int = 30
    created_at: datetime | None = None
    updated_at: datetime | None = None
