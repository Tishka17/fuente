from typing import (
    TypeVar, Union, Callable, )

from .base import Merger, MergeForbiddenError, Special

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
            f"New: {y}"
        )


class Concat(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return x + y  # type: ignore[operator]


class Unite(Merger):
    def _merge(self, name: str, x: T, y: T) -> T:
        return x | y  # type: ignore[operator]


class ApplyFunc(Merger):
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, name: str, x: Union[T, Special],
                 y: Union[T, Special]) -> Union[T, Special]:
        if x is Special.NOT_SET:
            return y
        if y is Special.NOT_SET:
            return x
        return self.func(x, y)
