from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, text

from core.db import Base


class IbgeFormulaCustomizada(Base):
    __tablename__ = 'ibge_formula_customizada'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False, unique=True)
    formula = Column(String(500), nullable=False)
    ativa = Column(Boolean, nullable=False, server_default=text('1'))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP'),
    )
