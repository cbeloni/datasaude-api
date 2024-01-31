from sqlalchemy import Column, Integer, String, Date, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base

class Paciente(Base):
    __tablename__ = 'paciente'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    CD_ATENDIMENTO = Column(Integer)
    NM_PACIENTE = Column(String)
    DT_ATENDIMENTO = Column(Date)
    TP_ATENDIMENTO = Column(String)
    DS_ORI_ATE = Column(String)
    DS_LEITO = Column(String, nullable=True)
    # DT_PREVISTA_ALTA = Column(String, nullable=True)
    DT_ALTA = Column(String)
    CD_SGRU_CID = Column(String)
    CD_CID = Column(String)
    DS_CID = Column(String)
    SN_INTERNADO = Column(String)
    DS_ENDERECO = Column(String)
    NR_ENDERECO = Column(Integer)
    NM_BAIRRO = Column(String)
    NR_CEP = Column(Integer)
    DT_NASC = Column(String)
    IDADE = Column(String)
    TP_SEXO = Column(String)