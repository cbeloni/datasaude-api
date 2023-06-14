from typing import List

from fastapi import APIRouter, Depends, Query

from api.poluentes.v1.response.poluente import PoluenteBase
from app.poluente.models import Poluente
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


@poluente_router.get(
    "",
    response_model=List[PoluenteBase],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_poluente_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    return await PoluenteService().get_poluente_list(limit=limit, prev=prev)

