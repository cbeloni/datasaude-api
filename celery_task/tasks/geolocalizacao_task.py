import time

from celery import Celery

celery_app = Celery('tasks', broker="amqp://guest:guest@177.93.130.249:5672")


@celery_app.task(name="geolocalizacao_task", queue='geolocalizacao')
def geolocalizacao_task(task_type):
    print("Iniciando geolocalizacao_task")
    time.sleep(int(task_type) * 10)
    print("Finalizando geolocalizacao_task")
    return True
