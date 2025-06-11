from typing import Any

from adaptix._internal.morphing.load_error import LoadError

from ..error_mode import ErrorMode
from ..merger_provider import MergeRetort


class MergeSource:
    def __init__(self, sources, recipe) -> None:
        self.sources = sources
        self.retort = MergeRetort(recipe=recipe)

    def load(self, t: Any, error_mode):
        merger = self.retort.merger(t)
        sources = iter(self.sources)
        first_cfg = next(sources).load(t, error_mode)
        for n, src in enumerate(sources, 1):
            try:
                next_cfg = src.load(t, error_mode)
            except LoadError:
                if error_mode is ErrorMode.SKIP_SOURCE:
                    continue
                raise
            first_cfg = merger(n, first_cfg, next_cfg)
        return first_cfg
