from app.poluente.models import PoluenteScrap
from app.poluente.repository.poluente_scrap_repository import PoluenteScrapRepository

_poluenteScrapRepository = PoluenteScrapRepository()


class PoluenteScrapService:

    def __init__(self):
        ...

    async def get_poluente_scrap_by_id(self, id: int) -> PoluenteScrap:
        return await _poluenteScrapRepository.get_by_id(id=id)

    async def update_poluente_scrap_by_id(self, id: int, params: dict) -> PoluenteScrap:
        await _poluenteScrapRepository.update_by_id(id=id, params=params)
        return await _poluenteScrapRepository.get_by_id(id=id)

    async def delete_poluente_srap_by_id(self, id: int) -> None:
        await _poluenteScrapRepository.delete_by_id(id=id)

    async def save_poluente_scrap(self, poluente_scrap: PoluenteScrap) -> None:
        return await _poluenteScrapRepository.save(poluente_scrap)