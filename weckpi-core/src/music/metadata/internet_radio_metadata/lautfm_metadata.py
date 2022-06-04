"""Tools for working with the metadata of Laut.FM radio stations"""
import time
import logging
import requests

from music.metadata.internet_radio_metadata.internet_radio_metadata import InternetRadioMetadataApi
from music.metadata.now_playing import NowPlaying


logger = logging.getLogger(f'weckpi.{__name__}')


class LautFmMetadataApi(InternetRadioMetadataApi):
    """A model for the Laut.FM metadata API"""
    station_name: str
    _station_image: str = None
    _now_playing: NowPlaying
    _song_ends: float = 0

    def __init__(self, station_name: str):
        """
        A model for the Laut.FM metadata API

        :param station_name: The name of the radio station to get the metadata for
        """
        self.station_name = station_name

    @property
    def now_playing(self) -> NowPlaying:
        """Get information about the song that is playing now"""
        # Only fetch the data if it is not up-to-date
        if time.time() > self._song_ends:
            with requests.get(f'https://api.laut.fm/station/{self.station_name}/current_song') as res:
                res.raise_for_status()
                json = res.json()

            title = json['title']
            artist = json['artist']['name']
            album = json['album']
            cover = self.station_image
            self._song_ends = time.mktime(time.strptime(json['ends_at'], '%Y-%m-%d %H:%M:%S %z'))
            self._now_playing = NowPlaying(title, artist, album, cover)
        else:
            logger.info('Laut.FM metadata should be up-to-date, using cached data')
        return self._now_playing

    @property
    def station_image(self) -> str:
        """Get the image of the station"""
        if self._station_image is None:
            with requests.get(f'https://api.laut.fm/station/{self.station_name}') as res:
                res.raise_for_status()
                json = res.json()

            self._station_image = json['images']['station']
        return self._station_image

    @property
    def song_ends(self) -> float:
        """Get the time when the next song is played"""
        return self._song_ends
