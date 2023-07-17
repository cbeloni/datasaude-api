"""indice poluente nome  e data

Revision ID: eb00028f8289
Revises: b6238f4a516b
Create Date: 2023-07-16 23:09:30.062848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb00028f8289'
down_revision = 'b6238f4a516b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('COMMIT')
    op.create_index('idx_poluente_nome_data', 'poluente', [sa.text('data', 'nome')], unique=True)


def downgrade():
    op.drop_index('idx_poluente_nome_data', table_name='poluente')
