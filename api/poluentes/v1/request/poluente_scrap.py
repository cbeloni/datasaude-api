from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.main import Optional


class PoluenteScrapRequest(BaseModel):
    i_rede: str = Field(..., example='A')
    data_inicial: datetime = Field(..., example='01/03/2023')
    data_final: datetime = Field(..., example='05/03/2023')
    i_tipo_dado: str = Field(..., example='P')
    estacao: int = Field(..., example=73, description="Ibirapuera")
    parametro: int = Field(..., example=16, description="Monóxido de carbono")
    file: Optional(str) = Field(None, example='Caminho do arquivo salvo')

    class Config:
        orm_mode = True


