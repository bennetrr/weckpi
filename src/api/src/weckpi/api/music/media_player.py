"""Base class for all media players."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence

import weckpi.api.music as wpm
from weckpi.api.utilities import property_setter_only


class MediaPlayer(ABC):
    """
    Base class for all media players.

    A media player class contains the code for playing media files that are provided by the media providers.
    Subclasses of this handle common functions like play, pause, queue management, volume control and many more.

    It's really important to resolve the MRIDs only when the resource should be played,
    and not when it is added to the queue.
    This is because the URLs produced by streaming services are usually expired after a given time.
    """

    @abstractmethod
    def play(self) -> None:
        """Start the playback."""

    @abstractmethod
    def pause(self) -> None:
        """Pause the playback."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the playback and reset the queue."""

    @abstractmethod
    def next(self) -> None:
        """
        Jump to the next element in the queue.

        :raises IndexError: When the last item in the queue is already playing.
        """

    @abstractmethod
    def previous(self) -> None:
        """
        Jump to the previous element in the queue.

        :raises IndexError: When the first item in the queue is already playing.
        """

    @abstractmethod
    def add_item(self, mrid: str) -> None:
        """Add one item at the end of the queue."""

    @abstractmethod
    def add_items(self, mrids: Sequence[str]) -> None:
        """Add multiple items at the end of the queue."""

    @abstractmethod
    def remove_item(self, index: int) -> None:
        """
        Remove the item with the given index from the queue.

        :raises IndexError: When the given index is not in the queue.
        """

    @property
    @abstractmethod
    def queue_position(self) -> int:
        """Get the index of the current queue item."""

    @queue_position.setter
    @abstractmethod
    def queue_position(self, value: int):
        """
        Set the index of the current queue item.

        :raises IndexError: When the given index is not in the queue.
        """

    @property
    @abstractmethod
    def queue(self) -> list[wpm.Metadata]:
        """Get the metadata of every queue item."""

    @abstractmethod
    def clear_queue(self) -> None:
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
    def volume(self, value: float) -> None:
        """
        Set the volume.

        :param value: The volume in percent (value between 0.0 and 100.0).
        :raises ValueError: When the given volume is not in the right range.
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
    def position(self, value: float) -> None:
        """
        Set the position of the player in the current queue item.

        :param value: The position in minutes.
        :raises ValueError: When the given position is not in the current queue item.
        """

    @property
    @abstractmethod
    def shuffle(self) -> bool:
        """Get whether the queue is shuffled."""

    @shuffle.setter
    @abstractmethod
    def shuffle(self, value: bool) -> None:
        """(Un-)shuffle the queue."""

    @property
    @abstractmethod
    def repeat(self) -> bool:
        """Get whether the queue is played from the beginning after reaching the end."""

    @repeat.setter
    @abstractmethod
    def repeat(self, value: bool) -> None:
        """Set whether the queue is played from the beginning after reaching the end."""

    @property
    @abstractmethod
    def metadata(self) -> wpm.Metadata:
        """Get the metadata of the current queue item."""

    @property
    @abstractmethod
    def continuous(self) -> bool:
        """Get whether the media ressource is continuous (should be ``true`` for internet radio and similar)."""

    @property_setter_only
    @abstractmethod
    def on_queue_position_change(self, value: Callable[[int], None]) -> None:
        """
        Register a function that is executed whenever the queue position changes.

        :param value: A function that takes one int argument for the new queue position.
        """

    @property_setter_only
    @abstractmethod
    def on_position_change(self, value: Callable[[float], None]) -> None:
        """
        Register a function that is executed whenever the position changes.

        :param value: A function that takes one float argument for the new position.
        """
