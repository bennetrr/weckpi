"""Media playback device using the MPV media player."""
from __future__ import annotations

import logging
import random
from typing import Sequence

import mpv

from weckpi.api.music import MediaPlayer, MediaResource, Metadata, MRID

logger = logging.getLogger(__name__)


class MpvMediaPlayer(MediaPlayer):
    """
    Playback device using the MPV media player.
    """
    _player: mpv.MPV
    _queue: list[MRID]
    _original_queue: list[MRID]
    _current_queue_index: int
    _current_item: MediaResource | None
    _shuffle: bool
    _repeat: bool

    def __init__(self):
        logger.debug('MPV version: %s', mpv.MPV_VERSION)

        self._player = mpv.MPV()
        self._queue = []
        self._current_queue_index = 0
        self._current_item = None
        self._shuffle = False
        self._repeat = False

        # Event handlers
        # noinspection PyUnusedLocal
        # pylint: disable=unused-argument
        def on_idle_status_change(prop: str, core_idle: bool):
            if not core_idle:
                return

            if self._current_queue_index + 1 >= len(self._queue):
                if not self._repeat:
                    return
                self._current_queue_index = 0

            self._current_queue_index += 1
            self._play_current_item()

        self._player.observe_property('core_idle', on_idle_status_change)

    def _play_current_item(self):
        """Get the media resource information for the MRID"""
        mrid = self._queue[self._current_queue_index]
        # TODO MRID resolution
        media_resource = MediaResource(None, mrid, None, None, None)
        self._player.play(media_resource.uri)

    def play(self):
        """Start the playback."""
        if self._player.pause:
            self._player.pause = False
        else:
            self._play_current_item()

    def pause(self):
        """Pause the playback."""
        if not self._player.core_idle:
            self._player.pause = True

    def stop(self):
        """Stop the playback and reset the queue."""
        if not self._player.core_idle:
            self._player.stop()
            self._current_queue_index = 0
            self._queue = self._original_queue.copy()

    def next(self):
        """Jump to the next element in the queue."""
        if self._current_queue_index + 1 >= len(self._queue):
            raise IndexError("There are no items left in the queue!")

        self._current_queue_index += 1
        self._play_current_item()

    def previous(self):
        """Jump to the previous element in the queue."""
        if self._current_queue_index <= 0:
            raise IndexError("You are already at the beginning of the queue!")

        self._current_queue_index -= 1
        self._play_current_item()

    def add_media(self, media: MRID | Sequence[MRID]):
        """Add one or multiple items at the end of the queue."""
        if isinstance(media, Sequence):
            self._queue.extend(media)
            self._original_queue.extend(media)
        else:
            self._queue.append(media)
            self._original_queue.append(media)

    def remove_media(self, index: int):
        """Remove the item with the given index from the queue."""
        if 0 >= index >= len(self._queue):
            raise IndexError('The index has to be between 0 and the length of the queue!')

        if self._current_queue_index == index:
            self.next()

        self._queue.pop(index)
        self._original_queue.pop(index)

    @property
    def queue_position(self) -> int:
        """Get the index of the current queue item."""
        return self._current_queue_index

    @queue_position.setter
    def queue_position(self, value: int):
        """Set the index of the current queue item."""
        if 0 >= value >= len(self._queue):
            raise IndexError('The index has to be between 0 and the length of the queue!')

        self._current_queue_index = value
        self._play_current_item()

    @property
    def queue(self) -> list[MRID]:
        """Get the queue."""
        return self._queue.copy()

    def clear_queue(self):
        """Remove all items from the queue."""
        self._queue.clear()
        self._original_queue.clear()

    @property
    def volume(self) -> float:
        """
        Get the volume.

        :return: The volume in percent (value between 0.0 and 100.0).
        """
        return self._player.volume

    @volume.setter
    def volume(self, value: float):
        """
        Set the volume.

        :param value: The volume in percent (value between 0.0 and 100.0).
        """
        if 0.0 >= value >= 100.0:
            raise ValueError('Volume must be between 0.0 and 100.0!')

        self._player.volume = value

    @property
    def position(self) -> float:
        """
        Get the position of the player in the current queue item.

        :return: The position in minutes.
        """
        return self._player.time_pos / 60

    @position.setter
    def position(self, value: float):
        """
        Set the position of the player in the current queue item.

        :param value: The position in minutes.
        """
        self._player.time_pos = value * 60

    @property
    def shuffle(self) -> bool:
        """Get whether the queue is shuffled."""
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value: bool):
        """Set whether the queue is shuffled."""
        if value:
            # Shuffle the queue and put the current item at the first index
            current_mrid = self._queue.pop(self._current_queue_index)
            random.shuffle(self._queue)
            self._queue.insert(0, current_mrid)
            self._current_queue_index = 0
        else:
            # Reset the playlist order and set the index to the right item
            self._queue = self._original_queue.copy()
            self._current_queue_index = self._queue.index(self._current_item.mrid)

        self._shuffle = value

    @property
    def repeat(self) -> bool:
        """Get whether the queue is repeated."""
        return self._repeat

    @repeat.setter
    def repeat(self, value: bool):
        """Set whether the queue is repeated."""
        self._repeat = value

    @property
    def metadata(self) -> Metadata:
        """Get the metadata of the current queue item."""
        # Only fetch the metadata every time from the media provider if the resource is continuous
        if self._current_item.continuous:
            return self._current_item.provider.get_metadata(self._current_item.mrid)
        return self._current_item.metadata

    @property
    def continuous(self) -> bool:
        """Get whether the media ressource is continuous."""
        return self._current_item.continuous

    @property
    def duration(self) -> float:
        """
        Get the duration of the current queue item.

        :return: The duration in minutes.
        """
        return self._player.duration / 60
