from typing import Optional, List

from api.paciente.v1.request.paciente import FiltroParams
from app.paciente.models.paciente_model import Paciente
from app.paciente.repository.paciente_repository import PacienteRepository
from core.db.session import session
from sqlalchemy import select, desc, asc, text, func
from dateutil.parser import parse

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
        query = select(Paciente)

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
        quantidade = (await session.execute(count_query)).scalar()

        query = query.offset(start).limit(limit).order_by(desc(Paciente.id))
        registros = (await session.execute(query)).scalars().all()

        # print(str(query))
        return (registros, quantidade)

async def paciente_count() -> int:
    return await PacienteRepository().count()
