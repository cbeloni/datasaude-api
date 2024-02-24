# import time
#
# from celery import Celery
#
# celery_app = Celery('tasks', broker="redis://177.93.130.51:6379")
# # rabbit_app = Celery('tasks', broker='amqp://guest:guest@177.93.130.249:5672/')
# rabbit_app = Celery('tasks', broker="amqp://guest:guest@177.93.130.249:5672")
#
#
# @celery_app.task(name="paciente_task")
# def paciente_task(task_type):
#     print("Iniciando task")
#     time.sleep(int(task_type) * 10)
#     print("Finalizando task")
#     return True
#
#
# @rabbit_app.task(name="geolocalizacao_task")
# def geolocalizacao_task(task_type):
#     print("Iniciando geolocalizacao_task")
#     time.sleep(int(task_type) * 10)
#     print("Finalizando geolocalizacao_task")
#     return True