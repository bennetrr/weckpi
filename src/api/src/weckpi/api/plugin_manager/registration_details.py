"""Details for classes registered in the plugin manager."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type

import weckpi.api.music as wpm


@dataclass(frozen=True)
class MediaProviderRegistration:
    """Details for media providers registered in the plugin manager."""
    name: str
    cls: Type[wpm.MediaProvider]
    _instances: dict[str, wpm.MediaProvider] = field(default_factory=dict, init=False)
    needs_login: bool
    has_search: bool
    has_explore: bool

    def register_instance(self, name: str, obj: wpm.MediaProvider):
        """Register a media provider instance to the plugin manager."""
        if name in self._instances:
            raise RuntimeError(f'The media provider instance {name} is already registered!')
        self._instances[name] = obj

    def get_instance(self, name: str) -> wpm.MediaProvider:
        """Get a registered media provider instance from the plugin manager."""
        if name not in self._instances:
            raise KeyError(f'The media provider instance {name} is not registered!')
        return self._instances[name]


@dataclass(frozen=True)
class MediaPlayerRegistration:
    """Details for media players registered in the plugin manager."""
    name: str
    cls: Type[wpm.MediaPlayer]
    _instances: dict[str, wpm.MediaPlayer] = field(default_factory=dict, init=False)

    def register_instance(self, name: str, obj: wpm.MediaPlayer):
        """Register a media player instance to the plugin manager."""
        if name in self._instances:
            raise RuntimeError(f'The media provider instance {name} is already registered!')
        self._instances[name] = obj

    def get_instance(self, name: str) -> wpm.MediaPlayer:
        """Get a registered media player instance from the plugin manager."""
        if name not in self._instances:
            raise KeyError(f'The media provider instance {name} is not registered!')
        return self._instances[name]
