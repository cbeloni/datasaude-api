from typing import Optional, List

from sqlalchemy import select

from app.poluente.models import Poluente
from app.poluente.repository.poluente_repository import PoluenteRepository
from core.db import session


class PoluenteService:
    def __init__(self):
        ...

    async def get_poluente_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[Poluente]:
        query = select(Poluente)

        if prev:
            query = query.where(Poluente.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    async def get_poluente_by_id(
            self,
            id: int = None
    ) -> Poluente:
        return await PoluenteRepository().get_by_id(id=id)

    async def count(self) -> Poluente:
        return await PoluenteRepository().count()

