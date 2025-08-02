import asyncio

from scanner.directory import scan

from pubsub import PubSub, TopicName, get_pubsub


message_broker: PubSub = get_pubsub()


def start_scan(message: dict):
    """
    Start the scan.
    """
    if message.get("type") == "directory":
        pass
    else:
        print(message)


def stop_scan(message: dict):
    """
    Stop the scan.
    """
    print(message)


message_broker.subscribe(TopicName.START_SCAN, start_scan)
message_broker.subscribe(TopicName.STOP_SCAN, stop_scan)


async def gather(directories: Directories, continuous: bool = False, task_name: str = "directory-scanner"):
    """
    This Gather function is used to gather all the files in the directories.

    Args:
        directories: The directories to scan.
        continuous: If True, the scanner will run continuously.
        task_name: The name of the task.
    """
    await asyncio.create_task(scan(directories, watchdog_mode=continuous), name=task_name)


