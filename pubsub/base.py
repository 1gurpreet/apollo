from abc import ABC, abstractmethod
from typing import Callable


class PubSub(ABC):
    @abstractmethod
    def connect(self, host: str = "localhost", port: int = 6379, db: int = 0):
        pass

    @abstractmethod
    async def publish(self, topic: str, message: dict):
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable):
        pass

    @abstractmethod
    async def unsubscribe(self, topic: str):
        pass
