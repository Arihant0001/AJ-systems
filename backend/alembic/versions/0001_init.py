"""init

Revision ID: 0001_init
Revises: 
Create Date: 2026-01-13

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "persons",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("owner_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_persons_owner_id", "persons", ["owner_id"], unique=False)

    op.create_table(
        "tiffin_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("owner_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("person_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("persons.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("action", sa.Enum("GIVEN", "REVERSED", name="tiffin_action"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("person_id", "date", "action", name="uq_tiffin_person_date_action"),
    )
    op.create_index("ix_tiffin_logs_owner_id", "tiffin_logs", ["owner_id"], unique=False)
    op.create_index("ix_tiffin_logs_person_id", "tiffin_logs", ["person_id"], unique=False)
    op.create_index("ix_tiffin_logs_date", "tiffin_logs", ["date"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_tiffin_logs_date", table_name="tiffin_logs")
    op.drop_index("ix_tiffin_logs_person_id", table_name="tiffin_logs")
    op.drop_index("ix_tiffin_logs_owner_id", table_name="tiffin_logs")
    op.drop_table("tiffin_logs")

    op.drop_index("ix_persons_owner_id", table_name="persons")
    op.drop_table("persons")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    op.execute("DROP TYPE IF EXISTS tiffin_action")
