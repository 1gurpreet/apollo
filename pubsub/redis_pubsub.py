import asyncio
import logging
import redis.asyncio as redis

from typing import Callable

from redis.exceptions import ConnectionError
from pubsub.base import PubSub


logger = logging.getLogger("REDIS-PUBSUB")
logger.setLevel(logging.ERROR)

class RedisPubSub(PubSub):
    _r: redis.Redis = None
    _futures: set[asyncio.Task] = set()

    def __init__(self):
        raise RuntimeError("Direct instantiation is not allowed. Use classmethods only.")

    @classmethod
    def connect(cls, host: str = "localhost", port: int = 6379, db: int = 0):
        """
        Connect to a Redis server.

        Args:
            host: The host of the Redis server.
            port: The port of the Redis server.
            db: The database to use.
        """
        try:
            cls._r = redis.Redis(host=host, port=port, db=db)
        except ConnectionError as _:
            cls._r = None

            error_msg = f"Failed to connect to Redis server please check if the Redis server is installed and running."
            logger.critical(error_msg)

    @classmethod
    async def publish(cls, topic: str, message: dict):
        """
        Publish a message to a topic.

        Args:
            topic: The topic to publish to.
            message: The message to publish.
        """
        await cls._r.publish(topic, message)

    @classmethod
    async def _subscribe_and_listen(cls, topic: str, callback: Callable):
        """
        Subscribe to a topic.

        Args:
            topic: The topic to subscribe to.
            callback: The callback to call when a message is published. 
        """
        task = await cls._r.subscribe(topic)
        cls._futures.add(task)
        task.add_done_callback(cls._futures.discard)

        while True:
            message = await cls._r.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                await callback(message)
                if message.get("type") == "unsubscribe":
                    logger.info(f"Unsubscribed from topic: {topic}")
                    await cls._r.unsubscribe(topic)
                    task.done()
                    break
            await asyncio.sleep(0.1)  # Small delay to prevent busy-waiting
     
    @classmethod
    async def subscribe(cls, topic: str, callback: Callable):
        """
        The task is added to the class's tasks set.
        The task is returned to the caller.

        Args:
            topic: The topic to subscribe to.
            callback: The callback to call when a message is published.
        """
        await cls._subscribe_and_listen(topic, callback)
    

    @classmethod
    async def unsubscribe(cls, callback: Callable, topic: str):
        """
        Unsubscribe from a topic.

        Args:
            topic: The topic to unsubscribe from.
        """
        await cls._r.unsubscribe(topic)

