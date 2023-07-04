from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PoluenteScrapRequest(BaseModel):
    i_rede: str = Field(..., example='A')
    data_inicial: datetime = Field(..., example='2023-07-03 23:28:57')
    data_final: datetime = Field(..., example='2023-07-05 23:28:57')
    i_tipo_dado: str = Field(..., example='P')
    estacao: int = Field(..., example=73, description="Ibirapuera")
    parametro: int = Field(..., example=16, description="Monóxido de carbono")
    file: Optional[str] = Field(None, example='Caminho do arquivo salvo')

    class Config:
        orm_mode = True


if __name__ == '__main__':
    from app.poluente.models.poluente_scrap_model import PoluenteScrap

    p = PoluenteScrapRequest(i_rede='A',
                             data_inicial='2023-07-03 23:28:57',
                             data_final='2023-07-03 23:28:57',
                             i_tipo_dado='P',
                             estacao=73,
                             parametro=16)


    poluenteScrap = PoluenteScrap(**p.dict())
    print(poluenteScrap.dict())