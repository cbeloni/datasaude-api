from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from aio_pika import Message

class PacienteBase(BaseModel):
    id: Optional[int] = Field(None, example=35717)
    CD_ATENDIMENTO: Optional[int] = Field(None, example=1748614)
    NM_PACIENTE: Optional[str] = Field(None, example="Andrew Hernandez")
    DT_ATENDIMENTO: Optional[date] = Field(None, example="2023-03-31")
    TP_ATENDIMENTO: Optional[str] = Field(None, example="A")
    DS_ORI_ATE: Optional[str] = Field(None, example="CENTRO DE EXCELENCIA")
    DS_LEITO: Optional[str] = Field(None, example="Some example")
    # DT_PREVISTA_ALTA: Optional[date] = Field(None, example="2023-04-01")
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
    endereco: Optional[str] = Field(None, example="AVENIDA BOSQUE DA SAUDE, 426, SAUDE - SP")
    latitude: Optional[str] = Field(None, example="-23.6114721")
    longitude: Optional[str] = Field(None, example="-46.631234")
    poluente: Optional[str] = Field(None, example="MP10")
    indice_interpolado: Optional[str] = Field(None, example="16.392966003938955")

    def to_model(self):
        campos_remover = ['id', 'endereco', 'latitude', 'longitude', 'indice_interpolado', 'poluente']
        return {chave: valor for chave, valor in self.dict().items() if chave not in campos_remover}

    def to_message(self):
        return Message(self.json().encode("utf-8"))


    class Config:
        orm_mode = True

class FiltroParams(BaseModel):
    dt_atendimento_inicial: Optional[str]
    dt_atendimento_final: Optional[str]
    idade_meses: Optional[str]
    idade_anos: Optional[str]

class PacienteListRequest(BaseModel):
        take: int = Field(..., description="quantos registros pegar", example=10)
        prev: Optional[int] = Field(None, description="a partir do registro")
        skip: int = Field(..., description="quantidade de registros para pular")
        columns: list = Field(..., description="colunas da tabela")

class PacientePagination(BaseModel):
    counter: Optional[int] = Field(None, description="Contador de versão")
    totalRecordCount: Optional[int] = Field(None, description="Total de registros")
    filteredRecordCount: Optional[int] = Field(None, description="Total filtrado")
    totalPages: Optional[int] = Field(None, description="Total filtrado")
    currentPage: Optional[int] = Field(None, description="Página atual")
    payload: Optional[List[PacienteBase]] = Field(None, description="Dados dos poluentes")
    aggregationPayload: Optional[List] = Field(None, description="AggregationPayload")


class PacienteTask(PacienteBase):
    ...

    def to_dict(self):
        return {chave: str(valor) for chave, valor in self.dict().items()}

class PacienteCoordenadasTask(BaseModel):
    id: Optional[int] = Field(None, example=35717)

    def to_message(self):
        return Message(self.json().encode("utf-8"))

class PacienteInterpolacaoTask(BaseModel):
    id: Optional[int] = Field(None, example=118)

    def to_message(self):
        return Message(self.json().encode("utf-8"))

class PacienteTaskError(PacienteBase):
    error: Optional[str] = Field(None, description="mensagem de erro ao adicionar na fila")