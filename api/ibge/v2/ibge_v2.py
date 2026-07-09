from fastapi import APIRouter

from api.ibge.v2.request.ibge import (
    IbgeFormulaCustomizadaCreate,
    IbgeFormulaCustomizadaListResponse,
    IbgeMongoQueryRequest,
    IbgeMongoQueryResponse,
)
from app.ibge.services.ibge_mongo_formula_service import (
    criar_formula_customizada,
    listar_formulas_customizadas,
    remover_formula_customizada,
)
from app.ibge.services.ibge_mongo_query_service import consultar_colecao_mongo
from app.user.schemas import ExceptionResponseSchema
from core.utils.logger import LoggerUtils

log = LoggerUtils(__name__)

ibge_v2_router = APIRouter()


@ibge_v2_router.post(
    "/mongo/consultar",
    response_model=IbgeMongoQueryResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def post_ibge_mongo_consultar(payload: IbgeMongoQueryRequest):
    log.info(
        "Consultando collection MongoDB %s com colunas %s",
        payload.collection_name,
        payload.columns,
    )
    return await consultar_colecao_mongo(payload)


@ibge_v2_router.get(
    "/formulas-customizadas",
    response_model=IbgeFormulaCustomizadaListResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_formulas_customizadas():
    formulas = await listar_formulas_customizadas()
    return {"payload": formulas}


@ibge_v2_router.post(
    "/formulas-customizadas",
    response_model=IbgeFormulaCustomizadaListResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def post_formula_customizada(payload: IbgeFormulaCustomizadaCreate):
    await criar_formula_customizada(payload)
    formulas = await listar_formulas_customizadas()
    return {"payload": formulas}


@ibge_v2_router.delete(
    "/formulas-customizadas/{formula_id}",
    response_model=IbgeFormulaCustomizadaListResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def delete_formula_customizada(formula_id: str):
    await remover_formula_customizada(formula_id)
    formulas = await listar_formulas_customizadas()
    return {"payload": formulas}
