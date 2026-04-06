from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.companies.domain.company_settings import CompanySettings
from agendou_api.companies.infrastructure.persistence.models.company_settings_model import (
    CompanySettingsModel,
)


def _to_domain(row: CompanySettingsModel) -> CompanySettings:
    return CompanySettings(
        id=row.id,
        company_id=row.company_id,
        booking_min_notice_minutes=row.booking_min_notice_minutes,
        booking_max_days_ahead=row.booking_max_days_ahead,
        cancellation_min_notice_minutes=row.cancellation_min_notice_minutes,
        reschedule_min_notice_minutes=row.reschedule_min_notice_minutes,
        allow_online_booking=row.allow_online_booking,
        allow_waitlist=row.allow_waitlist,
        require_payment_advance=row.require_payment_advance,
        default_slot_interval_minutes=row.default_slot_interval_minutes,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class SqlAlchemyCompanySettingsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_company_id(self, company_id: UUID) -> CompanySettings | None:
        result = await self._session.execute(
            select(CompanySettingsModel).where(CompanySettingsModel.company_id == company_id),
        )
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def save(self, settings: CompanySettings) -> CompanySettings:
        model = CompanySettingsModel(
            company_id=settings.company_id,
            booking_min_notice_minutes=settings.booking_min_notice_minutes,
            booking_max_days_ahead=settings.booking_max_days_ahead,
            cancellation_min_notice_minutes=settings.cancellation_min_notice_minutes,
            reschedule_min_notice_minutes=settings.reschedule_min_notice_minutes,
            allow_online_booking=settings.allow_online_booking,
            allow_waitlist=settings.allow_waitlist,
            require_payment_advance=settings.require_payment_advance,
            default_slot_interval_minutes=settings.default_slot_interval_minutes,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)

    async def update(self, settings: CompanySettings) -> CompanySettings:
        if settings.id is None:
            msg = "CompanySettings id is required for update"
            raise ValueError(msg)
        result = await self._session.execute(
            select(CompanySettingsModel).where(CompanySettingsModel.id == settings.id),
        )
        model = result.scalar_one_or_none()
        if model is None:
            msg = "Company settings not found"
            raise ValueError(msg)
        if model.company_id != settings.company_id:
            msg = "Company mismatch"
            raise ValueError(msg)
        model.booking_min_notice_minutes = settings.booking_min_notice_minutes
        model.booking_max_days_ahead = settings.booking_max_days_ahead
        model.cancellation_min_notice_minutes = settings.cancellation_min_notice_minutes
        model.reschedule_min_notice_minutes = settings.reschedule_min_notice_minutes
        model.allow_online_booking = settings.allow_online_booking
        model.allow_waitlist = settings.allow_waitlist
        model.require_payment_advance = settings.require_payment_advance
        model.default_slot_interval_minutes = settings.default_slot_interval_minutes
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)
