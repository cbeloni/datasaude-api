from fastapi import APIRouter
from core.db.session import session
from api.paciente.v1.request.paciente_coordenadas_request import PacienteCoordenadasLote
from app.paciente.services import coordenadas
from app.user.schemas import (
    ExceptionResponseSchema,
)
from distutils import log
paciente_router = APIRouter()

@paciente_router.post(
    "/coordenadas",
    response_model={},
    response_model_exclude={},
    responses={"400": {"model": ExceptionResponseSchema}},
    # dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def atualiza_paciente_coordenadas_lote(payload: PacienteCoordenadasLote):
    sql = """
            select p.id, concat(p.DS_ENDERECO,  ', ',  p.NR_ENDERECO,  ', ', p.NM_BAIRRO, ' - SP')
              from paciente p
             where not exists (select 1
                                from paciente_coordenadas pc
                               where pc.id_paciente = p.ID
                               and pc.provider = :provider)
              limit :limit;
            """

    pacientes = (await session.execute(sql, payload.to_dict())).all()
    dados_coordenadas_lista = []
    for paciente in pacientes:
        id_paciente = paciente[0]
        endereco = paciente[1]
        response = {'endereco': endereco, 'provider': payload.provider, 'id_paciente': id_paciente}
        try:
            dados_coordenadas = coordenadas.execute(endereco, payload.provider)

            response.update(dados_coordenadas)

        except Exception as ex:
            log.error("Não foi possível obter coordenadas %s" % paciente.id)

        inserir_sql = """
                                                INSERT INTO paciente_coordenadas (id_paciente, endereco, latitude, longitude, x, y, acuracia, provider, response, data_criacao, data_alteracao)
                                                VALUES (:id_paciente, :endereco, :latitude, :longitude, :x, :y, :acuracia, :provider, :response, NOW(), NOW())
                                            """
        await session.execute(inserir_sql, response)
        await session.commit()

        dados_coordenadas_lista.append(response)

    return dados_coordenadas_lista
