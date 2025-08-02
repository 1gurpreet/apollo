from abc import ABC, abstractmethod


class MetadataExtractor(ABC):
    @abstractmethod
    async def extract(self, file_path: str) -> dict:
        pass
