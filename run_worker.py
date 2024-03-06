import asyncio
import logging
from listeners.config import inicialize
from listeners.paciente_listener import on_message as on_message_paciente
from listeners.geolocalizacao_listener import on_message as on_message_geolocalizacao

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.info("Inicializando listener paciente")
    loop = asyncio.get_event_loop()
    loop.create_task(inicialize(loop, "paciente_upsert", on_message_paciente))
    loop.create_task(inicialize(loop, "geolocalizacao_upsert", on_message_geolocalizacao))
    loop.run_forever()
