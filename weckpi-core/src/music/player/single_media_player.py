"""A player for a single media source"""
import logging
from pathlib import Path

from music.metadata import NowPlaying
from music.player.base_player import BasePlayer

logger = logging.getLogger(f'weckpi.{__name__}')


class SingleMediaPlayer(BasePlayer):
    """A player for a single media source"""
    _now_playing: NowPlaying

    def __init__(self, media_source: str | Path, now_playing: NowPlaying, *args: str):
        """
        A player for a single media source

        :param media_source: The media source.
        Can be a URL to a local / remote file in a format that is supported by vlc.
        :param now_playing: Information about what this player's media is.
        Since the media is static (only one source), the information will also be.
        :param args: Arguments to pass to vlc.
        For possible arguments, see the help of the vlc cli.
        """
        super().__init__(*args)
        self.player = self.instance.media_player_new()
        self.set_media(media_source, now_playing)

    def set_media(self, media_source: str | Path, now_playing: NowPlaying):
        """Set the media source"""
        was_playing = self.player.is_playing()

        self.media = self.instance.media_new(media_source)
        self.player.set_media(self.media)
        self.media_source = media_source
        self._now_playing = now_playing

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
        return self._now_playing
