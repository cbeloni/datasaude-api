from typing import Optional
from pydantic import BaseModel, Field

class PacienteRequest(BaseModel):
    dt_atendimento: str = Field(default="2022-01-01", example="2022-01-01")
    poluente: str = Field(default="MP10", example="MP10")
    ds_cid: Optional[str] = Field(default=None, example="BRONQUIOLITE AGUDA, INFECCAO AGUDA DAS VIAS AEREAS SUPERIORES NAO ESPECIFICADA")


    def to_dict(self):
        return {
            "dt_atendimento": self.dt_atendimento,
            "poluente": self.poluente,
            "ds_cid": self.ds_cid
        }
