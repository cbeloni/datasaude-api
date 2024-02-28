from typing import Callable

from aio_pika import connect, Message
import os
from dotenv import load_dotenv

load_dotenv()

_rabbit = os.environ.get('RABBIT')


async def inicialize(loop: any, queue: str, on_message: Callable):
    connection = await connect(_rabbit, loop = loop)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(queue)
    await queue.consume(on_message, no_ack = False)


async def send_rabbitmq(msg: Message, queue: str):
    connection = await connect(_rabbit)
    channel = await connection.channel()
    await channel.default_exchange.publish(
        msg,
        routing_key=queue
    )
    await connection.close()
