"""payments, payment_items, refunds

Revision ID: 009_payments
Revises: 008_appointments
Create Date: 2026-04-06

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "009_payments"
down_revision: str | None = "008_appointments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

payment_status = postgresql.ENUM(
    "pending",
    "authorized",
    "paid",
    "partially_paid",
    "refunded",
    "failed",
    "cancelled",
    name="payment_status",
    create_type=False,
)

payment_method = postgresql.ENUM(
    "pix",
    "credit_card",
    "debit_card",
    "cash",
    "bank_transfer",
    "wallet",
    name="payment_method",
    create_type=False,
)


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True)),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            payment_status,
            nullable=False,
            server_default=sa.text("'pending'::payment_status"),
        ),
        sa.Column("method", payment_method, nullable=False),
        sa.Column("gateway", sa.String(length=60)),
        sa.Column("gateway_transaction_id", sa.String(length=120)),
        sa.Column("external_reference", sa.String(length=120)),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "paid_amount",
            sa.Numeric(12, 2),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "refunded_amount",
            sa.Numeric(12, 2),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("due_date", sa.DateTime(timezone=True)),
        sa.Column("paid_at", sa.DateTime(timezone=True)),
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
            ["appointment_id"],
            ["appointments.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_payments_appointment_id", "payments", ["appointment_id"])
    op.create_index("ix_payments_customer_id", "payments", ["customer_id"])
    op.create_index(
        "ix_payments_gateway_transaction_id",
        "payments",
        ["gateway_transaction_id"],
    )

    op.create_table(
        "payment_items",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("description", sa.String(length=180), nullable=False),
        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payments.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "refunds",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("gateway_refund_id", sa.String(length=120)),
        sa.Column("refunded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True)),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payments.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )


def downgrade() -> None:
    op.drop_table("refunds")
    op.drop_table("payment_items")
    op.drop_index("ix_payments_gateway_transaction_id", table_name="payments")
    op.drop_index("ix_payments_customer_id", table_name="payments")
    op.drop_index("ix_payments_appointment_id", table_name="payments")
    op.drop_table("payments")
