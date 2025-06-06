from typing import Any

from ..merger_provider import MergeRetort


class MergeSource:
    def __init__(self, sources, recipe) -> None:
        self.sources = sources
        self.retort = MergeRetort(recipe=recipe)

    def load(self, t: Any):
        merger = self.retort.merger(t)
        sources = iter(self.sources)
        first_cfg = next(sources).load(t)
        for n, src in enumerate(sources, 1):
            next_cfg = src.load(t)
            first_cfg = merger(n, first_cfg, next_cfg)
        return first_cfg
