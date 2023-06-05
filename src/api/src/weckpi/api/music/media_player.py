from __future__ import annotations

from abc import *
from collections.abc import Sequence

import weckpi.api.music as wpm


class MediaPlayer(ABC):
    """
    Interface for all media playback devices.
    """

    @abstractmethod
    def play(self):
        """Start the playback."""

    @abstractmethod
    def pause(self):
        """Pause the playback."""

    @abstractmethod
    def stop(self):
        """Stop the playback and reset the queue."""

    @abstractmethod
    def next(self):
        """Jump to the next element in the queue."""

    @abstractmethod
    def previous(self):
        """Jump to the previous element in the queue."""

    @abstractmethod
    def add_media(self, media: wpm.MediaResource | Sequence[wpm.MediaResource]):
        """Add one or multiple items at the end of the queue."""

    @abstractmethod
    def remove_media(self, index: int):
        """Remove the item with the given index from the queue."""

    @property
    @abstractmethod
    def queue_position(self) -> int:
        """Get the index of the current queue item."""

    @queue_position.setter
    @abstractmethod
    def queue_position(self, value: int):
        """Set the index of the current queue item."""

    @property
    @abstractmethod
    def queue(self) -> Sequence[wpm.MediaResource]:
        """Get the queue."""

    @abstractmethod
    def clear_queue(self):
        """Remove all items from the queue."""

    @property
    @abstractmethod
    def volume(self) -> float:
        """
        Get the volume.

        :return: The volume in percent (value between 0.0 and 100.0).
        """

    @volume.setter
    @abstractmethod
    def volume(self, value: float):
        """
        Set the volume.

        :param value: The volume in percent (value between 0.0 and 100.0).
        """

    @property
    @abstractmethod
    def position(self) -> float:
        """
        Get the position of the player in the current queue item.

        :return: The position in minutes.
        """

    @position.setter
    @abstractmethod
    def position(self, value: float):
        """
        Set the position of the player in the current queue item.

        :param value: The position in minutes.
        """

    @property
    @abstractmethod
    def shuffle(self) -> bool:
        """Get whether the queue is shuffled."""

    @shuffle.setter
    @abstractmethod
    def shuffle(self, value: bool):
        """Set whether the queue is shuffled."""

    @property
    @abstractmethod
    def repeat(self) -> bool:
        """Get whether the queue is repeated."""

    @repeat.setter
    @abstractmethod
    def repeat(self, value: bool):
        """Set whether the queue is repeated."""

    @property
    @abstractmethod
    def metadata(self) -> wpm.Metadata:
        """Get the metadata of the current queue item."""

    @property
    @abstractmethod
    def duration(self) -> float:
        """
        Get the duration of the current queue item.

        :return: The duration in minutes.
        """
