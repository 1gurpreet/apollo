import asyncio

from pathlib import Path

from metadata.extractor import get_metadata_from_file
from pubsub import PubSub, TopicName, get_pubsub

from scanner import scan

global_tasks = set()

class Apollo():
    _music_scanner_task: asyncio.Task = None

    def __init__(self): 
        self.message_broker: PubSub = get_pubsub()

    async def start(self):
        """
        Start the Apollo server.
        """
        await self.message_broker.connect()

        # Start the apollo server by scanning music file changes.
        self.message_broker.publish(TopicName.START_SCAN, message={"path": "/home/user/Music", "type": "directory"})

        self._music_scanner_task = asyncio.create_task(self.scan_music())
        global_tasks.add(self._music_scanner_task)



    async def stop_scan(self):
        """
        Stop the music scanner.
        """
        if self._music_scanner_task:
            self._music_scanner_task.cancel()
            global_tasks.discard(self._music_scanner_task)
            self._music_scanner_task = None


    async def scan_music(self, continuous: bool = False):
        """
        Scan for music files.

        Args:
            continuous: If True, the scanner will run continuously.
        """
        await scan(continuous, task_name="music-scanner")

