import time

from celery import Celery

celery_app = Celery('tasks', broker="amqp://guest:guest@177.93.130.249:5672")


@celery_app.task(name="paciente_task", queue='paciente')
def paciente_task(task_type):
    print("Iniciando task")
    time.sleep(int(task_type) * 10)
    print("Finalizando task")
    return True
