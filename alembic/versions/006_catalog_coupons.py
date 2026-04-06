"""coupons, service_categories, services, service_units, service_staff

Revision ID: 006_catalog_coupons
Revises: 005_users_customers_staff
Create Date: 2026-04-06

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "006_catalog_coupons"
down_revision: str | None = "005_users_customers_staff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

coupon_type = postgresql.ENUM(
    "percentage",
    "fixed_amount",
    name="coupon_type",
    create_type=False,
)

coupon_status = postgresql.ENUM(
    "active",
    "inactive",
    "expired",
    name="coupon_status",
    create_type=False,
)


def upgrade() -> None:
    op.create_table(
        "coupons",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("type", coupon_type, nullable=False),
        sa.Column("value", sa.Numeric(12, 2), nullable=False),
        sa.Column("min_order_amount", sa.Numeric(12, 2)),
        sa.Column("max_discount_amount", sa.Numeric(12, 2)),
        sa.Column("usage_limit", sa.Integer()),
        sa.Column(
            "usage_count",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("starts_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column(
            "status",
            coupon_status,
            nullable=False,
            server_default=sa.text("'active'::coupon_status"),
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
        sa.UniqueConstraint("company_id", "code", name="uq_coupons_company_id_code"),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_coupons_company_id", "coupons", ["company_id"])

    op.create_table(
        "service_categories",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column(
            "sort_order",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
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
        sa.UniqueConstraint(
            "company_id",
            "name",
            name="uq_service_categories_company_id_name",
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_service_categories_company_id", "service_categories", ["company_id"])

    op.create_table(
        "services",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True)),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column(
            "buffer_before_minutes",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "buffer_after_minutes",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "online_booking_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "requires_confirmation",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
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
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["service_categories.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_services_company_id", "services", ["company_id"])
    op.create_index(
        "ix_services_company_id_name",
        "services",
        ["company_id", "name"],
    )

    op.create_table(
        "service_units",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "service_id",
            "unit_id",
            name="uq_service_units_service_id_unit_id",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["units.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "service_staff",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("staff_profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("custom_price", sa.Numeric(12, 2)),
        sa.Column("custom_duration_minutes", sa.Integer()),
        sa.Column(
            "active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "service_id",
            "staff_profile_id",
            name="uq_service_staff_service_id_staff_profile_id",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["staff_profile_id"],
            ["staff_profiles.id"],
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("service_staff")
    op.drop_table("service_units")
    op.drop_index("ix_services_company_id_name", table_name="services")
    op.drop_index("ix_services_company_id", table_name="services")
    op.drop_table("services")
    op.drop_index("ix_service_categories_company_id", table_name="service_categories")
    op.drop_table("service_categories")
    op.drop_index("ix_coupons_company_id", table_name="coupons")
    op.drop_table("coupons")
