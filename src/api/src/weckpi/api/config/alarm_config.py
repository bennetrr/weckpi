"""All alarm related configuration models."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from typing import Literal


@dataclass
class AlarmConfig:
    """
    The root model for the alarm system config.

    :var monday: Config for the alarm on monday.
    :var tuesday: Config for the alarm on tuesday.
    :var wednesday: Config for the alarm on wednesday.
    :var thursday: Config for the alarm on thursday.
    :var friday: Config for the alarm on friday.
    :var saturday: Config for the alarm on saturday.
    :var sunday: Config for the alarm on sunday.
    """
    monday: AlarmDay
    tuesday: AlarmDay
    wednesday: AlarmDay
    thursday: AlarmDay
    friday: AlarmDay
    saturday: AlarmDay
    sunday: AlarmDay

    def get_alarm_config(self, iso_weekday: Literal[1, 2, 3, 4, 5, 6, 7]) -> AlarmDay:
        """Get the alarm config for the number of the weekday (monday = 1, sunday = 7)."""
        day_mapping = {
            1: 'monday',
            2: 'tuesday',
            3: 'wednesday',
            4: 'thursday',
            5: 'friday',
            6: 'saturday',
            7: 'sunday'
        }
        return getattr(self, day_mapping[iso_weekday])

    @classmethod
    def from_json(cls, config_json: dict) -> AlarmConfig:
        """Create a AlarmConfig object from a dict."""
        return cls(
            AlarmDay.from_json(config_json['monday']),
            AlarmDay.from_json(config_json['tuesday']),
            AlarmDay.from_json(config_json['wednesday']),
            AlarmDay.from_json(config_json['thursday']),
            AlarmDay.from_json(config_json['friday']),
            AlarmDay.from_json(config_json['saturday']),
            AlarmDay.from_json(config_json['sunday'])
        )

    def to_json(self) -> dict:
        """Dump this AlarmConfig object into a dict."""
        return {
            'monday': self.monday.to_json(),
            'tuesday': self.tuesday.to_json(),
            'wednesday': self.wednesday.to_json(),
            'thursday': self.thursday.to_json(),
            'friday': self.friday.to_json(),
            'saturday': self.saturday.to_json(),
            'sunday': self.sunday.to_json()
        }


@dataclass
class AlarmDay:
    """
    Alarm config for a single day.

    :var active: If the alarm is active on this day.
    :var time: The time the alarm should go off.
    :var override_active: If the alarm should only once go off at a different time.
    :var override_time: The time the alarm should go off if override_active is true.
    """
    active: bool
    time: time
    override_active: bool
    override_time: time

    @classmethod
    def from_json(cls, config_json: dict) -> AlarmDay:
        """Create a AlarmDay object from a dict."""
        return cls(
            config_json['active'],
            time.fromisoformat(config_json['time']),
            config_json['overrideActive'],
            time.fromisoformat(config_json['overrideTime'])
        )

    def to_json(self) -> dict:
        """Dump this AlarmDay object into a dict."""
        return {
            'active': self.active,
            'time': self.time.isoformat(),
            'overrideActive': self.override_active,
            'overrideTime': self.override_time.isoformat()
        }
