from app.poluente.models import PoluenteScrap
from core.repository.base import BaseRepo


class PoluenteScrapRepository(BaseRepo):

    def __init__(self):
        super().__init__(PoluenteScrap)
