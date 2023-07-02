from fastapi import APIRouter, Depends, Query, Path, Response

from api.poluentes.v1.response.poluente import PoluenteBase, PoluentePagination, PoluenteRequest
from app.poluente.integrations import cetesb
from app.poluente.models import Poluente
from app.poluente.services import PoluenteService
from app.user.schemas import (
    ExceptionResponseSchema,
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
        Counter=_counter.draw,
    )

    poluentePagination.Payload = await _poluenteService.get_poluente_list(limit=length,
                                                                          prev=prev,
                                                                          start=start)
    poluentePagination.TotalRecordCount = await _poluenteService.count()
    poluentePagination.FilteredRecordCount = poluentePagination.TotalRecordCount
    poluentePagination.TotalPages = poluentePagination.TotalRecordCount / length
    poluentePagination.CurrentPage = (start // length) + 1

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
    return await _poluenteService.get_poluente_by_id(id)


@poluente_router.put(
    "/cetesb",
    response_model=PoluentePagination,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_poluente_cetesb(persist: bool = Query(False, description="true para gravar o resultado na base")):
    poluentePagination: PoluentePagination = PoluentePagination(
        Counter=_counter.draw,
    )

    poluentePagination.Payload = await cetesb.execute_get_capa(persist)
    poluentePagination.TotalRecordCount = len(poluentePagination.Payload)
    poluentePagination.FilteredRecordCount = poluentePagination.TotalRecordCount
    poluentePagination.TotalPages = 1
    poluentePagination.CurrentPage = 1

    return poluentePagination

@poluente_router.post(
    "",
    response_model=PoluentePagination,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def post_poluente_list(payload: PoluenteRequest):
    poluentePagination: PoluentePagination = PoluentePagination(
        Counter=_counter.draw
    )

    poluentePagination.Payload = await _poluenteService.get_poluente_list(limit=payload.take,
                                                                          prev=payload.prev,
                                                                          start=payload.skip)
    poluentePagination.TotalRecordCount = await _poluenteService.count()
    poluentePagination.FilteredRecordCount = poluentePagination.TotalRecordCount
    poluentePagination.TotalPages = poluentePagination.TotalRecordCount / payload.take
    poluentePagination.CurrentPage = (payload.skip // payload.take) + 1

    return poluentePagination

@poluente_router.post(
    "/salvar",
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def save_poluente(poluenteBase: PoluenteBase):
    poluente: Poluente = Poluente(**poluenteBase.dict())
    await _poluenteService.save(poluente)
    return Response(status_code=201)
