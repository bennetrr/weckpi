"""Utilities for working with classes, methods and fields."""
from __future__ import annotations

from collections.abc import Callable


def exception_getter():
    """Getter for the setter-only property. Just raises an exception."""
    raise TypeError('This is a setter-only property, it does not support getting the value!')


def property_setter_only(func: Callable):
    """A property that has only a setter and no getter."""
    return property(fget=exception_getter, fset=func)
