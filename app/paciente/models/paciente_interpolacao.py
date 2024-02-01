from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PacienteInterpolacao(Base):
    __tablename__ = 'paciente_interpolacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_coordenada = Column(Integer, nullable=False)
    data = Column(String(50), nullable=True)
    poluente = Column(String(50), nullable=True)
    indice_interpolado = Column(String(100), nullable=True)
    data_criacao = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True)
