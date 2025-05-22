from abc import ABC
from copy import copy
from enum import Enum
from typing import (
    TypeVar, Callable, Union, )


class MergeForbiddenError(Exception):
    pass


class Special(Enum):
    NOT_SET = "<NOT SET>"


T = TypeVar("T")


class Merger(ABC):
    def __call__(self, name: str, x: Union[T, Special], y: Union[T, Special]) -> Union[T, Special]:
        if x is Special.NOT_SET:
            return y
        if y is Special.NOT_SET:
            return x
        return self._merge(name, x, y)

    def _merge(self, name: str, x: T, y: T) -> T:
        raise NotImplementedError


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


class DictMerge(Merger):
    def __init__(self, value_merger: Merger = Forbid()):
        self.value_merger = value_merger

    def _merge(self, name: str, x: dict, y: dict) -> dict:  # type: ignore[override]
        result = copy(x)
        for key, value in y.items():
            if key in result:
                result[key] = self.value_merger(key, result[key], value)
            else:
                result[key] = value
        return result


class ApplyFunc(Merger):
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, name: str, x: Union[T, Special], y: Union[T, Special]) -> Union[T, Special]:
        if x is Special.NOT_SET:
            return y
        if y is Special.NOT_SET:
            return x
        return self.func(x, y)


class TypedDictMerge(Merger):
    def __init__(self, value_mergers: dict[str, Merger], default: Merger = Forbid()):
        self.value_mergers = value_mergers
        self.default = default

    def _merge(self, name: str, x: dict, y: dict) -> dict:  # type: ignore[override]
        result = copy(x)
        for key, value in y.items():
            if key in result:
                value_merger = self.value_mergers.get(key, self.default)
                result[key] = value_merger(key, result[key], value)
            else:
                result[key] = value
        return result

