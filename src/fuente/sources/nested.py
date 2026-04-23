from abc import ABC, abstractmethod
from typing import Any

from adaptix import Provider, Retort

from fuente.dict_provider import ModelToDictLoaderProvider
from fuente.entities import SrcMetadata
from fuente.error_mode import ErrorMode
from fuente.protocols import (
    ConfigDictT,
    ConfigSourceLoader,
    ConfigT,
    ConfigWrapper,
    RawConfigSourceLoader,
    Source,
)
from fuente.skip_error_provider import SkipErrorProvider


class NestedSourceLoader(ConfigSourceLoader, ABC):
    def __init__(
            self,
            config_type: type,
            loading_retort: Retort,
            raw_loader: RawConfigSourceLoader,
    ):
        self.loading_retort = loading_retort
        self.config_type = config_type
        self.raw_loader = raw_loader

    def load(self):
        raw = self.raw_loader()
        values = self.loading_retort.load(raw, self.config_type)
        return ConfigWrapper(
            config=values,
            metadata=SrcMetadata(),
        )


class NestedSource(Source, ABC):
    def _loading_recipe(self) -> list[Provider]:
        return []

    def _make_loading_retort(
            self,
            config_type: type,
            error_mode: ErrorMode,
    ):
        recipe = self._loading_recipe()
        if error_mode in (ErrorMode.SKIP_FIELD, ErrorMode.FAIL_NOT_PARSED):
            recipe.append(SkipErrorProvider())
        recipe.append(ModelToDictLoaderProvider())
        return Retort(recipe=recipe)

    def make_loader(
            self,
            config_type: ConfigT,
            error_mode: ErrorMode,
    ) -> ConfigSourceLoader[ConfigDictT]:
        return self._make_loader(
            loading_retort=self._make_loading_retort(config_type, error_mode),
            config_type=config_type,
        )

    @abstractmethod
    def _load_raw(self) -> dict[str, Any]:
        raise NotImplementedError

    def _make_loader(
            self,
            loading_retort: Retort,
            config_type: ConfigDictT,
    ) -> ConfigSourceLoader[ConfigDictT]:
        return NestedSourceLoader(
            config_type=config_type,
            loading_retort=loading_retort,
            raw_loader=self._load_raw,
        )
