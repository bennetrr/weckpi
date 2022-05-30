"""Tools for working with the metadata of laut.fm"""
import requests

from music.metadata import NowPlaying
from music.metadata import InternetRadioMetadataApi


class LautFmMetadataApi(InternetRadioMetadataApi):
    """A class to interact with the laut.fm metadata API"""
    station_name: str
    _station_image: str = None

    def __init__(self, station_name: str):
        """
        A class to interact with the laut.fm metadata API

        :param station_name: The name of the station
        """
        self.station_name = station_name

    @property
    def now_playing(self) -> NowPlaying:
        """Get information about what song is playing now"""
        with requests.get(f'https://api.laut.fm/station/{self.station_name}/current_song') as res:
            res.raise_for_status()
            json = res.json()

        title = json['title']
        artist = json['artist']['name']
        album = json['album']
        cover = self.station_image

        return NowPlaying(title, artist, album, cover)

    @property
    def station_image(self) -> str:
        """Get the image of the radio station"""
        if self._station_image is None:
            with requests.get(f'https://api.laut.fm/station/{self.station_name}') as res:
                res.raise_for_status()
                json = res.json()

            self._station_image = json['images']['station']
        return self._station_image

