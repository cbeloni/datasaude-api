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
    draw: int = Field(..., description="Página atual")
    recordsTotal: int = Field(..., description="Total de registros")
    recordsFiltered: int = Field(..., description="Total filtrado")
    data: List[PoluenteBase] = Field(..., description="Dados dos poluentes")

class PoluenteCreate(PoluenteBase):
    pass


class PoluenteUpdate(PoluenteBase):
    pass


class Poluente(PoluenteBase):
    id: int
