"""Tools for working with internet radio metadata"""
from music.metadata import NowPlaying


class InternetRadioMetadataApi:
    """A model for the metadata API for internet radio providers"""

    @property
    def now_playing(self) -> NowPlaying:
        """Get information about what song is playing now"""
        return NowPlaying('', '', '', self.station_image)

    @property
    def station_image(self) -> str:
        """Get the image of the station"""
        return ''
