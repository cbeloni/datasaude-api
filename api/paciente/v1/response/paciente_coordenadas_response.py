from pydantic.main import BaseModel


class CoordenadasResponse(BaseModel):
    latitude: str
    longitude: str
    acuracia: str
    x: str
    y: str
    response: str