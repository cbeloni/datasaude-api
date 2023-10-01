from fastapi import APIRouter

from api.user.v1.user import user_router as user_v1_router
from api.auth.auth import auth_router
from api.poluentes.v1.poluente_v1 import poluente_router as poluente_v1_router
from api.poluentes.v1.poluente_scrap_v1 import poluente_scrap_router as poluente_scrap_v1_router
from api.poluentes.v1.poluente_historico_v1 import poluente_historico_router as poluente_historico_v1_router
from api.paciente.v1.paciente_v1 import paciente_router as paciete_v1_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(poluente_v1_router, prefix="/api/v1/poluentes", tags=["Poluentes"])
router.include_router(poluente_scrap_v1_router, prefix="/api/v1/poluentes_scrap", tags=["PoluentesScrap"])
router.include_router(poluente_historico_v1_router, prefix="/api/v1/poluentes_historico", tags=["PoluentesHistorico"])
router.include_router(paciete_v1_router, prefix="/api/v1/paciente", tags=["Paciente"])


__all__ = ["router"]
