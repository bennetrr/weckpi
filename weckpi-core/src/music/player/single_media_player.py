"""A player for a single media source"""
from music.player.base_player import BasePlayer
from pathlib import Path
import logging

logger = logging.getLogger('weckpi.music.player')


class SingleMediaPlayer(BasePlayer):
    """A player for a single media source"""

    def __init__(self, media_source: str | Path, args: str | tuple[str] = ()):
        """
        Initialize the player

        :param args: Command line arguments for vlc
        :param media_source: The media source
        """
        super().__init__(args)
        self.player = self.instance.media_player_new()
        self.set_media(media_source)

    def set_media(self, media_source: str | Path):
        """Set the media source"""
        self.media = self.instance.media_new(media_source)
        self.player.set_media(self.media)

    def next(self) -> None:
        """Next item in the playlist"""
        logger.warning('Next is not supported for single media types')

    def previous(self) -> None:
        """Previous item in the playlist"""
        logger.warning('Previous is not supported for single media types')