import logging

from app.paciente.services.queries import query_factory
from core.db import session


async def gera_previsao_serie_temporal(filtro):
    logging.info("Iniciando previsão série temporal")
    await session.execute(query_factory("previsao"), filtro)
    await session.commit()
    return True
