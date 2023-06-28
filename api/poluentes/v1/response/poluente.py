from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PoluenteBase(BaseModel):
    id: Optional[int] = Field(None, description="Id do banco")
    data: Optional[str] = Field(None, description="Data coleta do poluente")
    data_atual: Optional[datetime] = Field(None, description="Data inclusão banco")
    endereco: Optional[str] = Field(None, description="endereço da coleta do poluente")
    indice: Optional[int] = Field(None, description="índice poluente")
    municipio: Optional[str] = Field(None, description="municipio da coleta do poluente")
    nome: Optional[str] = Field(None, description="Nome da estação de coleta do poluente")
    poluente: Optional[str] = Field(None, description="Classificação do poluente")
    qualidade: Optional[str] = Field(None, description="Qualidade do ar")
    situacao_rede: Optional[str] = Field(None, description="Situação da estação de coleta")
    tipo_rede: Optional[str] = Field(None, description="Tipo de estação de coleta")

    class Config:
        orm_mode = True

class PoluentePagination(BaseModel):
    Counter: Optional[int] = Field(None, description="Contador de versão")
    TotalRecordCount: Optional[int] = Field(None, description="Total de registros")
    FilteredRecordCount: Optional[int] = Field(None, description="Total filtrado")
    TotalPages: Optional[int] = Field(None, description="Total filtrado")
    CurrentPage: Optional[int] = Field(None, description="Página atual")
    Payload: Optional[List[PoluenteBase]] = Field(None, description="Dados dos poluentes")
    AggregationPayload: Optional[List] = Field(None, description="AggregationPayload")


class PoluenteCreate(PoluenteBase):
    pass


class PoluenteUpdate(PoluenteBase):
    pass


class Poluente(PoluenteBase):
    id: int

class PoluenteRequest(BaseModel):
    take: int = Field(..., description="quantos registros pegar")
    prev: Optional[int] = Field(None, description="a partir do registro")
    skip: int = Field(..., description="quantidade de registros para pular")
    columns: list = Field(..., description="colunas da tabela")
