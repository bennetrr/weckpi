"""Tools for working with the metadata of laut.fm radio stations"""
import requests

from music.metadata.internet_radio_metadata.internet_radio_metadata import InternetRadioMetadataApi
from music.metadata.now_playing import NowPlaying


class LautFmMetadataApi(InternetRadioMetadataApi):
    """A model for the laut.fm metadata API"""
    station_name: str
    _station_image: str = None

    def __init__(self, station_name: str):
        """
        A model for the laut.fm metadata API

        :param station_name: The name of the radio station to get the metadata for
        """
        self.station_name = station_name

    @property
    def now_playing(self) -> NowPlaying:
        """Get information about the song that is playing now"""
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
        """Get the image of the station"""
        if self._station_image is None:
            with requests.get(f'https://api.laut.fm/station/{self.station_name}') as res:
                res.raise_for_status()
                json = res.json()

            self._station_image = json['images']['station']
        return self._station_image
