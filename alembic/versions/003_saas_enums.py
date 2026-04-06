"""create PostgreSQL enum types for SaaS schema

Revision ID: 003_saas_enums
Revises: 002_drop_legacy
Create Date: 2026-04-06

"""

from collections.abc import Sequence

from alembic import op

revision: str = "003_saas_enums"
down_revision: str | None = "002_drop_legacy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TYPE user_role AS ENUM (
            'super_admin', 'company_admin', 'manager', 'staff', 'customer'
        );
        CREATE TYPE user_status AS ENUM (
            'active', 'inactive', 'suspended', 'pending'
        );
        CREATE TYPE company_status AS ENUM (
            'active', 'inactive', 'blocked'
        );
        CREATE TYPE unit_status AS ENUM (
            'active', 'inactive'
        );
        CREATE TYPE appointment_status AS ENUM (
            'pending', 'confirmed', 'checked_in', 'in_progress', 'completed',
            'cancelled', 'no_show', 'rescheduled'
        );
        CREATE TYPE payment_status AS ENUM (
            'pending', 'authorized', 'paid', 'partially_paid', 'refunded',
            'failed', 'cancelled'
        );
        CREATE TYPE payment_method AS ENUM (
            'pix', 'credit_card', 'debit_card', 'cash', 'bank_transfer', 'wallet'
        );
        CREATE TYPE notification_channel AS ENUM (
            'email', 'sms', 'whatsapp', 'push', 'in_app'
        );
        CREATE TYPE notification_status AS ENUM (
            'pending', 'sent', 'delivered', 'read', 'failed', 'cancelled'
        );
        CREATE TYPE waitlist_status AS ENUM (
            'waiting', 'notified', 'accepted', 'expired', 'cancelled'
        );
        CREATE TYPE coupon_type AS ENUM (
            'percentage', 'fixed_amount'
        );
        CREATE TYPE coupon_status AS ENUM (
            'active', 'inactive', 'expired'
        );
        CREATE TYPE recurrence_frequency AS ENUM (
            'daily', 'weekly', 'monthly'
        );
        CREATE TYPE audit_action AS ENUM (
            'insert', 'update', 'delete', 'login', 'logout', 'status_change'
        );
        """
    )


def downgrade() -> None:
    for name in (
        "audit_action",
        "recurrence_frequency",
        "coupon_status",
        "coupon_type",
        "waitlist_status",
        "notification_status",
        "notification_channel",
        "payment_method",
        "payment_status",
        "appointment_status",
        "unit_status",
        "company_status",
        "user_status",
        "user_role",
    ):
        op.execute(f"DROP TYPE IF EXISTS {name}")
