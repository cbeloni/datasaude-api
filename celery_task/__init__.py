from datetime import timedelta

from celery import Celery
from core.config import config
# from celery.schedules import crontab
# from celery import shared_task

celery_app = Celery(
    "worker",
    backend=config.CELERY_BACKEND_URL,
    broker=config.CELERY_BROKER_URL,
)

celery_app.conf.task_routes = {"worker.celery_worker.test_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)

# @shared_task()
# def my_task():
#     # Código da função a ser executada periodicamente
#     print("Executando minha tarefa a cada hora")
#
# beat_schedule = {
#     'executar-tarefa-a-cada-segundo': {
#         'task': 'tasks.my_task',
#         'schedule': timedelta(seconds=1),
#     },
# }

# celery_app.autodiscover_tasks()
