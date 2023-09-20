"""The root data structure for the configuration."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from weckpi.api.config.alarm_config import AlarmConfig
from weckpi.api.config.music_config import MusicConfig


@dataclass
class WeckPiConfig:
    """
    The root config model.

    :var music: Config for the music system.
    """
    _config_file: Path
    music: MusicConfig
    alarm: AlarmConfig

    @classmethod
    def from_json_file(cls, config_file: Path) -> WeckPiConfig:
        """Create a WeckPiConfig object from a json file."""
        with config_file.open('r', encoding='utf-8') as config_stream:
            config_json: dict = json.load(config_stream)

        return cls(
            config_file,
            MusicConfig.from_json(config_json['music']),
            AlarmConfig.from_json(config_json['alarm'])
        )

    def to_json(self) -> dict:
        """Save this WeckPiConfig object to a json file."""
        return {
            'music': self.music.to_json(),
            'alarm': self.alarm.to_json()
        }

    def flush(self) -> None:
        """Flush this WeckPiConfig object to the config file."""
        with self._config_file.open('w', encoding='utf-8') as config_stream:
            json.dump(self.to_json(), config_stream, indent=4)


_config_instance: WeckPiConfig | None = None


def config(config_file: Path = None) -> WeckPiConfig:
    """Get the configuration object."""
    global _config_instance
    if _config_instance is None:
        _config_instance = WeckPiConfig.from_json_file(config_file)
    return _config_instance
