import asyncio, time,json

from aio_pika import IncomingMessage
from config import inicialize
import logging

log = logging.getLogger(__name__)

async def on_message(message: IncomingMessage):
    try:
        log.info("Processamento mensagem {}".format(message.body))
        print("Processamento mensagem {}".format(message.body))
        body = message.body.decode("utf-8")
        message_body_dict = json.loads(body)
        time.sleep(int(message_body_dict["sleep"]))
        log.info("Fim mensagem {}".format(message.body))
        print("Fim mensagem {}".format(message.body))
        await message.ack()
    except Exception as e:
        log.error(f"Erro no processamento da mensagem: {e}")
        print(f"Erro no processamento da mensagem: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(inicialize(loop, "paciente_upsert", on_message))
    loop.run_forever()
