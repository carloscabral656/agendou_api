"""users, customers, staff_profiles

Revision ID: 005_users_customers_staff
Revises: 004_tenant_core
Create Date: 2026-04-06

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "005_users_customers_staff"
down_revision: str | None = "004_tenant_core"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

user_role = postgresql.ENUM(
    "super_admin",
    "company_admin",
    "manager",
    "staff",
    "customer",
    name="user_role",
    create_type=False,
)

user_status = postgresql.ENUM(
    "active",
    "inactive",
    "suspended",
    "pending",
    name="user_status",
    create_type=False,
)

notification_channel = postgresql.ENUM(
    "email",
    "sms",
    "whatsapp",
    "push",
    "in_app",
    name="notification_channel",
    create_type=False,
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True)),
        sa.Column("full_name", sa.String(length=180), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("phone", sa.String(length=30)),
        sa.Column("password_hash", sa.String(length=255)),
        sa.Column("role", user_role, nullable=False),
        sa.Column(
            "status",
            user_status,
            nullable=False,
            server_default=sa.text("'active'::user_status"),
        ),
        sa.Column("avatar_url", sa.String(length=255)),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
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
            ondelete="SET NULL",
        ),
        sa.UniqueConstraint("company_id", "email", name="uq_users_company_id_email"),
    )
    op.create_index("ix_users_company_id", "users", ["company_id"])
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "customers",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True)),
        sa.Column("full_name", sa.String(length=180), nullable=False),
        sa.Column("email", sa.String(length=180)),
        sa.Column("phone", sa.String(length=30)),
        sa.Column("cpf", sa.String(length=20)),
        sa.Column("birth_date", sa.Date()),
        sa.Column("gender", sa.String(length=30)),
        sa.Column("notes", sa.Text()),
        sa.Column("preferred_channel", notification_channel),
        sa.Column(
            "lgpd_consent",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "marketing_consent",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
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
            ["user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_customers_company_id", "customers", ["company_id"])
    op.create_index("ix_customers_email", "customers", ["email"])
    op.create_index("ix_customers_phone", "customers", ["phone"])

    op.create_table(
        "staff_profiles",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unit_id", postgresql.UUID(as_uuid=True)),
        sa.Column("title", sa.String(length=120)),
        sa.Column("bio", sa.Text()),
        sa.Column(
            "commission_percentage",
            sa.Numeric(5, 2),
            server_default=sa.text("0"),
        ),
        sa.Column("color_hex", sa.String(length=10)),
        sa.Column(
            "is_bookable",
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
        sa.UniqueConstraint("user_id", name="uq_staff_profiles_user_id"),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["units.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_staff_profiles_company_id", "staff_profiles", ["company_id"])
    op.create_index("ix_staff_profiles_unit_id", "staff_profiles", ["unit_id"])


def downgrade() -> None:
    op.drop_index("ix_staff_profiles_unit_id", table_name="staff_profiles")
    op.drop_index("ix_staff_profiles_company_id", table_name="staff_profiles")
    op.drop_table("staff_profiles")
    op.drop_index("ix_customers_phone", table_name="customers")
    op.drop_index("ix_customers_email", table_name="customers")
    op.drop_index("ix_customers_company_id", table_name="customers")
    op.drop_table("customers")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_company_id", table_name="users")
    op.drop_table("users")
