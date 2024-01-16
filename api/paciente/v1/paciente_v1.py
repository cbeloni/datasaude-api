from fastapi import APIRouter, Header, Query

from api.paciente.v1.request.paciente import PacientePagination, PacienteListRequest
from api.paciente.v1.request.paciente_coordenadas_request import PacienteCoordenadasLote
from api.paciente.v1.request.paciente_internacao import PacienteInternacaoPayload
from api.paciente.v1.request.paciente_interpolacao_request import PacienteInterpolacaoLote
from api.paciente.v1.request.paciente_request import PacienteRequest
from app.paciente.services.coordenadas_lote import service_atualiza_paciente_coordenadas_lote
from app.paciente.services.paciente_service import obtem_paciente_service, paciente_list, paciente_count
from app.poluente.services.interpolacao_service import indice_poluente_lote
from app.paciente.services.internacao_service import execute as internacao_service_execute

from app.user.schemas import (
    ExceptionResponseSchema,
)
from distutils import log

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
    payload: PacienteListRequest
):
    pacientePagination: PacientePagination = PacientePagination(
        Counter=_counter.draw,
    )

    pacientePagination.Payload = await paciente_list(limit=payload.take,
                                                      prev=payload.prev,
                                                      start=payload.skip)
    pacientePagination.TotalRecordCount = await paciente_count()
    pacientePagination.FilteredRecordCount = pacientePagination.TotalRecordCount
    pacientePagination.TotalPages = pacientePagination.TotalRecordCount / payload.take
    pacientePagination.CurrentPage = (payload.skip // payload.take) + 1

    return pacientePagination
