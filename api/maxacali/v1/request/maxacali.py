from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class MaxacaliBase(BaseModel):
    id: Optional[int] = None
    cd_setor: Optional[str] = None
    situacao: Optional[str] = None
    cd_sit: Optional[int] = None
    cd_tipo: Optional[int] = None
    area_km2: Optional[Decimal] = None
    cd_regiao: Optional[int] = None
    nm_regiao: Optional[str] = None
    cd_uf: Optional[int] = None
    nm_uf: Optional[str] = None
    cd_mun: Optional[int] = None
    nm_mun: Optional[str] = None
    cd_dist: Optional[int] = None
    nm_dist: Optional[str] = None
    cd_subdist: Optional[int] = None
    nm_subdist: Optional[str] = None
    cd_bairro: Optional[int] = None
    nm_bairro: Optional[str] = None
    cd_nu: Optional[str] = None
    nm_nu: Optional[str] = None
    cd_fcu: Optional[str] = None
    nm_fcu: Optional[str] = None
    cd_aglom: Optional[str] = None
    nm_aglom: Optional[str] = None
    cd_rgint: Optional[int] = None
    nm_rgint: Optional[str] = None
    cd_rgi: Optional[int] = None
    nm_rgi: Optional[str] = None
    cd_concurb: Optional[str] = None
    nm_concurb: Optional[str] = None
    v0001: Optional[int] = None
    v0002: Optional[int] = None
    v0003: Optional[int] = None
    v0004: Optional[int] = None
    v0005: Optional[Decimal] = None
    v0006: Optional[Decimal] = None
    v0007: Optional[int] = None
    # campos da tabela maxacali_caracteristica (v00001 .. v00089)
    v00001: Optional[str] = None
    v00002: Optional[str] = None
    v00003: Optional[str] = None
    v00004: Optional[str] = None
    v00005: Optional[str] = None
    v00006: Optional[str] = None
    v00007: Optional[str] = None
    v00008: Optional[str] = None
    v00009: Optional[str] = None
    v00010: Optional[str] = None
    v00011: Optional[str] = None
    v00012: Optional[str] = None
    v00013: Optional[str] = None
    v00014: Optional[str] = None
    v00015: Optional[str] = None
    v00016: Optional[str] = None
    v00017: Optional[str] = None
    v00018: Optional[str] = None
    v00019: Optional[str] = None
    v00020: Optional[str] = None
    v00021: Optional[str] = None
    v00022: Optional[str] = None
    v00023: Optional[str] = None
    v00024: Optional[str] = None
    v00025: Optional[str] = None
    v00026: Optional[str] = None
    v00027: Optional[str] = None
    v00028: Optional[str] = None
    v00029: Optional[str] = None
    v00030: Optional[str] = None
    v00031: Optional[str] = None
    v00032: Optional[str] = None
    v00033: Optional[str] = None
    v00034: Optional[str] = None
    v00035: Optional[str] = None
    v00036: Optional[str] = None
    v00037: Optional[str] = None
    v00038: Optional[str] = None
    v00039: Optional[str] = None
    v00040: Optional[str] = None
    v00041: Optional[str] = None
    v00042: Optional[str] = None
    v00043: Optional[str] = None
    v00044: Optional[str] = None
    v00045: Optional[str] = None
    v00046: Optional[str] = None
    v00047: Optional[str] = None
    v00048: Optional[str] = None
    v00049: Optional[str] = None
    v00050: Optional[str] = None
    v00051: Optional[str] = None
    v00052: Optional[str] = None
    v00053: Optional[str] = None
    v00054: Optional[str] = None
    v00055: Optional[str] = None
    v00056: Optional[str] = None
    v00057: Optional[str] = None
    v00058: Optional[str] = None
    v00059: Optional[str] = None
    v00060: Optional[str] = None
    v00061: Optional[str] = None
    v00062: Optional[str] = None
    v00063: Optional[str] = None
    v00064: Optional[str] = None
    v00065: Optional[str] = None
    v00066: Optional[str] = None
    v00067: Optional[str] = None
    v00068: Optional[str] = None
    v00069: Optional[str] = None
    v00070: Optional[str] = None
    v00071: Optional[str] = None
    v00072: Optional[str] = None
    v00073: Optional[str] = None
    v00074: Optional[str] = None
    v00075: Optional[str] = None
    v00076: Optional[str] = None
    v00077: Optional[str] = None
    v00078: Optional[str] = None
    v00079: Optional[str] = None
    v00080: Optional[str] = None
    v00081: Optional[str] = None
    v00082: Optional[str] = None
    v00083: Optional[str] = None
    v00084: Optional[str] = None
    v00085: Optional[str] = None
    v00086: Optional[str] = None
    v00087: Optional[str] = None
    v00088: Optional[str] = None
    v00089: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MaxacaliFiltroParams(BaseModel):
    cd_setor: Optional[str] = Field(None, description="Código do setor")
    situacao: Optional[str] = Field(None, description="Situação")
    nm_uf: Optional[str] = Field(None, description="Nome da UF")
    nm_mun: Optional[str] = Field(None, description="Nome do município")
    nm_bairro: Optional[str] = Field(None, description="Nome do bairro")
    cd_uf: Optional[int] = Field(None, description="Código da UF")
    cd_mun: Optional[int] = Field(None, description="Código do município")
    cd_sit: Optional[int] = Field(None, description="Código da situação")
    cd_tipo: Optional[int] = Field(None, description="Código do tipo")
    cd_regiao: Optional[int] = Field(None, description="Código da região")

    area_km2_min: Optional[Decimal] = Field(None, description="Área mínima")
    area_km2_max: Optional[Decimal] = Field(None, description="Área máxima")
    v0001_min: Optional[int] = Field(None, description="Valor mínimo v0001")
    v0001_max: Optional[int] = Field(None, description="Valor máximo v0001")
    v0002_min: Optional[int] = Field(None, description="Valor mínimo v0002")
    v0002_max: Optional[int] = Field(None, description="Valor máximo v0002")
    v0003_min: Optional[int] = Field(None, description="Valor mínimo v0003")
    v0003_max: Optional[int] = Field(None, description="Valor máximo v0003")
    v0004_min: Optional[int] = Field(None, description="Valor mínimo v0004")
    v0004_max: Optional[int] = Field(None, description="Valor máximo v0004")
    v0005_min: Optional[Decimal] = Field(None, description="Valor mínimo v0005")
    v0005_max: Optional[Decimal] = Field(None, description="Valor máximo v0005")
    v0006_min: Optional[Decimal] = Field(None, description="Valor mínimo v0006")
    v0006_max: Optional[Decimal] = Field(None, description="Valor máximo v0006")
    v0007_min: Optional[int] = Field(None, description="Valor mínimo v0007")
    v0007_max: Optional[int] = Field(None, description="Valor máximo v0007")


class MaxacaliListRequest(BaseModel):
    take: int = Field(..., description="quantos registros pegar", example=10)
    prev: Optional[int] = Field(None, description="a partir do registro")
    skip: int = Field(..., description="quantidade de registros para pular")
    columns: list = Field(default_factory=list, description="colunas da tabela")


class MaxacaliPagination(BaseModel):
    counter: Optional[int] = Field(None, description="Contador de versão")
    totalRecordCount: Optional[int] = Field(None, description="Total de registros")
    filteredRecordCount: Optional[int] = Field(None, description="Total filtrado")
    totalPages: Optional[float] = Field(None, description="Total de páginas")
    currentPage: Optional[int] = Field(None, description="Página atual")
    payload: Optional[List[MaxacaliBase]] = Field(None, description="Dados da maxacali")
