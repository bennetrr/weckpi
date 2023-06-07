from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type

import weckpi.api.music as wpm


@dataclass(frozen=True)
class MediaProviderRegistration:
    name: str
    cls: Type[wpm.MediaProvider]
    _instances: dict[str, wpm.MediaProvider] = field(default_factory=dict, init=False)
    needs_login: bool
    has_search: bool
    has_explore: bool

    def register_instance(self, name: str, obj: wpm.MediaProvider):
        if name in self._instances:
            raise RuntimeError(f'The media provider instance {name} is already registered!')
        self._instances[name] = obj

    def get_instance(self, name: str) -> wpm.MediaProvider:
        if name not in self._instances:
            raise KeyError(f'The media provider instance {name} is not registered!')
        return self._instances[name]


@dataclass(frozen=True)
class MediaPlayerRegistration:
    name: str
    cls: Type[wpm.MediaPlayer]
    _instances: dict[str, wpm.MediaPlayer] = field(default_factory=dict, init=False)

    def register_instance(self, name: str, obj: wpm.MediaPlayer):
        if name in self._instances:
            raise RuntimeError(f'The media provider instance {name} is already registered!')
        self._instances[name] = obj

    def get_instance(self, name: str) -> wpm.MediaPlayer:
        if name not in self._instances:
            raise KeyError(f'The media provider instance {name} is not registered!')
        return self._instances[name]
