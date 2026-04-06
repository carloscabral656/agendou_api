"""reviews, notifications, waitlist, addresses, files, audit_logs

Revision ID: 010_reviews_misc
Revises: 009_payments
Create Date: 2026-04-06

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "010_reviews_misc"
down_revision: str | None = "009_payments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

notification_channel = postgresql.ENUM(
    "email",
    "sms",
    "whatsapp",
    "push",
    "in_app",
    name="notification_channel",
    create_type=False,
)

notification_status = postgresql.ENUM(
    "pending",
    "sent",
    "delivered",
    "read",
    "failed",
    "cancelled",
    name="notification_status",
    create_type=False,
)

waitlist_status = postgresql.ENUM(
    "waiting",
    "notified",
    "accepted",
    "expired",
    "cancelled",
    name="waitlist_status",
    create_type=False,
)

audit_action = postgresql.ENUM(
    "insert",
    "update",
    "delete",
    "login",
    "logout",
    "status_change",
    name="audit_action",
    create_type=False,
)


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("staff_profile_id", postgresql.UUID(as_uuid=True)),
        sa.Column("service_id", postgresql.UUID(as_uuid=True)),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text()),
        sa.Column(
            "anonymous",
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("appointment_id", name="uq_reviews_appointment_id"),
        sa.ForeignKeyConstraint(
            ["appointment_id"],
            ["appointments.id"],
            ondelete="CASCADE",
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
            ondelete="SET NULL",
        ),
    )

    op.create_table(
        "notifications",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True)),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True)),
        sa.Column("channel", notification_channel, nullable=False),
        sa.Column("template_key", sa.String(length=100)),
        sa.Column("recipient", sa.String(length=180), nullable=False),
        sa.Column("subject", sa.String(length=180)),
        sa.Column("content", sa.Text()),
        sa.Column(
            "status",
            notification_status,
            nullable=False,
            server_default=sa.text("'pending'::notification_status"),
        ),
        sa.Column("scheduled_at", sa.DateTime(timezone=True)),
        sa.Column("sent_at", sa.DateTime(timezone=True)),
        sa.Column("delivered_at", sa.DateTime(timezone=True)),
        sa.Column("error_message", sa.Text()),
        sa.Column(
            "created_at",
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
            ["customer_id"],
            ["customers.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["appointment_id"],
            ["appointments.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        "ix_notifications_appointment_id",
        "notifications",
        ["appointment_id"],
    )
    op.create_index(
        "ix_notifications_customer_id",
        "notifications",
        ["customer_id"],
    )
    op.create_index(
        "ix_notifications_status_scheduled_at",
        "notifications",
        ["status", "scheduled_at"],
    )

    op.create_table(
        "waitlist",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("preferred_staff_profile_id", postgresql.UUID(as_uuid=True)),
        sa.Column("preferred_date", sa.Date()),
        sa.Column("preferred_start_time", sa.Time()),
        sa.Column("preferred_end_time", sa.Time()),
        sa.Column(
            "status",
            waitlist_status,
            nullable=False,
            server_default=sa.text("'waiting'::waitlist_status"),
        ),
        sa.Column("notified_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
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
            ["service_id"],
            ["services.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["preferred_staff_profile_id"],
            ["staff_profiles.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        "ix_waitlist_company_id_status",
        "waitlist",
        ["company_id", "status"],
    )
    op.create_index(
        "ix_waitlist_customer_id_status",
        "waitlist",
        ["customer_id", "status"],
    )

    op.create_table(
        "customer_addresses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("label", sa.String(length=80)),
        sa.Column("zip_code", sa.String(length=20)),
        sa.Column("state", sa.String(length=80)),
        sa.Column("city", sa.String(length=120)),
        sa.Column("district", sa.String(length=120)),
        sa.Column("street", sa.String(length=180)),
        sa.Column("number", sa.String(length=30)),
        sa.Column("complement", sa.String(length=120)),
        sa.Column(
            "is_default",
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
            ["customer_id"],
            ["customers.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "files",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True)),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True)),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_url", sa.String(length=500), nullable=False),
        sa.Column("mime_type", sa.String(length=120)),
        sa.Column("size_bytes", sa.BigInteger()),
        sa.Column("entity_type", sa.String(length=50)),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True)),
        sa.Column(
            "created_at",
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
        sa.ForeignKeyConstraint(
            ["uploaded_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )

    op.create_table(
        "audit_logs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True)),
        sa.Column("user_id", postgresql.UUID(as_uuid=True)),
        sa.Column("entity_type", sa.String(length=60), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True)),
        sa.Column("action", audit_action, nullable=False),
        sa.Column("old_data", postgresql.JSONB()),
        sa.Column("new_data", postgresql.JSONB()),
        sa.Column("ip_address", sa.String(length=64)),
        sa.Column("user_agent", sa.String(length=255)),
        sa.Column(
            "created_at",
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        "ix_audit_logs_company_id_created_at",
        "audit_logs",
        ["company_id", "created_at"],
    )
    op.create_index(
        "ix_audit_logs_entity_type_entity_id",
        "audit_logs",
        ["entity_type", "entity_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_audit_logs_entity_type_entity_id",
        table_name="audit_logs",
    )
    op.drop_index(
        "ix_audit_logs_company_id_created_at",
        table_name="audit_logs",
    )
    op.drop_table("audit_logs")
    op.drop_table("files")
    op.drop_table("customer_addresses")
    op.drop_index(
        "ix_waitlist_customer_id_status",
        table_name="waitlist",
    )
    op.drop_index(
        "ix_waitlist_company_id_status",
        table_name="waitlist",
    )
    op.drop_table("waitlist")
    op.drop_index(
        "ix_notifications_status_scheduled_at",
        table_name="notifications",
    )
    op.drop_index(
        "ix_notifications_customer_id",
        table_name="notifications",
    )
    op.drop_index(
        "ix_notifications_appointment_id",
        table_name="notifications",
    )
    op.drop_table("notifications")
    op.drop_table("reviews")
