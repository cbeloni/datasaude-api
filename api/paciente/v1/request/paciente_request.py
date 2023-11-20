from pydantic import BaseModel, Field

class PacienteRequest(BaseModel):
    dt_atendimento: str = Field(default="2022-01-01", example="2022-01-01")
    poluente: str = Field(default="MP10", example="MP10")


    def to_dict(self):
        return {
            "dt_atendimento": self.dt_atendimento,
            "poluente": self.poluente
        }
