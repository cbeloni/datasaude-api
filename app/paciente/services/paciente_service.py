from core.db.session import session
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
