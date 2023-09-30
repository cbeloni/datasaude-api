from fastapi import APIRouter

from app.user.schemas import (
    ExceptionResponseSchema,
)
paciente_router = APIRouter()

@paciente_router.get(
    "",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_paciente():
    return "Success"