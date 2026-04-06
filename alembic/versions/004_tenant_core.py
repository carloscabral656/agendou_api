"""companies, company_settings, units

Revision ID: 004_tenant_core
Revises: 003_saas_enums
Create Date: 2026-04-06

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "004_tenant_core"
down_revision: str | None = "003_saas_enums"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

company_status = postgresql.ENUM(
    "active",
    "inactive",
    "blocked",
    name="company_status",
    create_type=False,
)

unit_status = postgresql.ENUM(
    "active",
    "inactive",
    name="unit_status",
    create_type=False,
)


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("legal_name", sa.String(length=180), nullable=False),
        sa.Column("trade_name", sa.String(length=180)),
        sa.Column("document_number", sa.String(length=30)),
        sa.Column("email", sa.String(length=180)),
        sa.Column("phone", sa.String(length=30)),
        sa.Column("website", sa.String(length=180)),
        sa.Column(
            "timezone",
            sa.String(length=80),
            nullable=False,
            server_default=sa.text("'America/Sao_Paulo'"),
        ),
        sa.Column(
            "currency",
            sa.String(length=10),
            nullable=False,
            server_default=sa.text("'BRL'"),
        ),
        sa.Column(
            "status",
            company_status,
            nullable=False,
            server_default=sa.text("'active'::company_status"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_number", name="uq_companies_document_number"),
    )
    op.create_table(
        "company_settings",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "booking_min_notice_minutes",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("60"),
        ),
        sa.Column(
            "booking_max_days_ahead",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("60"),
        ),
        sa.Column(
            "cancellation_min_notice_minutes",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1440"),
        ),
        sa.Column(
            "reschedule_min_notice_minutes",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1440"),
        ),
        sa.Column(
            "allow_online_booking",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "allow_waitlist",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "require_payment_advance",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "default_slot_interval_minutes",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("30"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id", name="uq_company_settings_company_id"),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_table(
        "units",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=180)),
        sa.Column("phone", sa.String(length=30)),
        sa.Column(
            "status",
            unit_status,
            nullable=False,
            server_default=sa.text("'active'::unit_status"),
        ),
        sa.Column("zip_code", sa.String(length=20)),
        sa.Column("state", sa.String(length=80)),
        sa.Column("city", sa.String(length=120)),
        sa.Column("district", sa.String(length=120)),
        sa.Column("street", sa.String(length=180)),
        sa.Column("number", sa.String(length=30)),
        sa.Column("complement", sa.String(length=120)),
        sa.Column("latitude", sa.Numeric(10, 7)),
        sa.Column("longitude", sa.Numeric(10, 7)),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_units_company_id", "units", ["company_id"])


def downgrade() -> None:
    op.drop_index("ix_units_company_id", table_name="units")
    op.drop_table("units")
    op.drop_table("company_settings")
    op.drop_table("companies")
