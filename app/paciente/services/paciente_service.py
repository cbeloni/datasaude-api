from core.db.session import session
def query_pacientes():
    return """
        SELECT p.id, p.CD_ATENDIMENTO, p.NM_PACIENTE, p.DT_ATENDIMENTO, p.DS_ORI_ATE, p.DS_LEITO, p.DT_ALTA,
               p.ds_cid, pc.endereco, pc.longitude, pc.latitude, pc.x, pc.y
          FROM paciente p, paciente_coordenadas pc
         WHERE p.id = pc.id_paciente
           AND DT_ATENDIMENTO = :dt_atendimento
           AND pc.validado = 1;
    """

async def obtem_paciente_service(filtros):
    pacientes = (await session.execute(query_pacientes(), filtros.to_dict())).all()
    return pacientes
