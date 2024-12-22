"""create documents table

Revision ID: 001
Revises: 
Create Date: 2023-12-22 16:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_name'), 'documents', ['name'], unique=False)
    op.create_index(op.f('idx_date'), 'documents', ['date'], unique=False)

def downgrade():
    op.drop_index(op.f('idx_date'), table_name='documents')
    op.drop_index(op.f('idx_name'), table_name='documents')
    op.drop_table('documents') 