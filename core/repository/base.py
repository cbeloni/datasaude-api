from typing import TypeVar, Type, Optional, Generic

from sqlalchemy import select, update, delete, func

from core.db import Transactional
from core.db.session import Base, session
from core.repository.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await session.execute(query)
        row = result.fetchone()
        return row[0] if row else None

    async def update_by_id(
        self,
        id: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**params)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    async def delete(self, model: ModelType) -> None:
        await session.delete(model)

    async def delete_by_id(
        self,
        id: int,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            delete(self.model)
            .where(self.model.id == id)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    @Transactional()
    async def save(self, model: ModelType) -> None:
        session.add(model)

    async def count(self) -> int:
        query = select(func.count()).select_from(self.model)
        result = await session.execute(query)
        row = result.fetchone()
        return row[0] if row else 0