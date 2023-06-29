import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from app.poluente.integrations import cetesb
from app.poluente.models import Poluente
from app.poluente.repository.poluente_repository import PoluenteRepository

_poluenteRepository: PoluenteRepository = PoluenteRepository()

def scheduled_task():
    print("Executando tarefa agendada")
    # poluente: Poluente = Poluente(endereco= 'Rua arujá')
    # asyncio.run(_poluenteRepository.save(poluente))

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(cetesb.capa, 'interval', minutes=0.2)
    scheduler.add_job(scheduled_task, 'interval', minutes=2)
    scheduler.start()
