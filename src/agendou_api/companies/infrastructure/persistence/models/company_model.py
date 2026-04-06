from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func, text
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from agendou_api.companies.domain.enums import CompanyStatus
from agendou_api.shared.infrastructure.database.base import Base

company_status_pg = PG_ENUM(CompanyStatus, name="company_status", create_type=False)


class CompanyModel(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    legal_name: Mapped[str] = mapped_column(String(180))
    trade_name: Mapped[str | None] = mapped_column(String(180))
    document_number: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(180))
    phone: Mapped[str | None] = mapped_column(String(30))
    website: Mapped[str | None] = mapped_column(String(180))
    timezone: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        server_default=text("'America/Sao_Paulo'"),
    )
    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text("'BRL'"),
    )
    status: Mapped[CompanyStatus] = mapped_column(
        company_status_pg,
        nullable=False,
        server_default=text("'active'::company_status"),
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
