from typing import TypeVar

from adaptix._internal.morphing.load_error import LoadError

from fuente.error_mode import ErrorMode
from fuente.merger_provider import MergeRetort
from fuente.protocols import ConfigSourceLoader

ConfigT = TypeVar("ConfigT")
ConfigDictT = TypeVar("ConfigDictT")


class MergeSourceLoader(ConfigSourceLoader):
    def __init__(
            self,
            sources,
            retort,
            error_mode,
            config_type,
    ) -> None:
        self.sources = sources
        self.retort = retort
        self.error_mode = error_mode
        self.config_type = config_type

    def load(self):
        merger = self.retort.merger(self.config_type)
        sources = iter(self.sources)
        first_cfg = next(sources).load()
        for n, src in enumerate(sources, 1):
            try:
                next_cfg = src.load()
            except LoadError:
                if self.error_mode is ErrorMode.SKIP_SOURCE:
                    continue
                raise
            first_cfg = merger(n, first_cfg, next_cfg)
        return first_cfg


class MergeSource:
    def __init__(self, recipe, sources):
        self._recipe = recipe
        self._sources = sources

    def make_loader(
            self,
            config_type: ConfigT,
            error_mode: ErrorMode,
    ) -> ConfigSourceLoader[ConfigDictT]:
        return MergeSourceLoader(
            retort=MergeRetort(recipe=self._recipe),
            sources=self._sources,
            config_type=config_type,
            error_mode=error_mode,
        )
