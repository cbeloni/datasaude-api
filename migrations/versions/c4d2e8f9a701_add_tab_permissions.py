"""add table and map tab permissions

Revision ID: c4d2e8f9a701
Revises: 8a7f5c2d9e11
"""

from alembic import op
import sqlalchemy as sa


revision = "c4d2e8f9a701"
down_revision = "8a7f5c2d9e11"
branch_labels = None
depends_on = None


PERMISSIONS = [
    ("table.patients.view", "Tabelas / Pacientes"),
    ("table.pollutants.view", "Tabelas / Poluente online"),
    ("table.ibge_v1.view", "Tabelas / IBGE v1"),
    ("table.ibge_v2.view", "Tabelas / IBGE"),
    ("maps.dynamic.view", "Mapas / Mapa dinâmico"),
    ("maps.bronquiolite.view", "Mapas / Bronquiolite"),
    ("maps.static.view", "Mapas / Mapa estático"),
    ("maps.ibge.view", "Mapas / Mapa IBGE"),
    ("maps.ibge_v2.view", "Mapas / Mapa IBGE V2"),
    ("maps.bronquiolite_vsr.view", "Mapas / Bronquiolite VSR"),
]


def upgrade():
    op.bulk_insert(
        sa.table(
            "permissions",
            sa.column("code", sa.Unicode(length=120)),
            sa.column("name", sa.Unicode(length=255)),
        ),
        [{"code": code, "name": name} for code, name in PERMISSIONS],
    )


def downgrade():
    permission_table = sa.table(
        "permissions", sa.column("code", sa.Unicode(length=120))
    )
    op.execute(
        permission_table.delete().where(
            permission_table.c.code.in_([code for code, _ in PERMISSIONS])
        )
    )
