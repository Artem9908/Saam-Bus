"""add doc fields

Revision ID: 002
Revises: 001
Create Date: 2023-12-22 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('documents', sa.Column('doc_url', sa.String(), nullable=True))
    op.add_column('documents', sa.Column('doc_id', sa.String(), nullable=True))

def downgrade():
    op.drop_column('documents', 'doc_url')
    op.drop_column('documents', 'doc_id') 