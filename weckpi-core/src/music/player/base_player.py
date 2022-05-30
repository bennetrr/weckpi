"""The base for a vlc player"""
import vlc


class BasePlayer:
    """
    The base for a vlc player.

    This class is an abstract class, do not instantiate it directly!
    """
    instance: vlc.Instance
    player: vlc.MediaListPlayer | vlc.MediaPlayer
    media: vlc.MediaList | vlc.Media

    def __init__(self, args: str | tuple[str] = ()):
        """
        Initialize the player

        :param args: Command line arguments for vlc
        """
        self.instance = vlc.Instance(args)
        self.volume = 1

    def play(self) -> None:
        """Start the playback of the media"""
        self.player.play()

    def pause(self) -> None:
        """Pause the playback of the media"""
        self.player.pause()

    def stop(self) -> None:
        """Stop the playback of the media and reset the media"""
        self.player.stop()

    def next(self) -> None:
        """Next item in the playlist"""

    def previous(self) -> None:
        """Previous item in the playlist"""

    @property
    def volume(self) -> int:
        """
        Get the volume of the player

        :return: The volume of the player
        """
        return self.player.audio_get_volume()

    @volume.setter
    def volume(self, volume) -> None:
        """
        Set the volume of the player

        :param volume: The volume in percent (0 = mute, 100 = 0dB)
        :raises ValueError: If the given volume is out of range
        """
        if volume < 0 or volume > 100:
            raise ValueError(f'The volume is out of range (0≰{volume}≰100)')
        self.player.audio_set_volume(volume)
