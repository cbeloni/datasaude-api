from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, Unicode

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=True)


class Role(Base, TimestampMixin):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(120), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(Unicode(120), nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(
        BigInteger,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id = Column(
        BigInteger,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )
