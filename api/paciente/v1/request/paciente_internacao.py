from typing import List
from pydantic import BaseModel, Field

class InternacaoFeature(BaseModel):
    MP10_NORMALIZADO: float = Field(..., example=0.106)
    O3_NORMALIZADO: float = Field(..., example=0.356)
    TEMP_NORMALIZADO: float = Field(..., example=0.625)
    UR_NORMALIZADO: float = Field(..., example=0.649)
    DS_CID_GRAVIDADE: str = Field(..., example="OUTROS TRANSTORNOS RESPIRATORIOS")
    outono: int = Field(..., example=0)
    inverno: int = Field(..., example=0)
    primavera: int = Field(..., example=0)
    verao: int = Field(..., example=1)
    Jan: int = Field(..., example=0)
    Feb: int = Field(..., example=1)
    Mar: int = Field(..., example=0)
    Apr: int = Field(..., example=0)
    May: int = Field(..., example=0)
    Jun: int = Field(..., example=0)
    Jul: int = Field(..., example=0)
    Aug: int = Field(..., example=0)
    Sep: int = Field(..., example=0)
    Oct: int = Field(..., example=0)
    Nov: int = Field(..., example=0)
    Dec: int = Field(..., example=0)
    MENOR_1_ANO: str = Field(..., example="0")
    ENTRE_1_4_ANOS: str = Field(..., example="1")
    ENTRE_5_9_ANOS: str = Field(..., example="0")
    ENTRE_10_14_ANOS: str = Field(..., example="0")
    ENTRE_15_18_ANOS: str = Field(..., example="0")
    TP_SEXO: str = Field(..., example="F")

class PacienteInternacaoData(BaseModel):
    data: List[InternacaoFeature]

class PacienteInternacaoPayload(BaseModel):
    Inputs: PacienteInternacaoData


if __name__ == '__main__':

    json_data = {
        "Inputs": {
            "data": [
                {
                    "MP10_NORMALIZADO": 0.106,
                    "O3_NORMALIZADO": 0.356,
                    "TEMP_NORMALIZADO": 0.625,
                    "UR_NORMALIZADO": 0.649,
                    "DS_CID_GRAVIDADE": "OUTROS TRANSTORNOS RESPIRATORIOS",
                    "outono": 0,
                    "inverno": 0,
                    "primavera": 0,
                    "verao": 1,
                    "Jan": 0,
                    "Feb": 1,
                    "Mar": 0,
                    "Apr": 0,
                    "May": 0,
                    "Jun": 0,
                    "Jul": 0,
                    "Aug": 0,
                    "Sep": 0,
                    "Oct": 0,
                    "Nov": 0,
                    "Dec": 0,
                    "MENOR_1_ANO": "0",
                    "ENTRE_1_4_ANOS": "1",
                    "ENTRE_5_9_ANOS": "0",
                    "ENTRE_10_14_ANOS": "0",
                    "ENTRE_15_18_ANOS": "0",
                    "TP_SEXO": "F"
                }
            ]
        }
    }

    input_payload = PacienteInternacaoPayload(**json_data)
    print(input_payload)
