from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text

from core.db import Base


class IbgePessoas(Base):
    __tablename__ = "ibge_pessoas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cd_setor = Column(String(100), nullable=False)
    v01690 = Column(String(10), nullable=True)
    v01691 = Column(String(10), nullable=True)
    v01692 = Column(String(10), nullable=True)
    v01693 = Column(String(10), nullable=True)
    v01694 = Column(String(10), nullable=True)
    v01695 = Column(String(10), nullable=True)
    v01696 = Column(String(10), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )
