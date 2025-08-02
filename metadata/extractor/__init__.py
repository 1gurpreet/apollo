import asyncio
import os

from metadata.extractor.m4a import M4aExtractor
from metadata.extractor.flac import FlacExtractor
from metadata.extractor.wav import WavExtractor
from metadata.extractor.ape import ApeExtractor
from metadata.extractor.base import MetadataExtractor


__all__ = ["get_metadata_from_file"]


def get_extractor(file_type: str) -> MetadataExtractor:
    """
    Returns a MetadataExtractor instance based on the file type.

    Args:
        file_type (str): The type of file to extract metadata from.

    Returns:
        MetadataExtractor: An instance of the appropriate MetadataExtractor subclass.

    Raises:
        ValueError: If the file type is not supported.
    """
    if file_type == "m4a":
        return M4aExtractor()
    elif file_type == "flac":
        return FlacExtractor()
    elif file_type == "wav":
        return WavExtractor()
    elif file_type == "ape":
        return ApeExtractor()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


async def get_metadata_from_file(file_path: str) -> dict:
    """
    Extracts metadata from a file.

    Args:
        file_path (str): The path to the file to extract metadata from.
    """
    _, file_extension = os.path.splitext(file_path)
    extractor = get_extractor(file_type=file_extension.lower().replace(".", ""))
    # File I/O is blocking, so we need to run extract in a separate thread so that the event loop is not blocked.
    return await asyncio.to_thread(extractor.extract, file_path)