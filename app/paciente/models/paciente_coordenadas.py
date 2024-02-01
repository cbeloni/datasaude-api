from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PacienteCoordenadas(Base):
    __tablename__ = 'paciente_coordenadas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_paciente = Column(Integer, nullable=False)
    endereco = Column(String(300), nullable=True)
    latitude = Column(String(100), nullable=True)
    longitude = Column(String(100), nullable=True)
    x = Column(String(100), nullable=True)
    y = Column(String(100), nullable=True)
    acuracia = Column(String(20), nullable=True)
    provider = Column(String(50), nullable=True)
    postcode = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    county = Column(String(100), nullable=True)
    quarter = Column(String(50), nullable=True)
    suburb = Column(String(100), nullable=True)
    formatted = Column(String(200), nullable=True)
    response = Column(Text, nullable=True)
    validado = Column(Boolean, default=False, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    data_alteracao = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
