from fastapi import APIRouter, Header, Depends, Query

from api.paciente.v1.request.paciente import PacientePagination, PacienteListRequest, FiltroParams, PacienteBase, \
    PacienteTask
from api.paciente.v1.request.paciente_coordenadas_request import PacienteCoordenadasLote
from api.paciente.v1.request.paciente_internacao import PacienteInternacaoPayload
from api.paciente.v1.request.paciente_interpolacao_request import PacienteInterpolacaoLote
from api.paciente.v1.request.paciente_request import PacienteRequest
from app.paciente.services.coordenadas_insert import service_atualiza_paciente_coordenadas_lote, \
    service_atualiza_paciente_por_id
from app.paciente.services.paciente_service import obtem_paciente_service, paciente_list, get_paciente_coordenadas, \
    salvar_paciente
from app.poluente.services.interpolacao_service import indice_poluente_lote
from app.paciente.services.internacao_service import execute as internacao_service_execute
from fastapi.responses import JSONResponse

from app.user.schemas import (
    ExceptionResponseSchema,
)
# from distutils import log
import logging

from listeners.config import send_rabbitmq

log = logging.getLogger(__name__)
from core.utils.counter import DrawConter

paciente_router = APIRouter()

_counter = DrawConter()

@paciente_router.post(
    "/coordenadas",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def atualiza_paciente_coordenadas_lote(payload: PacienteCoordenadasLote):
    log.info("Iniciando atualização paciante coordenadas lote")
    return await service_atualiza_paciente_coordenadas_lote(payload)

@paciente_router.post(
    "/coordenadas/{id}",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def atualiza_paciente_coordenadas_lote(id: int = Query(10, description="id do paciente")):
    log.info("Iniciando atualização paciante por id")
    return await service_atualiza_paciente_por_id(id)

@paciente_router.post(
    "/interpolacao",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def atualiza_paciente_interpolacao_lote(payload: PacienteInterpolacaoLote):
    log.info("Iniciando atualização paciante interpolacao lote")
    return await indice_poluente_lote(payload)

@paciente_router.post(
    "/internacao",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def analisa_risco_internacao(payload: PacienteInternacaoPayload,
                                   token: str = Header(..., description="Token de autenticação")):
    log.info(f"Iniciando análise risco internação {payload}")
    return internacao_service_execute(payload, token)

@paciente_router.post(
    "/",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def obtem_paciente(payload: PacienteRequest):
    log.info(f"Obtendo paciante {payload}")
    return await obtem_paciente_service(payload)

@paciente_router.post(
    "/listar",
    response_model=PacientePagination,
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def post_paciente_list(
    filtro: FiltroParams = Depends(),
    payload: PacienteListRequest = None
):
    log.info(f"Obtendo paciante list {payload}")
    pacientePagination: PacientePagination = PacientePagination(
        counter=_counter.draw,
    )

    (pacientePagination.payload, pacientePagination.totalRecordCount) \
        = await paciente_list(limit=payload.take,
                              prev=payload.prev,
                              start=payload.skip,
                              filter=filtro)

    pacientePagination.filteredRecordCount = pacientePagination.totalRecordCount
    pacientePagination.totalPages = pacientePagination.totalRecordCount / payload.take
    pacientePagination.currentPage = (payload.skip // payload.take) + 1

    return pacientePagination

@paciente_router.get(
"/coordenadas",
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def paciente_coordenadas(id: int):
    return await get_paciente_coordenadas(id)

@paciente_router.post(
    "/salvar",
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def post_paciente_salvar(
    payload: PacienteBase = None
):
    log.info(f"Salvando paciante {payload}")
    return await salvar_paciente(payload)

@paciente_router.post("/async", status_code=201)
async def run_task(payload: PacienteTask):
    await send_rabbitmq(payload.to_message(), "paciente_upsert")
    content = {"message": "sucess"}
    return JSONResponse(content=content, status_code=200)

@paciente_router.post("/geolocalizacao/async", status_code=201)
async def run_task(payload: PacienteTask):
    await send_rabbitmq(payload.to_message(), "geolocalizacao_upsert")
    content = {"message": "sucess"}
    return JSONResponse(content=content, status_code=200)

