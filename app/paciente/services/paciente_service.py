from typing import Optional

from api.paciente.v1.request.paciente import FiltroParams, PacienteBase
from app.paciente.models.paciente_coordenadas import PacienteCoordenadas
from app.paciente.models.paciente_interpolacao import PacienteInterpolacao
from app.paciente.models.paciente_model import Paciente
from app.paciente.repository.paciente_repository import PacienteRepository
from core.db.session import session
from sqlalchemy import select, update, desc, text, func
from dateutil.parser import parse
import logging
log = logging.getLogger(__name__)

def query_pacientes():
    return """   
           SELECT p.cd_atendimento, p.nm_paciente, pi.id, pi.data, pc.endereco, pc.longitude, pc.latitude, pc.x, pc.y, pi.indice_interpolado as indice, pi.poluente
          FROM paciente p, paciente_coordenadas pc, paciente_interpolacao pi
         WHERE p.id = pc.id_paciente
           AND pc.id = pi.id_coordenada
           AND DT_ATENDIMENTO =  :dt_atendimento
           AND pi.poluente = :poluente
           AND pc.validado = 1
           AND pc.latitude is not null;
    """

async def obtem_paciente_service(filtros):
    pacientes = (await session.execute(query_pacientes(), filtros.to_dict())).all()
    return pacientes


async def paciente_list(
        limit: int = None,
        prev: Optional[int] = None,
        start: int = 0,
        filter: FiltroParams = None
    ) -> (any, int):
        query = (select(Paciente.id, Paciente.CD_ATENDIMENTO, Paciente.NM_PACIENTE, Paciente.DT_ATENDIMENTO, Paciente.TP_ATENDIMENTO, Paciente.DS_ORI_ATE, Paciente.DS_LEITO, Paciente.DT_ALTA, Paciente.CD_SGRU_CID, Paciente.CD_CID, Paciente.DS_CID, Paciente.SN_INTERNADO, Paciente.DS_ENDERECO, Paciente.NR_ENDERECO, Paciente.NM_BAIRRO, Paciente.NR_CEP, Paciente.DT_NASC, Paciente.IDADE, Paciente.TP_SEXO,
                       PacienteCoordenadas.endereco, PacienteCoordenadas.latitude, PacienteCoordenadas.longitude,
                        PacienteInterpolacao.poluente, PacienteInterpolacao.indice_interpolado)
                 .join(PacienteCoordenadas, Paciente.id == PacienteCoordenadas.id_paciente)
                 .join(PacienteInterpolacao, PacienteCoordenadas.id == PacienteInterpolacao.id_coordenada)
                 .where(PacienteCoordenadas.validado == 1))

        if prev:
            query = query.where(Paciente.id < prev)

        if filter.dt_atendimento_inicial is not None:
            query = query.where(Paciente.DT_ATENDIMENTO >= parse(filter.dt_atendimento_inicial))
        if filter.dt_atendimento_final is not None:
            query = query.where(Paciente.DT_ATENDIMENTO <= parse(filter.dt_atendimento_final))
        if filter.idade_meses is not None:
            query = query.where(text("TIMESTAMPDIFF(MONTH, dt_nasc, CURRENT_DATE()) = :idade_meses").bindparams(idade_meses=filter.idade_meses))
        if filter.idade_anos is not None:
            query = query.where(text("TIMESTAMPDIFF(YEAR, dt_nasc, CURRENT_DATE()) = :idade_anos").bindparams(idade_anos=filter.idade_anos))


        if limit > 1000:
            limit = 1000

        count_query = select([func.count()]).select_from(query.alias())
        print(count_query)
        quantidade = (await session.execute(count_query)).scalar()

        query = query.offset(start).limit(limit).order_by(desc(Paciente.id))
        registros = (await session.execute(query)).all()

        # print(str(query))
        return (registros, quantidade)

async def paciente_count() -> int:
    return await PacienteRepository().count()

async def get_paciente_coordenadas(id) -> any:

    query = (
        select(PacienteCoordenadas.id, PacienteCoordenadas.longitude,PacienteCoordenadas.longitude, PacienteCoordenadas.endereco, Paciente, PacienteInterpolacao)
        .join(PacienteCoordenadas, Paciente.id == PacienteCoordenadas.id_paciente)
        .join(PacienteInterpolacao, PacienteCoordenadas.id == PacienteInterpolacao.id_coordenada)
        .where(PacienteCoordenadas.id == id)
        .where(PacienteCoordenadas.validado == 1)
    )
    print(query)
    registros = (await session.execute(query)).all()
    return registros


async def salvar_paciente(pacienteBase: PacienteBase):
    log.debug(f"pacienteBase {pacienteBase}")
    cd_atendimento = pacienteBase.CD_ATENDIMENTO
    query = select(Paciente).where(Paciente.CD_ATENDIMENTO == cd_atendimento)
    paciente_existente = await session.execute(query)
    paciente_existente = paciente_existente.scalar_one_or_none()
    paciente = Paciente(**pacienteBase.to_model())
    if paciente_existente:
        await session.execute(
            update(Paciente)
            .where(Paciente.CD_ATENDIMENTO == cd_atendimento)
            .values(**pacienteBase.to_model())
        )
    else:
        session.add(paciente)

    await session.commit()
    paciente_retorno = await session.execute(query)
    return paciente_retorno.scalar_one_or_none()
