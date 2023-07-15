"""indice id desc poluente

Revision ID: b6238f4a516b
Revises: 301692715a1a
Create Date: 2023-07-14 22:22:25.719289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6238f4a516b'
down_revision = '301692715a1a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('COMMIT')
    op.create_index('idx_poluente_id_desc', 'poluente', [sa.text('id DESC')], unique=True)

def downgrade():
    op.drop_index('idx_id_desc', table_name='poluente')

