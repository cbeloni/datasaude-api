from typing import Optional, List

from app.paciente.models.paciente_model import Paciente
from app.paciente.repository.paciente_repository import PacienteRepository
from core.db.session import session
from sqlalchemy import select, desc, asc

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
        start: int = 0
    ) -> List[Paciente]:
        query = select(Paciente)

        if prev:
            query = query.where(Paciente.id < prev)

        if limit > 1000:
            limit = 1000

        query = query.offset(start).limit(limit).order_by(desc(Paciente.id))

        return (await session.execute(query)).scalars().all()

async def paciente_count() -> int:
    return await PacienteRepository().count()
