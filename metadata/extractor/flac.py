from metadata.extractor.extractor import MetadataExtractor
from mutagen import File


class FlacExtractor(MetadataExtractor):
    def extract(self, file_path: str) -> dict:
        '''
        Extracts metadata from an MP3 file.

        Args:
            file_path (str): The path to the MP3 file to extract metadata from.

        Returns:
            dict: A dictionary containing the metadata.
        '''
        audio = File(file_path)

        metadata = {}

        if "title" in audio.tags:
            metadata["title"] = audio["title"][0]
        if "artist" in audio.tags:
            metadata["artist"] = audio["artist"][0]
        if "album" in audio.tags:
            metadata["album"] = audio["album"][0]
        if "date" in audio.tags:
            metadata["date"] = audio["date"][0]
        if "genre" in audio.tags:
            metadata["genre"] = audio["genre"][0]
        if "tracknumber" in audio.tags:
            metadata["tracknumber"] = audio["tracknumber"][0]
        if "discnumber" in audio.tags:
            metadata["discnumber"] = audio["discnumber"][0]
        if "picture" in audio.tags:
            metadata["picture"] = audio["picture"][0]
        if "lyrics" in audio.tags:
            metadata["lyrics"] = audio["lyrics"][0]
        if "composer" in audio.tags:
            metadata["composer"] = audio["composer"][0]
        if "copyright" in audio.tags:
            metadata["copyright"] = audio["copyright"][0]
        if "encoder" in audio.tags:
            metadata["encoder"] = audio["encoder"][0]
        if "language" in audio.tags:
            metadata["language"] = audio["language"][0]
        if "publisher" in audio.tags:
            metadata["publisher"] = audio["publisher"][0]
        if "encodedby" in audio.tags:
            metadata["encodedby"] = audio["encodedby"][0]
        if "originaldate" in audio.tags:
            metadata["originaldate"] = audio["originaldate"][0]
        if "originalfilename" in audio.tags:
            metadata["originalfilename"] = audio["originalfilename"][0]
        if "originalartist" in audio.tags:
            metadata["originalartist"] = audio["originalartist"][0]
        if "originalalbum" in audio.tags:
            metadata["originalalbum"] = audio["originalalbum"][0]

        return metadata
