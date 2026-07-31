"""update_lead_tracking_statuses

Revision ID: 1b2e7278edc1
Revises: 0b3b60eff1e1
Create Date: 2026-07-27 23:47:57.997758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b2e7278edc1'
down_revision: Union[str, Sequence[str], None] = '0b3b60eff1e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    import uuid
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    
    # Soft-delete old tpl-lead statuses to preserve existing foreign keys
    op.execute("UPDATE template_statuses SET deleted_at = CURRENT_TIMESTAMP WHERE template_id = 'tpl-lead' AND deleted_at IS NULL")
    
    # Insert new lead statuses
    template_statuses_table = sa.table('template_statuses',
        sa.column('id', sa.String),
        sa.column('template_id', sa.String),
        sa.column('name', sa.String),
        sa.column('group_key', sa.String),
        sa.column('color', sa.String),
        sa.column('position', sa.Integer),
        sa.column('is_default', sa.Boolean),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime)
    )
    
    lead_statuses = [
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "New Lead", "group_key": "OPEN", "color": "#94A3B8", "position": 0, "is_default": True, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "AI Engagement Started", "group_key": "OPEN", "color": "#3B82F6", "position": 1, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Attempted Contact", "group_key": "IN_PROGRESS", "color": "#FBBF24", "position": 0, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Connected", "group_key": "IN_PROGRESS", "color": "#10B981", "position": 1, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Qualified", "group_key": "IN_PROGRESS", "color": "#8B5CF6", "position": 2, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Demo Scheduled", "group_key": "IN_PROGRESS", "color": "#D946EF", "position": 3, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Demo Completed", "group_key": "IN_PROGRESS", "color": "#6366F1", "position": 4, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Nurturing", "group_key": "ON_HOLD", "color": "#F59E0B", "position": 0, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Unqualified", "group_key": "CLOSED", "color": "#6B7280", "position": 0, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Lost", "group_key": "CLOSED", "color": "#EF4444", "position": 1, "is_default": False, "created_at": now, "updated_at": now},
        {"id": str(uuid.uuid4()), "template_id": "tpl-lead", "name": "Converted to Opportunity", "group_key": "CLOSED", "color": "#22C55E", "position": 2, "is_default": False, "created_at": now, "updated_at": now},
    ]
    
    op.bulk_insert(template_statuses_table, lead_statuses)


def downgrade() -> None:
    """Downgrade schema."""
    # Delete the newly inserted statuses
    op.execute("DELETE FROM template_statuses WHERE template_id = 'tpl-lead' AND deleted_at IS NULL")
    
    # Restore the soft-deleted old statuses
    op.execute("UPDATE template_statuses SET deleted_at = NULL WHERE template_id = 'tpl-lead' AND deleted_at IS NOT NULL")
