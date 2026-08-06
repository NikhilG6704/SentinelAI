"""create recovery workflows table

Revision ID: d0b5ac91c0c6
Revises: d52ccd621ca8
Create Date: 2026-08-05 18:36:30.455313

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d0b5ac91c0c6"
down_revision: Union[str, Sequence[str], None] = "d52ccd621ca8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "recovery_workflows",
        sa.Column("workflow_name", sa.String(length=255), nullable=False),
        sa.Column("automation_rule_id", sa.Integer(), nullable=False),
        sa.Column("incident_id", sa.Integer(), nullable=True),
        sa.Column("infrastructure_asset_id", sa.Integer(), nullable=False),
        sa.Column(
            "action_type",
            sa.Enum(
                "RESTART_SERVICE",
                "RESTART_CONTAINER",
                "RESTART_VM",
                "REBOOT_SERVER",
                "CLEAR_CACHE",
                "RESTART_MONITORING_AGENT",
                "SEND_NOTIFICATION",
                name="recovery_action_type_enum",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "execution_mode",
            sa.Enum(
                "SIMULATION",
                name="execution_mode_enum",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "execution_status",
            sa.Enum(
                "PENDING",
                "RUNNING",
                "COMPLETED",
                "FAILED",
                "CANCELLED",
                name="execution_status_enum",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("execution_log", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("executed_by", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.ForeignKeyConstraint(
            ["automation_rule_id"],
            ["automation_rules.id"],
        ),
        sa.ForeignKeyConstraint(
            ["incident_id"],
            ["incidents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["infrastructure_asset_id"],
            ["infrastructure_assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_recovery_workflows_automation_rule_id"),
        "recovery_workflows",
        ["automation_rule_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_recovery_workflows_id"),
        "recovery_workflows",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_recovery_workflows_incident_id"),
        "recovery_workflows",
        ["incident_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_recovery_workflows_infrastructure_asset_id"),
        "recovery_workflows",
        ["infrastructure_asset_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_recovery_workflows_infrastructure_asset_id"),
        table_name="recovery_workflows",
    )

    op.drop_index(
        op.f("ix_recovery_workflows_incident_id"),
        table_name="recovery_workflows",
    )

    op.drop_index(
        op.f("ix_recovery_workflows_id"),
        table_name="recovery_workflows",
    )

    op.drop_index(
        op.f("ix_recovery_workflows_automation_rule_id"),
        table_name="recovery_workflows",
    )

    op.drop_table("recovery_workflows")