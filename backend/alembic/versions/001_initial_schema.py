"""Initial schema

Revision ID: 001
Create Date: 2024-12-23
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create generated_documents table
    op.create_table(
        'generated_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('template_type', sa.String(), nullable=True),
        sa.Column('doc_id', sa.String(), nullable=True),
        sa.Column('doc_url', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create document_versions table
    op.create_table(
        'document_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), sa.ForeignKey('generated_documents.id'), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_document_versions_document_id', 'document_versions', ['document_id'])

def downgrade():
    op.drop_index('ix_document_versions_document_id')
    op.drop_table('document_versions')
    op.drop_table('generated_documents') 