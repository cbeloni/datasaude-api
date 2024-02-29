import asyncio, json, os
import logging
from aio_pika import IncomingMessage

from api.paciente.v1.request.paciente import PacienteTaskError, PacienteBase
from integrations.datasaude_api import paciente_salvar
from listeners.config import inicialize
from listeners.config import send_rabbitmq

from dotenv import load_dotenv
load_dotenv()


_datasaude_api = os.environ.get('DATASAUDE_API')

log = logging.getLogger(__name__)


async def on_message(message: IncomingMessage):
    payload = None
    try:
        log.info("Processamento mensagem {}".format(message.body))
        body = message.body.decode("utf-8")
        payload = json.loads(body)
        paciente = PacienteBase(**payload)
        result = await paciente_salvar(paciente.json())
        if (result.status_code != 200):
            await send_deadletter(payload, result.content)
        log.info(f"Fim mensagem {message.body} - resultado {result}")
        await message.ack()
    except Exception as e:
        log.error(f"Erro no processamento da mensagem: {e}")
        await send_deadletter (payload, str(e))
        await message.ack()


async def send_deadletter(payload, error_message):
    payload_deadletter = PacienteTaskError(**payload)
    payload_deadletter.error = error_message
    await send_rabbitmq(payload_deadletter.to_message(), "paciente_deadletter")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(inicialize(loop, "paciente_upsert", on_message))
    loop.run_forever()
