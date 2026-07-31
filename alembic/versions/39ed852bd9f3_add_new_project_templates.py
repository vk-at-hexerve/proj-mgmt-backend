"""add_new_project_templates

Revision ID: 39ed852bd9f3
Revises: 1b2e7278edc1
Create Date: 2026-07-27 23:58:15.351525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39ed852bd9f3'
down_revision: Union[str, Sequence[str], None] = '1b2e7278edc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# The 6 new template IDs being added
NEW_TEMPLATE_IDS = [
    'tpl-opportunity',
    'tpl-finance',
    'tpl-onboarding',
    'tpl-managed-service',
    'tpl-ai-agent',
    'tpl-customer-health',
]


def upgrade() -> None:
    """Seed statuses for 6 new project templates. INSERT-only — no existing data is touched."""
    import uuid
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)

    template_statuses_table = sa.table('template_statuses',
        sa.column('id', sa.String),
        sa.column('template_id', sa.String),
        sa.column('name', sa.String),
        sa.column('group_key', sa.String),
        sa.column('color', sa.String),
        sa.column('position', sa.Integer),
        sa.column('is_default', sa.Boolean),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )

    def row(tid, name, group, color, pos, default=False):
        return {
            "id": str(uuid.uuid4()), "template_id": tid,
            "name": name, "group_key": group, "color": color,
            "position": pos, "is_default": default,
            "created_at": now, "updated_at": now,
        }

    all_statuses = [
        # ── Opportunity / Deal ────────────────────────────────────
        row("tpl-opportunity", "Discovery",          "OPEN",        "#94A3B8", 0, True),
        row("tpl-opportunity", "Solution Proposed",   "OPEN",        "#3B82F6", 1),
        row("tpl-opportunity", "Proposal Sent",       "IN_PROGRESS", "#FBBF24", 0),
        row("tpl-opportunity", "Negotiation",         "IN_PROGRESS", "#F59E0B", 1),
        row("tpl-opportunity", "Awaiting Decision",   "IN_PROGRESS", "#8B5CF6", 2),
        row("tpl-opportunity", "Proposal Approved",   "IN_PROGRESS", "#10B981", 3),
        row("tpl-opportunity", "Contract Sent",       "IN_PROGRESS", "#6366F1", 4),
        row("tpl-opportunity", "Contract Signed",     "IN_PROGRESS", "#D946EF", 5),
        row("tpl-opportunity", "On Hold",             "ON_HOLD",     "#F59E0B", 0),
        row("tpl-opportunity", "Won",                 "CLOSED",      "#22C55E", 0),
        row("tpl-opportunity", "Lost",                "CLOSED",      "#EF4444", 1),

        # ── Finance ───────────────────────────────────────────────
        row("tpl-finance", "Invoice Pending",         "OPEN",        "#94A3B8", 0, True),
        row("tpl-finance", "Invoice Sent",            "IN_PROGRESS", "#3B82F6", 0),
        row("tpl-finance", "Partially Received",      "IN_PROGRESS", "#FBBF24", 1),
        row("tpl-finance", "Payment Received",        "CLOSED",      "#22C55E", 0),
        row("tpl-finance", "Subscription Created",    "OPEN",        "#8B5CF6", 1),
        row("tpl-finance", "Subscription Active",     "IN_PROGRESS", "#10B981", 2),
        row("tpl-finance", "Subscription Paused",     "ON_HOLD",     "#F59E0B", 0),
        row("tpl-finance", "Subscription Cancelled",  "CLOSED",      "#EF4444", 1),
        row("tpl-finance", "Refund Issued",           "CLOSED",      "#F43F5E", 2),

        # ── Customer Onboarding ───────────────────────────────────
        row("tpl-onboarding", "Welcome Sent",         "OPEN",        "#94A3B8", 0, True),
        row("tpl-onboarding", "Kickoff Scheduled",    "OPEN",        "#3B82F6", 1),
        row("tpl-onboarding", "Kickoff Completed",    "IN_PROGRESS", "#10B981", 0),
        row("tpl-onboarding", "Documents Pending",    "ON_HOLD",     "#FBBF24", 0),
        row("tpl-onboarding", "Access Pending",       "ON_HOLD",     "#F59E0B", 1),
        row("tpl-onboarding", "Integrations In Progress", "IN_PROGRESS", "#8B5CF6", 1),
        row("tpl-onboarding", "Training Scheduled",   "IN_PROGRESS", "#6366F1", 2),
        row("tpl-onboarding", "Onboarding Complete",  "CLOSED",      "#22C55E", 0),

        # ── Managed Service / BAU ─────────────────────────────────
        row("tpl-managed-service", "Active",               "OPEN",        "#10B981", 0, True),
        row("tpl-managed-service", "Work In Progress",     "IN_PROGRESS", "#3B82F6", 0),
        row("tpl-managed-service", "Awaiting Client Input","ON_HOLD",     "#FBBF24", 0),
        row("tpl-managed-service", "Completed This Cycle", "CLOSED",      "#22C55E", 0),
        row("tpl-managed-service", "Renewing",             "IN_PROGRESS", "#8B5CF6", 1),
        row("tpl-managed-service", "Suspended",            "ON_HOLD",     "#F59E0B", 1),
        row("tpl-managed-service", "Cancelled",            "CLOSED",      "#EF4444", 1),

        # ── AI Agent ──────────────────────────────────────────────
        row("tpl-ai-agent", "AI Working",             "IN_PROGRESS", "#3B82F6", 0, True),
        row("tpl-ai-agent", "Waiting for Human",      "ON_HOLD",     "#FBBF24", 0),
        row("tpl-ai-agent", "Waiting for Customer",   "ON_HOLD",     "#F59E0B", 1),
        row("tpl-ai-agent", "Automation Complete",     "CLOSED",      "#22C55E", 0),
        row("tpl-ai-agent", "Exception Detected",      "ON_HOLD",     "#EF4444", 2),
        row("tpl-ai-agent", "Manual Override",         "IN_PROGRESS", "#8B5CF6", 1),
        row("tpl-ai-agent", "Escalated to Human",      "IN_PROGRESS", "#F43F5E", 2),

        # ── Customer Health ───────────────────────────────────────
        row("tpl-customer-health", "Healthy",          "OPEN",        "#22C55E", 0, True),
        row("tpl-customer-health", "Needs Attention",  "IN_PROGRESS", "#FBBF24", 0),
        row("tpl-customer-health", "At Risk",          "ON_HOLD",     "#F59E0B", 0),
        row("tpl-customer-health", "Escalated",        "IN_PROGRESS", "#EF4444", 1),
        row("tpl-customer-health", "Churn Risk",       "ON_HOLD",     "#F43F5E", 1),
        row("tpl-customer-health", "Churned",          "CLOSED",      "#6B7280", 0),
    ]

    op.bulk_insert(template_statuses_table, all_statuses)


def downgrade() -> None:
    """Remove only the statuses added by this migration."""
    ids = "', '".join(NEW_TEMPLATE_IDS)
    op.execute(f"DELETE FROM template_statuses WHERE template_id IN ('{ids}')")

