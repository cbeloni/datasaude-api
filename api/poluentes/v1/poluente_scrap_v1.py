from fastapi import APIRouter, Query

from api.poluentes.v1.request.poluente_scrap import PoluenteScrapRequest
from api.poluentes.v1.response.poluente_scrap import PoluenteScrapResponse
from app.poluente.services.poluente_scrap_service import PoluenteScrapService
from app.user.schemas import (
    ExceptionResponseSchema,
)

poluente_scrap_router = APIRouter()
_poluenteScrapService = PoluenteScrapService()

@poluente_scrap_router.get(
    "/{id}",
    response_model=PoluenteScrapResponse,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_poluente_scrap_by_id(
        id: int = Query(10, description="id do registro em poluente_scrap"),
):
    return await _poluenteScrapService.get_poluente_scrap_by_id(id=id)

@poluente_scrap_router.post(
    "",
    response_model=None,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def post_poluente_scrap(
        payload: PoluenteScrapRequest,
):

    return await _poluenteScrapService.save_poluente_scrap(poluente_scrap_request=payload)