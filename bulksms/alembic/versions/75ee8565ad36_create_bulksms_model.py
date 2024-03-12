"""create_bulksms_model

Revision ID: 75ee8565ad36
Revises: None
Create Date: 2023-06-04 22:31:10.817827

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid

# revision identifiers, used by Alembic.
revision = '75ee8565ad36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'bulksms',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, index=True, default=str(uuid.uuid4)),
        sa.Column('name', sa.String(length=30)),
        sa.Column('workspace_id', UUID(as_uuid=False), nullable=False),
        sa.Column('status', sa.String(length=10)),
        sa.Column('message', sa.Text()),
        sa.Column('contact_count', sa.Integer(), default=0),
        sa.Column('total_cost', sa.Float(), default=0),
        sa.Column("all_contacts", JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('modified_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bulksms_info',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, index=True, default=str(uuid.uuid4)),
        sa.Column('bulksms_id',UUID(as_uuid=False), nullable=False),
        sa.Column('sms_status', sa.String(length=10)),
        sa.Column('contact_number', sa.String(length=15)),
        sa.Column('contact_name', sa.String(length=30)),
        sa.Column('sms_cost', sa.Float(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('modified_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(["bulksms_id"], ["bulksms.id"]),
    )


def downgrade() -> None:
    op.drop_table('bulksms')
    op.drop_table('bulksms_info')
