from pydantic import BaseModel, Field

class PacienteRequest(BaseModel):
    dt_atendimento: str = Field(default="2022-01-01", example="2022-01-01")


    def to_dict(self):
        return {
            "dt_atendimento": self.dt_atendimento
        }
