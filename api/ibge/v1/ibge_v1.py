from fastapi import APIRouter, Depends

from api.ibge.v1.request.ibge import IbgeFiltroParams, IbgeListRequest, IbgePagination
from app.ibge.services.ibge_service import ibge_list
from app.user.schemas import ExceptionResponseSchema
from core.utils.counter import DrawConter
from core.utils.logger import LoggerUtils

log = LoggerUtils(__name__)

ibge_router = APIRouter()
_counter = DrawConter()


@ibge_router.post(
    "/listar",
    response_model=IbgePagination,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def post_ibge_list(
    filtro: IbgeFiltroParams = Depends(),
    payload: IbgeListRequest = None,
):
    log.info(f"Obtendo ibge list {payload}")

    ibge_pagination: IbgePagination = IbgePagination(
        counter=_counter.draw,
    )

    if payload is None:
        payload = IbgeListRequest(take=10, prev=None, skip=0, columns=[])

    ibge_pagination.payload, ibge_pagination.totalRecordCount = await ibge_list(
        limit=payload.take,
        prev=payload.prev,
        start=payload.skip,
        filtro=filtro,
    )

    ibge_pagination.filteredRecordCount = ibge_pagination.totalRecordCount
    ibge_pagination.totalPages = ibge_pagination.totalRecordCount / payload.take
    ibge_pagination.currentPage = (payload.skip // payload.take) + 1

    return ibge_pagination
