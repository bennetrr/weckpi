"""A player for internet radio with metadata access"""
from music.player import SingleMediaPlayer
from music.metadata import InternetRadioMetadataApi, NowPlaying


class InternetRadioPlayer(SingleMediaPlayer):
    """A player for internet radio with metadata access"""
    metadata_api: InternetRadioMetadataApi

    def __init__(self, media_source: str, metadata_api: InternetRadioMetadataApi, args: str | tuple[str] = ()):
        """Create an internet radio player"""
        args += '--input-repeat=-1'
        super().__init__(media_source, args)
        self.metadata_api = metadata_api

    @property
    def now_playing(self):
        """Get information about what song is playing now"""
        return self.metadata_api.now_playing
