from pydantic import BaseModel, Field, validator


class PacienteCoordenadasLote(BaseModel):
    provider: str = Field(..., example="openstretmap")
    limit: int = Field(..., example=2500)

    @validator("limit")
    def validate_limit(cls, limit):
        if limit < 0:
            raise ValueError("O valor do limite deve ser maior ou igual a zero")
        return limit

    def to_dict(self):
        return {
            "provider": self.provider,
            "limit": self.limit
        }