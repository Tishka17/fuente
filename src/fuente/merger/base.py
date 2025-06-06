from abc import ABC
from enum import Enum
from typing import TypeVar


class MergeForbiddenError(Exception):
    pass


class Special(Enum):
    NOT_SET = "<NOT SET>"


T = TypeVar("T")


class Merger(ABC):
    def __call__(self, name: str, x: T | Special,
                 y: T | Special) -> T | Special:
        if x is Special.NOT_SET:
            return y
        if y is Special.NOT_SET:
            return x
        return self._merge(name, x, y)

    def _merge(self, name: str, x: T, y: T) -> T:
        raise NotImplementedError
