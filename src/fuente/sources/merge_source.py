from collections.abc import Sequence
from typing import TypeVar

from adaptix import Provider
from adaptix._internal.morphing.load_error import LoadError

from fuente.error_mode import ErrorMode
from fuente.merger_provider import MergeRetort
from fuente.protocols import ConfigSourceLoader, Source

ConfigT = TypeVar("ConfigT")
ConfigDictT = TypeVar("ConfigDictT")


class MergeSourceLoader(ConfigSourceLoader[ConfigDictT]):
    def __init__(
            self,
            source_loaders: list[ConfigSourceLoader[ConfigDictT]],
            retort: MergeRetort,
            error_mode: ErrorMode,
            config_type: type,
    ) -> None:
        self.source_loaders = source_loaders
        self.retort = retort
        self.error_mode = error_mode
        self.config_type = config_type

    def load(self):
        merger = self.retort.merger(self.config_type)
        loaders = iter(self.source_loaders)
        first_cfg = next(loaders).load()
        for n, src in enumerate(loaders, 1):
            try:
                next_cfg = src.load()
            except LoadError:
                if self.error_mode is ErrorMode.SKIP_SOURCE:
                    continue
                raise
            first_cfg = merger(n, first_cfg, next_cfg)
        return first_cfg


class MergeSource(Source[ConfigT, ConfigDictT]):
    def __init__(
            self,
            recipe: list[Provider],
            sources: Sequence[Source[ConfigT, ConfigDictT]],
    ) -> None:
        self._recipe = recipe
        self._sources = sources

    def make_loader(
            self,
            config_type: ConfigT,
            error_mode: ErrorMode,
    ) -> ConfigSourceLoader[ConfigDictT]:
        return MergeSourceLoader(
            retort=MergeRetort(recipe=self._recipe),
            source_loaders=[
                s.make_loader(config_type=config_type, error_mode=error_mode)
                for s in self._sources
            ],
            config_type=config_type,
            error_mode=error_mode,
        )
