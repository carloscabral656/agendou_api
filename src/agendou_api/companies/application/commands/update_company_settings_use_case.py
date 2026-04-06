from uuid import UUID

from agendou_api.companies.application.ports.company_settings_repository import (
    CompanySettingsRepository,
)
from agendou_api.companies.domain.company_settings import CompanySettings


class UpdateCompanySettingsUseCase:
    def __init__(self, settings: CompanySettingsRepository) -> None:
        self._settings = settings

    async def execute(
        self,
        company_id: UUID,
        *,
        booking_min_notice_minutes: int | None = None,
        booking_max_days_ahead: int | None = None,
        cancellation_min_notice_minutes: int | None = None,
        reschedule_min_notice_minutes: int | None = None,
        allow_online_booking: bool | None = None,
        allow_waitlist: bool | None = None,
        require_payment_advance: bool | None = None,
        default_slot_interval_minutes: int | None = None,
    ) -> CompanySettings:
        current = await self._settings.get_by_company_id(company_id)
        if current is None:
            msg = "Company settings not found"
            raise ValueError(msg)
        updated = CompanySettings(
            id=current.id,
            company_id=current.company_id,
            booking_min_notice_minutes=booking_min_notice_minutes
            if booking_min_notice_minutes is not None
            else current.booking_min_notice_minutes,
            booking_max_days_ahead=booking_max_days_ahead
            if booking_max_days_ahead is not None
            else current.booking_max_days_ahead,
            cancellation_min_notice_minutes=cancellation_min_notice_minutes
            if cancellation_min_notice_minutes is not None
            else current.cancellation_min_notice_minutes,
            reschedule_min_notice_minutes=reschedule_min_notice_minutes
            if reschedule_min_notice_minutes is not None
            else current.reschedule_min_notice_minutes,
            allow_online_booking=allow_online_booking
            if allow_online_booking is not None
            else current.allow_online_booking,
            allow_waitlist=allow_waitlist if allow_waitlist is not None else current.allow_waitlist,
            require_payment_advance=require_payment_advance
            if require_payment_advance is not None
            else current.require_payment_advance,
            default_slot_interval_minutes=default_slot_interval_minutes
            if default_slot_interval_minutes is not None
            else current.default_slot_interval_minutes,
            created_at=current.created_at,
            updated_at=current.updated_at,
        )
        return await self._settings.update(updated)
