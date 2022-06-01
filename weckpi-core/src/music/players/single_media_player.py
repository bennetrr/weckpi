"""A player for a single media source"""
import logging
from pathlib import Path
from typing import Optional

from music.metadata import NowPlaying
from music.players.bases.single_media_base_player import SingleMediaBasePlayer

logger = logging.getLogger(f'weckpi.{__name__}')


class SingleMediaPlayer(SingleMediaBasePlayer):
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
        self.set_media(media_source, now_playing)

    def set_media(self, media_source: str | Path, now_playing: NowPlaying) -> None:
        """Set the media source"""
        was_playing = self.is_playing

        self.media = self.instance.media_new(media_source)
        self.player.set_media(self.media)
        self.media_source = media_source
        self._now_playing = now_playing

        if was_playing:
            self.play()

    @property
    def now_playing(self) -> Optional[NowPlaying]:
        """Get information about the song that is playing now"""
        if self.is_playing:
            return self._now_playing
        return None
