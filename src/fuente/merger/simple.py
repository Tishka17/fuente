from collections.abc import Callable
from typing import TypeVar

from .base import MergeForbiddenError, Merger

T = TypeVar("T")


class UseFirst(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return x


class UseLast(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return y


class Forbid(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        raise MergeForbiddenError(f"Override is forbidden for field {name}")


class ForbidChange(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        if x == y:
            return x
        raise MergeForbiddenError(
            f"Override with different value is forbidden for field {name}:\n"
            f"Old: {x}\n"
            f"New: {y}",
        )


class Concat(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return x + y  # type: ignore[operator]


class Unite(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return x | y  # type: ignore[operator]


class Max(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return max(x, y)  # type: ignore[operator]


class Min(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return min(x, y)  # type: ignore[operator]


class ApplyFunc(Merger):
    def __init__(self, func: Callable[[T, T], T]):
        self.func = func

    def _merge(self, name: str, x: T, y: T) -> T:
        return self.func(x, y)  # type: ignore[operator]
