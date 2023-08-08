"""Media player using libmpv and the package `python-mpv <https://github.com/jaseg/python-mpv>`_."""
from __future__ import annotations

import logging
import random
from collections.abc import Callable
from typing import Sequence

import mpv

from weckpi.api.music import MediaNotAvailableException, MediaPlayer, MediaResource, Metadata
from weckpi.api.plugin_manager import plugin_manager
from weckpi.api.utilities import property_setter_only

logger = logging.getLogger(__name__)

# TODO Add unit tests


class Mpv(MediaPlayer):
    """Media player using libmpv."""
    _player: mpv.MPV
    _block_idle_status_event: bool

    _queue: list[str]
    _metadata_queue: list[Metadata]
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
        self._block_idle_status_event = True

        self._queue = []
        self._metadata_queue = []
        # This list contains the current index (index) and the original index (value) of the queue items.
        self._original_queue = []

        self._current_queue_index = 0
        self._current_item = None

        self._shuffle = False
        self._repeat = False

        self._on_queue_position_change = None
        self._on_position_change = None

        # Event handlers
        def on_idle_status_change(_, idle: bool):
            """Event handler for the core_idle property."""
            if not idle:
                if self._on_queue_position_change is None:
                    return

                self._on_queue_position_change(self._current_queue_index)
                return

            if self._block_idle_status_event:
                self._block_idle_status_event = False
                return

            if self._current_queue_index + 1 >= len(self._queue):
                if not self._repeat:
                    return
                self._current_queue_index = 0
            else:
                self._current_queue_index += 1

            self._play_current_item()

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
        """Get the media resource information for the MRID and play the item."""
        mrid = self._queue[self._current_queue_index]

        try:
            self._current_item = self._get_plugin_instance(mrid).resolve_mrid(mrid)
        except MediaNotAvailableException:
            self.next()

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

        self._block_idle_status_event = True
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

        self._block_idle_status_event = True
        self._play_current_item()

    def previous(self):
        """Jump to the previous element in the queue."""
        if self._current_queue_index <= 0:
            if not self._repeat:
                raise IndexError("You are already at the beginning of the queue!")

            self._current_queue_index = len(self._queue) - 1
        else:
            self._current_queue_index -= 1

        self._block_idle_status_event = True
        self._play_current_item()

    def add_item(self, mrid: str):
        """Add one item at the end of the queue."""
        self._queue.append(mrid)
        self._metadata_queue.append(self._get_plugin_instance(mrid).get_metadata(mrid))
        self._original_queue.append(len(self._original_queue))

    def add_items(self, mrids: Sequence[str]):
        """Add multiple items at the end of the queue."""
        for mrid in mrids:
            self.add_item(mrid)

    def remove_item(self, index: int):
        """
        Remove the item with the given index from the queue.

        :raises IndexError: When the given index is not in the queue.
        """
        if 0 >= index >= len(self._queue):
            raise IndexError('The index has to be between 0 and the length of the queue!')

        if self._current_queue_index == index:
            self._block_idle_status_event = True
            self.next()

        self._queue.pop(index)
        self._original_queue.remove(index)

    @property
    def queue_position(self) -> int:
        """Get the index of the current queue item."""
        return self._current_queue_index

    @queue_position.setter
    def queue_position(self, value: int):
        """
        Set the index of the current queue item.

        :raises IndexError: When the given index is not in the queue.
        """
        if 0 > value >= len(self._queue):
            raise IndexError('The index has to be between 0 and the length of the queue!')

        self._current_queue_index = value

        self._block_idle_status_event = True
        self._play_current_item()

    @property
    def queue(self) -> list[Metadata]:
        """Get the metadata of every queue item."""
        return self._metadata_queue.copy()

    def clear_queue(self):
        """Remove all items from the queue."""
        self.stop()
        self._queue.clear()
        self._metadata_queue.clear()
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
        :raises ValueError: When the value is not in the right range.
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
        if 0.0 > value > self.metadata.duration:
            raise ValueError('The position must be between 0.0 and the duration of the current queue item!')

        self._block_idle_status_event = True
        self._player.time_pos = value * 60

    @property
    def shuffle(self) -> bool:
        """Get whether the queue is shuffled."""
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value: bool):
        """(Un-)shuffle the queue."""
        if value:
            # TODO Shuffle all items if the playlist wasn't played yet
            self._original_queue.remove(self._current_queue_index)
            random.shuffle(self._original_queue)
            self._original_queue.insert(0, self._current_queue_index)

            self._queue = [self._queue[i] for i in self._original_queue]
            self._metadata_queue = [self._metadata_queue[i] for i in self._original_queue]

            self._current_queue_index = 0
        else:
            new_queue: list[str | None] = [None] * len(self._queue)
            new_queue_metadata: list[Metadata | None] = [None] * len(self._metadata_queue)

            for current_index, original_index in enumerate(self._original_queue):
                new_queue[original_index] = self._queue[current_index]
                new_queue_metadata[original_index] = self._metadata_queue[current_index]

            self._queue = new_queue
            self._metadata_queue = new_queue_metadata
            self._original_queue.sort()

            self._current_queue_index = self._original_queue[self._current_queue_index]

        self._shuffle = value

    @property
    def repeat(self) -> bool:
        """Get whether the queue is played from the beginning after reaching the end."""
        return self._repeat

    @repeat.setter
    def repeat(self, value: bool):
        """Set whether the queue is played from the beginning after reaching the end."""
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
        """Get whether the media ressource is continuous (should be ``true`` for internet radio and similar)."""
        return self._current_item.continuous

    @property_setter_only
    def on_queue_position_change(self, value: Callable[[int], None]):
        """
        Register a function that is executed whenever the queue position changes.

        :param value: A function that takes one int argument for the new queue position.
        """
        self._on_queue_position_change = value

    @property_setter_only
    def on_position_change(self, value: Callable[[float], None]):
        """
        Register a function that is executed whenever the position changes.

        :param value: A function that takes one float argument for the new position.
        """
        self._on_position_change = value

    def __repr__(self):
        return f'Playing element {self._current_queue_index + 1} of {len(self._queue)}: {self.metadata}'
