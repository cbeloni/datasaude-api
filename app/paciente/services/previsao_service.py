from core.utils.logger import LoggerUtils

from app.paciente.services.queries import query_factory
from core.db import session

log = LoggerUtils(__name__)

async def gera_previsao_serie_temporal(filtro):
    log.info("Iniciando previsão série temporal")
    await session.execute(query_factory("previsao"), filtro)
    await session.commit()
    return True

async def upsert_previsao_serie_temporal(filtro):
    log.info("Iniciando upsert_previsao_serie_temporal ")
    result = await session.execute(query_factory("select_paciente_previsao"), filtro)
    rows = result.fetchall()

    for row in rows:
        data = row['dt_atendimento']
        valor_historico = row['atendimentos']
        cid = row['cid']
        tipo_analise = row['tipo_analise']
        qtd_pp = row['qtd_pp']
        filtro_upsert = { "data": data, "valor_historico": valor_historico, "cid": cid, "tipo_analise": tipo_analise }
        if qtd_pp > 0:
            log.info(f"executando update: {filtro_upsert}")
            query = query_factory("update_paciente_previsao")
        else:
            log.info(f"executando insert: {filtro_upsert}")
            query = query_factory("insert_paciente_previsao")
        
        # Execute the query (assuming you have a function to execute queries)
        await session.execute(query, filtro_upsert)
        await session.commit()
        
    return True