from fastapi import APIRouter, Query

from api.poluentes.v1.response.poluente_scrap import PoluenteScrapResponse
from app.poluente.models.poluente_historico_model import PoluenteHistorico
from app.user.schemas import (
    ExceptionResponseSchema,
)
from core.db import BaseSqlite, sessionSqlite

poluente_historico_router = APIRouter()

@poluente_historico_router.get(
    "/{id}",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_poluente_scrap_by_id(
        id: int = Query(10, description="id do registro em poluente_scrap"),
):
    return sessionSqlite.query(PoluenteHistorico).all()
