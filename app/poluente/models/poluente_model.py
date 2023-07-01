from sqlalchemy import Column, Unicode, BigInteger, DateTime, Integer

from core.db import Base
from core.db.mixins import TimestampMixin


class Poluente(Base, TimestampMixin):
    __tablename__ = "poluente"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    data = Column(Unicode(255))
    data_atual = Column(DateTime)
    endereco = Column(Unicode(255))
    indice = Column(Integer)
    municipio = Column(Unicode(50))
    nome = Column(Unicode(50))
    poluente = Column(Unicode(50))
    qualidade = Column(Unicode(50))
    situacao_rede = Column(Unicode(50))
    tipo_rede = Column(Unicode(50))
