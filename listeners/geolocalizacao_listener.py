import asyncio, time, json
from aio_pika import IncomingMessage
from config import inicialize


async def on_message(message: IncomingMessage):
    print("Processamento mensagem {}".format(message.body))
    body = message.body.decode("utf-8")
    message_body_dict = json.loads(body)
    time.sleep(int(message_body_dict["sleep"]))
    print("Fim mensagem {}".format(message.body))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(inicialize(loop, "geolocalizacao_upsert", on_message))
    loop.run_forever()
