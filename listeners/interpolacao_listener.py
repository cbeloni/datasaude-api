import asyncio, json, os
import logging
from aio_pika import IncomingMessage

from api.paciente.v1.request.paciente import PacienteInterpolacaoTask
from app.poluente.services.interpolacao_service import indice_poluente_por_id
from listeners.config import inicialize

from dotenv import load_dotenv

from listeners.paciente_listener import send_deadletter

load_dotenv()


_datasaude_api = os.environ.get('DATASAUDE_API')

log = logging.getLogger(__name__)

async def on_message(message: IncomingMessage):
    payload = None
    try:
        log.info("Processamento mensagem {}".format(message.body))
        body = message.body.decode("utf-8")
        payload = json.loads(body)
        paciente = PacienteInterpolacaoTask(**payload)
        result = await indice_poluente_por_id(paciente.id)
        if (result.status_code != 200):
            await send_deadletter(payload, result.content)
        log.info(f"Fim mensagem {message.body} - resultado {result}")
        await message.ack()
    except Exception as e:
        log.error(f"Erro no processamento da mensagem: {e}")
        await send_deadletter (payload, str(e))
        await message.ack()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(inicialize(loop, "interpolacao_insert", on_message))
    loop.run_forever()
