from enum import Enum

from pubsub.base import PubSub
from pubsub.redis_pubsub import RedisPubSub


class TopicName(str, Enum):
    METADATA = "metadata"
    SCAN = "scan"
    START_SCAN = "start-scan"
    STOP_SCAN = "stop-scan"
    STREAM = "stream"
    TRANSCODE = "transcode"
    CONVERT = "convert"
    RENAME = "rename"
    DELETE = "delete"


class PubSubLibrary(str, Enum):
    REDIS = "redis"


def get_pubsub(library: str = PubSubLibrary.REDIS) -> PubSub:
    """
    Get a pubsub instance based on the library specified.

    Args:
        library: The library to use for pubsub. Currently only "redis" is supported.

    Returns:
        A pubsub reference.
    """
    if library == PubSubLibrary.REDIS:
        RedisPubSub.connect()
        return RedisPubSub
    else:
        raise ValueError(f"Unsupported library: {library}")
