from typing import List

from fastapi import APIRouter, Depends, Query, Path

from api.poluentes.v1.response.poluente import PoluenteBase, PoluentePagination
from app.poluente.services import PoluenteService
from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
)
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)

poluente_router = APIRouter()
_poluenteService = PoluenteService()

class DrawConter:
    def __init__(self):
        self._counter = 0

    @property
    def draw(self):
        self._counter += 1
        return self._counter

_counter = DrawConter()

@poluente_router.get(
    "",
    response_model=PoluentePagination,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_poluente_list(
        length: int = Query(10, description="quantidade de registros que devem retornar"),
        prev: int = Query(None, description="Prev ID"),
        start: int = Query(1, description="Página atual"),
):
    poluentePagination: PoluentePagination = PoluentePagination(
        data=[],
        draw=_counter.draw,
        recordsTotal=1,
        recordsFiltered=1
    )

    poluentePagination.data = await _poluenteService.get_poluente_list(limit=length, prev=prev, start=start)
    poluentePagination.recordsTotal = await _poluenteService.count()
    poluentePagination.recordsFiltered = poluentePagination.recordsTotal

    return poluentePagination


@poluente_router.get(
    "/{id}",
    response_model=PoluenteBase,
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_poluente_by_id(
        limit: int = Query(10, description="Limit"),
        prev: int = Query(None, description="Prev ID"),
        id: int = Path(..., description="ID"),
):
    return await PoluenteService().get_poluente_by_id(id)
