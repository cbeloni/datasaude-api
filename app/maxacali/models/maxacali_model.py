from sqlalchemy import Column, BigInteger, Integer, String, Numeric, SmallInteger, TIMESTAMP, text

from core.db import Base


class Maxacali(Base):
    __tablename__ = "maxacali"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cd_setor = Column(String(100), nullable=False)
    situacao = Column(String(20), nullable=True)
    cd_sit = Column(Integer, nullable=True)
    cd_tipo = Column(Integer, nullable=True)
    area_km2 = Column(Numeric(12, 7), nullable=True)
    cd_regiao = Column(Integer, nullable=True)
    nm_regiao = Column(String(50), nullable=True)
    cd_uf = Column(SmallInteger, nullable=True)
    nm_uf = Column(String(100), nullable=True)
    cd_mun = Column(Integer, nullable=True)
    nm_mun = Column(String(150), nullable=True)
    cd_dist = Column(BigInteger, nullable=True)
    nm_dist = Column(String(150), nullable=True)
    cd_subdist = Column(BigInteger, nullable=True)
    nm_subdist = Column(String(150), nullable=True)
    cd_bairro = Column(BigInteger, nullable=True)
    nm_bairro = Column(String(150), nullable=True)
    cd_nu = Column(String(30), nullable=True)
    nm_nu = Column(String(150), nullable=True)
    cd_fcu = Column(String(30), nullable=True)
    nm_fcu = Column(String(150), nullable=True)
    cd_aglom = Column(String(30), nullable=True)
    nm_aglom = Column(String(150), nullable=True)
    cd_rgint = Column(Integer, nullable=True)
    nm_rgint = Column(String(150), nullable=True)
    cd_rgi = Column(Integer, nullable=True)
    nm_rgi = Column(String(150), nullable=True)
    cd_concurb = Column(String(30), nullable=True)
    nm_concurb = Column(String(150), nullable=True)
    v0001 = Column(Integer, nullable=True)
    v0002 = Column(Integer, nullable=True)
    v0003 = Column(Integer, nullable=True)
    v0004 = Column(Integer, nullable=True)
    v0005 = Column(Numeric(6, 2), nullable=True)
    v0006 = Column(Numeric(12, 4), nullable=True)
    v0007 = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )
