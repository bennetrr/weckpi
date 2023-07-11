"""Media playback device using the MPV media player."""
from __future__ import annotations

import logging
import random
from collections.abc import Callable
from typing import Sequence

import mpv

from weckpi.api.music import MediaPlayer, MediaResource, Metadata
from weckpi.api.plugin_manager import plugin_manager

logger = logging.getLogger(__name__)


class MpvMediaPlayer(MediaPlayer):
    """
    Playback device using the MPV media player.
    """
    _player: mpv.MPV
    _block_on_idle_status_change: bool

    _queue: list[str]
    _queue_metadata: list[Metadata]
    _original_queue: list[int]

    _current_queue_index: int
    _current_item: MediaResource | None

    _shuffle: bool
    _repeat: bool

    _on_queue_position_change: Callable[[int], None] | None
    _on_position_change: Callable[[float], None] | None

    def __init__(self):
        logger.debug('MPV version: %s', mpv.MPV_VERSION)

        self._player = mpv.MPV()
        self._block_on_idle_status_change = True

        self._queue = []
        self._queue_metadata = []
        # This list contains the current index (index) and the original index (value) of the queue items.
        self._original_queue = []

        self._current_queue_index = 0
        self._current_item = None

        self._shuffle = False
        self._repeat = False

        self._on_queue_position_change = None
        self._on_position_change = None

        # Event handlers
        def on_idle_status_change(_, is_idle: bool):
            """Event handler for the core_idle property."""
            print(f'{is_idle=}{", blocked" if self._block_on_idle_status_change or not is_idle else ""}')

            if not is_idle:
                if self._on_queue_position_change is not None:
                    self._on_queue_position_change(self._current_queue_index)
                return

            if self._block_on_idle_status_change:
                self._block_on_idle_status_change = False
                return

            if self._current_queue_index + 1 >= len(self._queue):
                if not self._repeat:
                    return
                self._current_queue_index = 0
            else:
                self._current_queue_index += 1

            self._play_current_item()
            print('Changed to next item in queue')

        self._player.observe_property('core-idle', on_idle_status_change)

        def on_time_pos_change(_, _2):
            if self._on_position_change is None:
                return
            self._on_position_change(self.position)

        self._player.observe_property('time-pos', on_time_pos_change)

    @staticmethod
    def _get_plugin_instance(mrid: str):
        """Get the plugin instance for the given MRID."""
        provider_id, provider_instance_id, _ = mrid.split(':', 2)

        return plugin_manager().get_media_provider(provider_id).get_instance(provider_instance_id)

    def _play_current_item(self):
        """Get the media resource information for the MRID."""
        mrid = self._queue[self._current_queue_index]
        provider_id, provider_instance_id, _ = mrid.split(':', 2)

        self._current_item = self._get_plugin_instance(mrid).resolve_mrid(mrid)

        self._player.play(self._current_item.uri)

    def play(self):
        """Start the playback."""
        if not self._player.core_idle:
            return

        if self._player.pause:
            self._player.pause = False
        else:
            self._play_current_item()

    def pause(self):
        """Pause the playback."""
        if self._player.core_idle:
            return

        self._block_on_idle_status_change = True
        self._player.pause = True

    def stop(self):
        """Stop the playback and reset the queue."""
        if not self._player.core_idle:
            self._player.stop()
            self._current_queue_index = 0

            if self._shuffle:
                random.shuffle(self._queue)

    def next(self):
        """Jump to the next element in the queue."""
        if self._current_queue_index + 1 >= len(self._queue):
            if not self._repeat:
                raise IndexError("There are no items left in the queue!")

            self._current_queue_index = 0
        else:
            self._current_queue_index += 1

        self._block_on_idle_status_change = True
        self._play_current_item()

    def previous(self):
        """Jump to the previous element in the queue."""
        if self._current_queue_index <= 0:
            if not self._repeat:
                raise IndexError("You are already at the beginning of the queue!")

            self._current_queue_index = len(self._queue) - 1
        else:
            self._current_queue_index -= 1

        self._block_on_idle_status_change = True
        self._play_current_item()

    def _add_item(self, mrid: str):
        """Add one item at the end of the queue."""
        self._queue.append(mrid)
        self._queue_metadata.append(self._get_plugin_instance(mrid).get_metadata(mrid))
        self._original_queue.append(len(self._original_queue))

    def add_media(self, mrid: str | Sequence[str]):
        """Add one or multiple items at the end of the queue."""
        if isinstance(mrid, str):
            self._add_item(mrid)
        else:
            [self._add_item(item) for item in mrid]

    def remove_media(self, index: int):
        """Remove the item with the given index from the queue."""
        if 0 >= index >= len(self._queue):
            raise IndexError('The index has to be between 0 and the length of the queue!')

        if self._current_queue_index == index:
            self._block_on_idle_status_change = True
            self.next()

        self._queue.pop(index)
        self._original_queue.remove(index)

    @property
    def queue_position(self) -> int:
        """Get the index of the current queue item."""
        return self._current_queue_index

    @queue_position.setter
    def queue_position(self, value: int):
        """Set the index of the current queue item."""
        if 0 > value >= len(self._queue):
            raise IndexError('The index has to be between 0 and the length of the queue!')

        self._current_queue_index = value

        self._block_on_idle_status_change = True
        self._play_current_item()

    @property
    def queue(self) -> list[Metadata]:
        """Get the queue."""
        return self._queue_metadata.copy()

    def clear_queue(self):
        """Remove all items from the queue."""
        self.stop()
        self._queue.clear()
        self._queue_metadata.clear()
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
        if self._player.time_pos is None:
            return 0
        return self._player.time_pos / 60

    @position.setter
    def position(self, value: float):
        """
        Set the position of the player in the current queue item.

        :param value: The position in minutes.
        """
        if 0.0 > value > self._player.duration:
            raise ValueError('The position must be between 0.0 and the duration of the current queue item!')

        self._block_on_idle_status_change = True
        self._player.time_pos = value * 60

    @property
    def shuffle(self) -> bool:
        """Get whether the queue is shuffled."""
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value: bool):
        """Set whether the queue is shuffled."""
        if value:
            self._original_queue.remove(self._current_queue_index)
            random.shuffle(self._original_queue)
            self._original_queue.insert(0, self._current_queue_index)

            self._queue = [self._queue[i] for i in self._original_queue]
            self._queue_metadata = [self._queue_metadata[i] for i in self._original_queue]

            self._current_queue_index = 0
        else:
            new_queue: list[str] = [None] * len(self._queue)
            new_queue_metadata: list[Metadata] = [None] * len(self._queue_metadata)

            for current_index, original_index in enumerate(self._original_queue):
                new_queue[original_index] = self._queue[current_index]
                new_queue_metadata[original_index] = self._queue_metadata[current_index]

            self._queue = new_queue
            self._queue_metadata = new_queue_metadata
            self._original_queue.sort()

            self._current_queue_index = self._original_queue[self._current_queue_index]

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
        if self._player.duration is None:
            return 0
        return self._player.duration / 60

    def __repr__(self):
        return f'Playing element {self._current_queue_index + 1} of {len(self._queue)}: {self.metadata}'

    def set_on_queue_position_change(self, function: Callable[[int], None]):
        """Set a function that is executed whenever the queue position changes."""
        self._on_queue_position_change = function

    def set_on_position_change(self, function: Callable[[float], None]):
        """Set a function that is executed whenever the position changes."""
        self._on_position_change = function
