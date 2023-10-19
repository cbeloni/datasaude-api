
from pydantic import BaseModel
from pydantic.fields import Field

class PacienteCoordenadas(BaseModel):
    id_paciente: int
    endereco: str
    latitude: str = Field(default="")
    longitude: str = Field(default="")
    x: str = Field(default="")
    y: str = Field(default="")
    acuracia: str = Field(default="")
    provider: str = Field(default="")
    postcode: str = Field(default="")
    city: str = Field(default="")
    state: str = Field(default="")
    country: str = Field(default="")
    county: str = Field(default="")
    quarter: str = Field(default="")
    suburb: str = Field(default="")
    formatted: str = Field(default="")
    response: str = Field(default="")
    validado: int = Field(default="0")
