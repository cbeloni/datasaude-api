from app.poluente.models import Poluente
from core.repository.base import BaseRepo


class PoluenteRepository(BaseRepo):

    def __init__(self):
        super().__init__(Poluente)
