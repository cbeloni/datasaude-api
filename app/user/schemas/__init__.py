from pydantic import BaseModel

from .user import *
from .admin import *


class ExceptionResponseSchema(BaseModel):
    error: str


__all__ = [
    *[name for name in globals() if name.endswith("Schema")],
    "ExceptionResponseSchema",
]
