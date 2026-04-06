from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from agendou_api.shared.infrastructure.database.base import Base


class CompanySettingsModel(Base):
    __tablename__ = "company_settings"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    company_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    booking_min_notice_minutes: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        server_default="60",
    )
    booking_max_days_ahead: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        server_default="60",
    )
    cancellation_min_notice_minutes: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        server_default="1440",
    )
    reschedule_min_notice_minutes: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        server_default="1440",
    )
    allow_online_booking: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        server_default="true",
    )
    allow_waitlist: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        server_default="true",
    )
    require_payment_advance: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        server_default="false",
    )
    default_slot_interval_minutes: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        server_default="30",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
