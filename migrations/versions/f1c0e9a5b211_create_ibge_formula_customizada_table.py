"""create ibge formula customizada table

Revision ID: f1c0e9a5b211
Revises: eb00028f8289
Create Date: 2026-05-29 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = 'f1c0e9a5b211'
down_revision = 'eb00028f8289'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ibge_formula_customizada',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('formula', sa.String(length=500), nullable=False),
        sa.Column('ativa', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome'),
    )


def downgrade():
    op.drop_table('ibge_formula_customizada')
