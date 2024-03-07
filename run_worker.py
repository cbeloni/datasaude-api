import asyncio
import logging
from listeners.config import inicialize
from listeners.paciente_listener import on_message as on_message_paciente
from listeners.geolocalizacao_listener import on_message as on_message_geolocalizacao
from listeners.interpolacao_listener import on_message as on_message_interpolacao

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.info("Inicializando listener paciente")
    loop = asyncio.get_event_loop()
    log.info("Iniciando listeners")

    # Inicializa todas as tarefas
    task_paciente = inicialize(loop, "paciente_upsert", on_message_paciente)
    task_geolocalizacao = inicialize(loop, "geolocalizacao_upsert", on_message_geolocalizacao)
    task_interpolacao = inicialize(loop, "interpolacao_insert", on_message_interpolacao)

    tasks = [task_paciente, task_geolocalizacao, task_interpolacao]

    # Executa todas as tarefas em paralelo
    loop.run_until_complete(asyncio.gather(*tasks))

    log.info("Listeners inicializados")
    loop.run_forever()
