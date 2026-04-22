from fastapi import APIRouter, Depends

from api.maxacali.v1.request.maxacali import MaxacaliFiltroParams, MaxacaliListRequest, MaxacaliPagination
from app.maxacali.services.maxacali_service import maxacali_list
from app.user.schemas import ExceptionResponseSchema
from core.utils.counter import DrawConter
from core.utils.logger import LoggerUtils

log = LoggerUtils(__name__)

maxacali_router = APIRouter()
_counter = DrawConter()


@maxacali_router.post(
    "/listar",
    response_model=MaxacaliPagination,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def post_maxacali_list(
    filtro: MaxacaliFiltroParams = Depends(),
    payload: MaxacaliListRequest = None,
):
    log.info(f"Obtendo maxacali list {payload}")

    maxacali_pagination: MaxacaliPagination = MaxacaliPagination(
        counter=_counter.draw,
    )

    if payload is None:
        payload = MaxacaliListRequest(take=10, prev=None, skip=0, columns=[])

    maxacali_pagination.payload, maxacali_pagination.totalRecordCount = await maxacali_list(
        limit=payload.take,
        prev=payload.prev,
        start=payload.skip,
        filtro=filtro,
    )

    maxacali_pagination.filteredRecordCount = maxacali_pagination.totalRecordCount
    maxacali_pagination.totalPages = maxacali_pagination.totalRecordCount / payload.take
    maxacali_pagination.currentPage = (payload.skip // payload.take) + 1

    return maxacali_pagination
