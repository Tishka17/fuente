from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar


class MergeForbiddenError(Exception):
    pass


class Special(Enum):
    NOT_LOADED = "<NOT LOADED>"


T = TypeVar("T")


class Merger(ABC):
    def __call__(self, name: str, x: T | Special,
                 y: T | Special) -> T | Special:
        if x is Special.NOT_LOADED:
            return y
        if y is Special.NOT_LOADED:
            return x
        return self._merge(name, x, y)

    @abstractmethod
    def _merge(self, name: str, x: T, y: T) -> T:
        raise NotImplementedError
