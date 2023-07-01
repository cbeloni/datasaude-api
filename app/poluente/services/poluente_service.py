from typing import Optional, List

from sqlalchemy import select, desc, asc

from api.poluentes.v1.request.poluente import PoluenteBase
from app.poluente.models import Poluente
from app.poluente.repository.poluente_repository import PoluenteRepository
from core.db import session


class PoluenteService:
    def __init__(self):
        ...

    async def get_poluente_list(
        self,
        limit: int = None,
        prev: Optional[int] = None,
        start: int = 0
    ) -> List[Poluente]:
        query = select(Poluente)

        if prev:
            query = query.where(Poluente.id < prev)

        if limit > 1000:
            limit = 1000

        query = query.offset(start).limit(limit).order_by(desc(Poluente.id))

        return (await session.execute(query)).scalars().all()
    async def get_poluente_by_id(
            self,
            id: int = None
    ) -> Poluente:
        return await PoluenteRepository().get_by_id(id=id)

    async def count(self) -> Poluente:
        return await PoluenteRepository().count()

    async def save(self, poluente: Poluente) -> None:
        await PoluenteRepository().save(poluente)
