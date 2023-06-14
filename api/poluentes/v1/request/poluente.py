from datetime import datetime
from pydantic import BaseModel, Field


class PoluenteBase(BaseModel):
    data: str = Field(..., description="Data coleta do poluente")
    data_atual: datetime = Field(..., description="Data inclusão banco")
    endereco: str = Field(..., description="endereço da coleta do poluente")
    indice: int = Field(..., description="índice poluente")
    municipio: str = Field(..., description="municipio da coleta do poluente")
    nome: str = Field(..., description="Nome da estação de coleta do poluente")
    poluente: str = Field(..., description="Classificação do poluente")
    qualidade: str = Field(..., description="Qualidade do ar")
    situacao_rede: str = Field(..., description="Situação da estação de coleta")
    tipo_rede: str = Field(..., description="Tipo de estação de coleta")

    class Config:
        orm_mode = True


class PoluenteCreate(PoluenteBase):
    pass


class PoluenteUpdate(PoluenteBase):
    pass


class Poluente(PoluenteBase):
    id: int
