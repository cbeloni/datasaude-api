from typing import Callable

from aio_pika import connect, Message
import os, json
from dotenv import load_dotenv

load_dotenv()

_rabbit = os.environ.get('RABBIT')


async def inicialize(loop: any, queue: str, on_message: Callable):
    connection = await connect(_rabbit, loop = loop)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue)
    await queue.consume(on_message, no_ack = True)


async def send_rabbitmq(msg, queue: str):
    connection = await connect(_rabbit)
    channel = await connection.channel()
    await channel.default_exchange.publish(
        Message(json.dumps(msg.dict()).encode("utf-8")),
        routing_key=queue
    )
    await connection.close()
