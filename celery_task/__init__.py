import time

from celery import Celery

celery_app = Celery('tasks', broker="redis://redis:6379")

@celery_app.task(name="paciente_task")
def paciente_task(task_type):
    print("Iniciando task")
    time.sleep(int(task_type) * 10)
    print("Finalizando task")
    return True