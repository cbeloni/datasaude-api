from fastapi import APIRouter, Depends

from api.ibge.v1.request.ibge import (
    IbgeFiltroParams,
    IbgeFormulaCustomizadaCreate,
    IbgeFormulaCustomizadaListResponse,
    IbgeListRequest,
    IbgePagination,
)
from app.ibge.services.ibge_service import ibge_list
from app.ibge.services.ibge_formula_service import (
    criar_formula_customizada,
    listar_formulas_customizadas,
    remover_formula_customizada,
)
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


@ibge_router.get(
    '/formulas-customizadas',
    response_model=IbgeFormulaCustomizadaListResponse,
    responses={'400': {'model': ExceptionResponseSchema}},
)
async def get_formulas_customizadas():
    formulas = await listar_formulas_customizadas()
    return {'payload': formulas}


@ibge_router.post(
    '/formulas-customizadas',
    response_model=IbgeFormulaCustomizadaListResponse,
    responses={'400': {'model': ExceptionResponseSchema}},
)
async def post_formula_customizada(payload: IbgeFormulaCustomizadaCreate):
    await criar_formula_customizada(payload)
    formulas = await listar_formulas_customizadas()
    return {'payload': formulas}


@ibge_router.delete(
    '/formulas-customizadas/{formula_id}',
    response_model=IbgeFormulaCustomizadaListResponse,
    responses={'400': {'model': ExceptionResponseSchema}},
)
async def delete_formula_customizada(formula_id: int):
    await remover_formula_customizada(formula_id)
    formulas = await listar_formulas_customizadas()
    return {'payload': formulas}
