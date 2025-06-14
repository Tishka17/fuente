from copy import copy

from .base import Merger
from .simple import Forbid


class DictMerge(Merger):
    def __init__(
            self,
            value_merger: Merger = Forbid(),
    ):
        self.value_merger = value_merger

    def _merge(
            self,
            name: str,
            x: dict,
            y: dict,
    ) -> dict:  # type: ignore[override]
        result = copy(x)
        for key, value in y.items():
            if key in result:
                result[key] = self.value_merger(key, result[key], value)
            else:
                result[key] = value
        return result


class TypedDictMerge(Merger):
    def __init__(
            self,
            value_mergers: dict[str, Merger],
            default: Merger = Forbid(),
    ):
        self.value_mergers = value_mergers
        self.default = default

    def _merge(
            self,
            name: str,
            x: dict,
            y: dict,
    ) -> dict:  # type: ignore[override]
        result = copy(x)
        for key, value in y.items():
            if key in result:
                value_merger = self.value_mergers.get(key, self.default)
                result[key] = value_merger(key, result[key], value)
            else:
                result[key] = value
        return result
