from sqlalchemy import Column, Unicode, BigInteger, DateTime, Integer

from core.db import Base
from core.db.mixins import TimestampMixin


class PoluenteScrap(Base, TimestampMixin):
    __tablename__ = "poluente_scrap"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    i_rede = Column(Unicode(50))
    data_inicial = Column(DateTime)
    data_final = Column(DateTime)
    i_tipo_dado = Column(Unicode(2))
    estacao = Column(Integer)
    parametro = Column(Integer)
    file = Column(Unicode(50))

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
