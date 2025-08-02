from metadata.extractor.base import MetadataExtractor

from mutagen import File


class Mp3MetadataExtractor(MetadataExtractor):
    async def extract(self, file_path: str) -> dict:
        """
        Extracts metadata from an MP3 file.

        Args:
            file_path (str): The path to the MP3 file to extract metadata from.

        Returns:
            dict: A dictionary containing the metadata.
        """
        audio = File(file_path)
        for key, value in audio.items():
            print(key, value)
