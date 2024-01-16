from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

class PacienteBase(BaseModel):
    id: int = Field(None, example=35717)
    CD_ATENDIMENTO: Optional[int] = Field(None, example=1748614)
    NM_PACIENTE: Optional[str] = Field(None, example="Andrew Hernandez")
    DT_ATENDIMENTO: Optional[date] = Field(None, example="2023-03-31")
    TP_ATENDIMENTO: Optional[str] = Field(None, example="A")
    DS_ORI_ATE: Optional[str] = Field(None, example="CENTRO DE EXCELENCIA")
    DS_LEITO: Optional[str] = Field(None, example="Some example")
    DT_PREVISTA_ALTA: Optional[date] = Field(None, example="2023-04-01")
    DT_ALTA: Optional[date] = Field(None, example="2023-03-31")
    CD_SGRU_CID: Optional[str] = Field(None, example="J85")
    CD_CID: Optional[str] = Field(None, example="J851")
    DS_CID: Optional[str] = Field(None, example="ABSCESSO DO PULMAO COM PNEUMONIA")
    SN_INTERNADO: Optional[str] = Field(None, example="N")
    DS_ENDERECO: Optional[str] = Field(None, example="RUA BENTO BRANCO DE ANDRADE FILHO")
    NR_ENDERECO: Optional[int] = Field(None, example=495)
    NM_BAIRRO: Optional[str] = Field(None, example="JARDIM DOM BOSCO")
    NR_CEP: Optional[int] = Field(None, example=4757000)
    DT_NASC: Optional[date] = Field(None, example="2014-03-11")
    IDADE: Optional[str] = Field(None, example="9a 0m 19d")
    TP_SEXO: Optional[str] = Field(None, example="F")

    class Config:
        orm_mode = True

class PacientePagination(BaseModel):
    Counter: Optional[int] = Field(None, description="Contador de versão")
    TotalRecordCount: Optional[int] = Field(None, description="Total de registros")
    FilteredRecordCount: Optional[int] = Field(None, description="Total filtrado")
    TotalPages: Optional[int] = Field(None, description="Total filtrado")
    CurrentPage: Optional[int] = Field(None, description="Página atual")
    Payload: Optional[List[PacienteBase]] = Field(None, description="Dados dos poluentes")
    AggregationPayload: Optional[List] = Field(None, description="AggregationPayload")