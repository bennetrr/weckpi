"""A player for internet radio with integration for internet radio station metadata"""
import logging
from typing import Optional

from music.metadata import InternetRadioMetadataApi, NowPlaying
from music.players.bases.single_media_base_player import SingleMediaBasePlayer
from music.utils import add_vlc_argument

logger = logging.getLogger(f'weckpi.{__name__}')


class InternetRadioPlayer(SingleMediaBasePlayer):
    """A player for internet radio with integration for internet radio station metadata"""
    metadata_api: InternetRadioMetadataApi

    def __init__(self, media_source: str, metadata_api: InternetRadioMetadataApi, *args: str):
        """
        A player for internet radio with integration for internet radio station metadata

        :param media_source: The media source.
        Can be a URL to a local / remote file in a format that is supported by vlc.
        :param metadata_api: An object of the model for the internet radio provider's metadata API.
        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        args = add_vlc_argument(args, '--input-repeat=-1')
        super().__init__(*args)
        self.set_media(media_source, metadata_api)

    def set_media(self, media_source: str, metadata_api: InternetRadioMetadataApi) -> None:
        """Set the media source"""
        was_playing = self.is_playing

        self.media = self.instance.media_new(media_source)
        self.player.set_media(self.media)
        self.media_source = media_source
        self.metadata_api = metadata_api

        if was_playing:
            self.play()

    @property
    def now_playing(self) -> Optional[NowPlaying]:
        """Get information about the song that is playing now"""
        if self.is_playing:
            return self.metadata_api.now_playing
        return None
