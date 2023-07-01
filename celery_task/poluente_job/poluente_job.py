import asyncio
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from app.poluente.integrations import cetesb
from app.poluente.models import Poluente
from app.poluente.repository.poluente_repository import PoluenteRepository
from core.db import standalone_session

_poluenteRepository: PoluenteRepository = PoluenteRepository()


def poluente_job_task():
    @standalone_session
    async def salvar(**kwargs):
        p: Poluente = Poluente(**kwargs)
        await PoluenteRepository().save(p)

    logging.info('Starting job')
    asyncio.run(salvar(endereco='Rua arujá 2'))
    logging.info('Finish job')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cetesb.execute_get_capa, 'interval', minutes=5)
    # scheduler.add_job(poluente_job_task, 'interval', minutes=0.2)
    scheduler.start()
