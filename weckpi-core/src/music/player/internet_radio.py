"""A player for internet radio with integration for internet radio station metadata"""
import logging

from music.metadata import InternetRadioMetadataApi, NowPlaying
from music.player.base_player import BasePlayer, add_argument

logger = logging.getLogger('weckpi.music.player')


class InternetRadioPlayer(BasePlayer):
    """A player for internet radio with integration for internet radio station metadata"""
    metadata_api: InternetRadioMetadataApi

    def __init__(self, media_source: str, metadata_api: InternetRadioMetadataApi, *args: str):
        """
        A player for internet radio with integration for internet radio station metadata

        :param media_source: The media source.
        Can be a URL to a local / remote file in a format that is supported by vlc.
        :param now_playing: Information about what this player's media is.
        Since the media is static (only one source), the information will also be.
        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        args = add_argument(args, '--input-repeat=-1')
        super().__init__(*args)

        self.player = self.instance.media_player_new()
        self.set_media(media_source, metadata_api)

    def set_media(self, media_source: str, metadata_api: InternetRadioMetadataApi):
        """Set the media source"""
        was_playing = self.player.is_playing()

        self.media = self.instance.media_new(media_source)
        self.player.set_media(self.media)
        self.media_source = media_source
        self.metadata_api = metadata_api

        if was_playing:
            self.play()

    def next(self) -> None:
        """Jump to the next item in the playlist"""
        logger.warning('Next is not supported for single media types')

    def previous(self) -> None:
        """Jump to the previous item in the playlist"""
        logger.warning('Previous is not supported for single media types')

    @property
    def now_playing(self) -> NowPlaying:
        """Get information about the song that is playing now"""
        return self.metadata_api.now_playing
