from abc import ABC, abstractmethod
from typing import Any, TypedDict

from adaptix import CannotProvide, Retort
from adaptix._internal.provider.loc_stack_filtering import LocStack
from adaptix._internal.provider.location import TypeHintLoc
from adaptix._internal.provider.shape_provider import InputShapeRequest

from fuente.error_mode import ErrorMode
from fuente.protocols import (
    ConfigDictT,
    ConfigSourceLoader,
    ConfigT,
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
        return self.loading_retort.load(raw, self.config_type)


class NestedSource(Source, ABC):
    def __init__(self):
        self._retort = Retort()

    def _make_loading_retort(
            self,
            config_type: type,
            error_mode: ErrorMode,
    ):
        recipe = []
        if error_mode in (ErrorMode.SKIP_FIELD, ErrorMode.FAIL_NOT_PARSED):
            recipe.append(SkipErrorProvider())
        return Retort(recipe=recipe)

    def _convert_type(self, types: dict[str, Any], t: Any) -> Any:
        if t in types:
            return types[t]

        try:
            shape = self._retort._provide_from_recipe(  # noqa: SLF001
                InputShapeRequest(LocStack(TypeHintLoc(type=t))),
            )
        except CannotProvide:
            return t

        field_types = {}
        for field in shape.fields:
            field_types[field.id] = self._convert_type(types, field.type)
        new_t = TypedDict("Config_td", field_types, total=False)
        types[t] = new_t
        return new_t

    def make_loader(
            self,
            config_type: ConfigT,
            error_mode: ErrorMode,
    ) -> ConfigSourceLoader[ConfigDictT]:
        return self._make_loader(
            loading_retort=self._make_loading_retort(config_type, error_mode),
            config_type=self._convert_type({}, config_type),
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
