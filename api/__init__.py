from fastapi import APIRouter

from api.user.v1.user import user_router as user_v1_router
from api.auth.auth import auth_router
from api.poluentes.v1.poluente import  poluente_router as poluente_v1_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(poluente_v1_router, prefix="/api/v1/poluentes", tags=["Poluentes"])


__all__ = ["router"]
