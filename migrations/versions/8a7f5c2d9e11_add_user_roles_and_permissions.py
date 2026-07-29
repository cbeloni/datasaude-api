"""add user roles, permissions and active status

Revision ID: 8a7f5c2d9e11
Revises: f1c0e9a5b211
"""

from datetime import datetime

from alembic import op
import sqlalchemy as sa


revision = "8a7f5c2d9e11"
down_revision = "f1c0e9a5b211"
branch_labels = None
depends_on = None


PERMISSIONS = [
    (1, "dashboard.view", "Dashboard"),
    (2, "previsao.view", "Previsão"),
    (3, "chat_ia.view", "IA Chat"),
    (4, "indicadores.view", "Indicadores"),
    (5, "table.view", "Tabelas"),
    (6, "maps.view", "Mapas"),
    (7, "users.manage", "Gestão de usuários"),
    (8, "roles.manage", "Gestão de perfis"),
]


def upgrade():
    op.create_table(
        "roles",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.Unicode(length=120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "permissions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.Unicode(length=120), nullable=False),
        sa.Column("name", sa.Unicode(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.BigInteger(), nullable=False),
        sa.Column("permission_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column("users", sa.Column("role_id", sa.BigInteger(), nullable=True))
    op.create_foreign_key(
        "fk_users_role_id",
        "users",
        "roles",
        ["role_id"],
        ["id"],
    )

    now = datetime.utcnow()
    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("id", sa.BigInteger()),
            sa.column("name", sa.Unicode()),
            sa.column("is_active", sa.Boolean()),
            sa.column("created_at", sa.DateTime()),
            sa.column("updated_at", sa.DateTime()),
        ),
        [{"id": 1, "name": "Administrador", "is_active": True, "created_at": now, "updated_at": now}],
    )
    op.bulk_insert(
        sa.table(
            "permissions",
            sa.column("id", sa.BigInteger()),
            sa.column("code", sa.Unicode()),
            sa.column("name", sa.Unicode()),
        ),
        [{"id": id_, "code": code, "name": name} for id_, code, name in PERMISSIONS],
    )
    op.bulk_insert(
        sa.table(
            "role_permissions",
            sa.column("role_id", sa.BigInteger()),
            sa.column("permission_id", sa.BigInteger()),
        ),
        [{"role_id": 1, "permission_id": id_} for id_, _, _ in PERMISSIONS],
    )
    op.execute(sa.text("UPDATE users SET role_id = 1, is_active = 1 WHERE is_admin = 1"))


def downgrade():
    op.drop_constraint("fk_users_role_id", "users", type_="foreignkey")
    op.drop_column("users", "role_id")
    op.drop_column("users", "is_active")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
