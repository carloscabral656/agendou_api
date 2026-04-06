"""appointments and related tables

Revision ID: 008_appointments
Revises: 007_schedule_resources
Create Date: 2026-04-06

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "008_appointments"
down_revision: str | None = "007_schedule_resources"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

appointment_status = postgresql.ENUM(
    "pending",
    "confirmed",
    "checked_in",
    "in_progress",
    "completed",
    "cancelled",
    "no_show",
    "rescheduled",
    name="appointment_status",
    create_type=False,
)

recurrence_frequency = postgresql.ENUM(
    "daily",
    "weekly",
    "monthly",
    name="recurrence_frequency",
    create_type=False,
)


def upgrade() -> None:
    op.create_table(
        "appointments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("staff_profile_id", postgresql.UUID(as_uuid=True)),
        sa.Column("room_id", postgresql.UUID(as_uuid=True)),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("coupon_id", postgresql.UUID(as_uuid=True)),
        sa.Column(
            "status",
            appointment_status,
            nullable=False,
            server_default=sa.text("'pending'::appointment_status"),
        ),
        sa.Column(
            "source",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'web'"),
        ),
        sa.Column("scheduled_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("scheduled_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("check_in_at", sa.DateTime(timezone=True)),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("cancelled_at", sa.DateTime(timezone=True)),
        sa.Column("cancellation_reason", sa.Text()),
        sa.Column("notes", sa.Text()),
        sa.Column("internal_notes", sa.Text()),
        sa.Column("listed_price", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "discount_amount",
            sa.Numeric(12, 2),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("final_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True)),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True)),
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
            ["unit_id"],
            ["units.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["staff_profile_id"],
            ["staff_profiles.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["coupon_id"],
            ["coupons.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["updated_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_appointments_company_id", "appointments", ["company_id"])
    op.create_index(
        "ix_appointments_unit_id_scheduled_start",
        "appointments",
        ["unit_id", "scheduled_start"],
    )
    op.create_index(
        "ix_appointments_customer_id_scheduled_start",
        "appointments",
        ["customer_id", "scheduled_start"],
    )
    op.create_index(
        "ix_appointments_staff_profile_id_scheduled_start",
        "appointments",
        ["staff_profile_id", "scheduled_start"],
    )
    op.create_index(
        "ix_appointments_status_scheduled_start",
        "appointments",
        ["status", "scheduled_start"],
    )

    op.create_table(
        "appointment_status_history",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("old_status", appointment_status),
        sa.Column("new_status", appointment_status, nullable=False),
        sa.Column("changed_by", postgresql.UUID(as_uuid=True)),
        sa.Column("reason", sa.Text()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["appointment_id"],
            ["appointments.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["changed_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        "ix_appointment_status_history_appointment_id_created_at",
        "appointment_status_history",
        ["appointment_id", "created_at"],
    )

    op.create_table(
        "appointment_services",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("staff_profile_id", postgresql.UUID(as_uuid=True)),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "sort_order",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["appointment_id"],
            ["appointments.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["staff_profile_id"],
            ["staff_profiles.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        "ix_appointment_services_appointment_id",
        "appointment_services",
        ["appointment_id"],
    )

    op.create_table(
        "appointment_resources",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "quantity_used",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "appointment_id",
            "resource_id",
            name="uq_appointment_resources_appointment_id_resource_id",
        ),
        sa.ForeignKeyConstraint(
            ["appointment_id"],
            ["appointments.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["resource_id"],
            ["resources.id"],
            ondelete="RESTRICT",
        ),
    )

    op.create_table(
        "recurring_appointments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("staff_profile_id", postgresql.UUID(as_uuid=True)),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("frequency", recurrence_frequency, nullable=False),
        sa.Column(
            "interval_value",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),
        sa.Column("weekday", sa.Integer()),
        sa.Column("day_of_month", sa.Integer()),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date()),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column(
            "active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column("created_by", postgresql.UUID(as_uuid=True)),
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
            ["unit_id"],
            ["units.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["staff_profile_id"],
            ["staff_profiles.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )


def downgrade() -> None:
    op.drop_table("recurring_appointments")
    op.drop_table("appointment_resources")
    op.drop_index(
        "ix_appointment_services_appointment_id",
        table_name="appointment_services",
    )
    op.drop_table("appointment_services")
    op.drop_index(
        "ix_appointment_status_history_appointment_id_created_at",
        table_name="appointment_status_history",
    )
    op.drop_table("appointment_status_history")
    op.drop_index(
        "ix_appointments_status_scheduled_start",
        table_name="appointments",
    )
    op.drop_index(
        "ix_appointments_staff_profile_id_scheduled_start",
        table_name="appointments",
    )
    op.drop_index(
        "ix_appointments_customer_id_scheduled_start",
        table_name="appointments",
    )
    op.drop_index(
        "ix_appointments_unit_id_scheduled_start",
        table_name="appointments",
    )
    op.drop_index("ix_appointments_company_id", table_name="appointments")
    op.drop_table("appointments")
