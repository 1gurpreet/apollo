import asyncio
import watchdog
import logging

from os import walk
from os.path import isdir, join
from pathlib import Path

from .. import PubSub, TopicName, get_pubsub


message_broker: PubSub = get_pubsub()

logger = logging.getLogger("DIRECTORY-SCANNER")
logger.setLevel(logging.INFO)


class Directories:
    _directories: asyncio.Queue[Path] = asyncio.Queue()

    def __init__(self, directories: list[Path] = []):
        self._directories: asyncio.Queue[Path] = asyncio.Queue()
        for directory in directories:
            if isdir(directory):
                self.directories.put_nowait(Path(directory))

    async def sync_to_db(self):
        """
        Sync the directories with the database.
        """
        message_broker.publish(TopicName.SYNC_TO_DB, message={"type": "directory"})

    async def sync_from_db(cls, message: dict):
        """
        Grab directory paths from the database.
        """
        if message.get("type") == "directory":
            for directory in message.get("directories"):
                await cls._directories.put(Path(directory))

    async def add(self, directory: str):
        """
        Add a directory to the queue.

        Args:
            directory: The directory to add.
        """

        if isdir(directory):
            await self.directories.put(Path(directory))
        else:
            error_msg = f"'{directory}' is not a directory or does not exist"
            logger.error(error_msg)
            #raise ValueError(error_msg)

        logger.info(f"Adding directory: {directory}")

    async def __aiter__(self):
        """
        Iterate over the directories in the queue.

        Yields:
            Path: The next directory in the queue.
        """
        while True:
            yield await self.directories.get()


async def scan(directories: Directories, watchdog_mode: bool = False):
    """
    Scan a directory for files and publish them to the pubsub topic.

    Args:
        directories: The directories to scan.
        watchdog_mode: If True, the directories will actively be monitored for changes.
    """

    if watchdog_mode:
        #TODO: Implement watchdog mode
        pass
    else:
        async for directory in directories:
            for root, _, files in walk(directory):
                for f in files:
                    message_broker.publish(TopicName.SCAN, message={"path": join(root, f), "type": "file"})


message_broker.subscribe(TopicName.SYNC_FROM_DB, Directories.sync_from_db)

