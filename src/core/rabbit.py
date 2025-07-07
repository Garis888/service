from src.core.utils import Singleton
from src.config import settings
from aio_pika import connect, Message
from loguru import logger


class Rabbit(metaclass=Singleton):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def disconnect(self) -> None:
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        self.connection = None
        self.channel = None

    async def connect(self) -> bool:
        try:
            logger.info(f"RABBIT_USER: {settings.RABBIT_USER} RABBIT_HOST: {settings.RABBIT_HOST} RABBIT_PORT: {settings.RABBIT_PORT}")
            url = f'amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}@{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/%2F'
            #url = f'amqp://guest:guest@localhost:5672/%2F'
            self.connection = await connect(url)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                'direct',
                auto_delete=False,
            )
            logger.info(f"Rabbit connect success!")
            return True
        except Exception as e:
            logger.error(f"Rabbit connect error!")
            await self.disconnect()
            return False

    async def send_message(
            self,
            routing_key,
            msg: str,
    ) -> None:
        message = Message(
            body=msg,
            delivery_mode=2,
        )
        queue = await self.channel.declare_queue(
            name=routing_key,
            auto_delete=False,
        )
        await queue.bind(self.exchange, routing_key)
        await self.exchange.publish(
            message=message,
            routing_key=routing_key,
        )
