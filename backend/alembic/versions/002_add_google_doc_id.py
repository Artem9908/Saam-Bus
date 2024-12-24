"""Add google_doc_id column

Revision ID: 002
Create Date: 2024-12-23
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Get inspector to check existing columns
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('generated_documents')]
    
    # Only add the column if it doesn't exist
    if 'google_doc_id' not in columns:
        op.add_column('generated_documents', sa.Column('google_doc_id', sa.String(), nullable=True))

def downgrade():
    op.drop_column('generated_documents', 'google_doc_id')