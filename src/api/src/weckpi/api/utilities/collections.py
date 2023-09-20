"""Utilities for working with collections."""
import itertools
from collections.abc import Iterable, Mapping
from typing import TypeVar

TFlatten = TypeVar('TFlatten')


def flatten(iterable: Iterable[Iterable[TFlatten]]) -> list[TFlatten]:
    """Flatten the iterable one level and return the result as a list."""
    return list(itertools.chain.from_iterable(iterable))


def flatten_dict(dictionary: Mapping[any, TFlatten]) -> list[TFlatten]:
    """Flatten the dictionary so that all values are in one list."""
    return flatten(list(dictionary.values()))
