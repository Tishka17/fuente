from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, TypedDict

from adaptix import (
    CannotProvide,
    Chain,
    P,
    Retort,
    as_is_dumper,
    loader,
    name_mapping,
)
from adaptix._internal.provider.loc_stack_filtering import LocStack
from adaptix._internal.provider.location import TypeHintLoc
from adaptix._internal.provider.shape_provider import InputShapeRequest

from fuente.error_mode import ErrorMode
from fuente.protocols import ConfigSourceLoader, RawConfigSourceLoader, Source
from fuente.skip_error_provider import SkipErrorProvider


class FlatSourceLoader(ConfigSourceLoader):
    def __init__(
            self,
            loading_retort: Retort,
            dumping_retort: Retort,
            config_type: type,
            raw_loader: RawConfigSourceLoader,
    ) -> None:
        self._loading_retort = loading_retort
        self._dumping_retort = dumping_retort
        self._config_type = config_type
        self._raw_loader = raw_loader

    def load(self):
        raw = self._raw_loader()
        return self._dumping_retort.dump(
            self._loading_retort.load(raw, self._config_type),
            self._config_type,
        )


class FlatSource(Source, ABC):
    def __init__(
            self,
            *,
            prefix: str,
            sep: str = "_",
            names: dict[str, Iterable[str]] | None = None,
    ):
        self.retort = Retort()
        self._prefix = prefix
        self.loading_retort = None
        self.dumping_retort = None
        self._type = None
        self._sep = sep
        self._user_mapping = names or {}

    def _gen_key(self, prefix: str, path: list[str]):
        for user_key, user_path in self._user_mapping.items():
            if isinstance(user_path, str):
                user_path = [user_path]
            else:
                user_path = list(user_path)
            if user_path == path:
                return user_key
        return prefix + self._sep.join(x.upper() for x in path)

    def _convert_type(
            self, t: Any, prefix: str,
            path: list[str] | None = None,
    ) -> tuple[dict[str, list[str]] | None, dict[str, Any] | None]:
        names = {}
        types = {}
        if path is None:
            path = []

        try:
            shape = self.retort._provide_from_recipe(
                InputShapeRequest(LocStack(TypeHintLoc(type=t))),
            )
        except CannotProvide:
            return None, None

        for field in shape.fields:
            field_path = [*path, field.id]
            field_name = self._gen_key(prefix, field_path)
            tmp, tmp_types = self._convert_type(
                field.type, prefix, field_path,
            )
            if not tmp:
                names[field_name] = field_path
                types[field_name] = field.type
            else:
                names.update(tmp)
                types.update(tmp_types)

        return names, types

    def make_loader(
            self,
            config_type,
            error_mode: ErrorMode,
    ) -> FlatSourceLoader:
        names, types = self._convert_type(config_type, self._prefix)
        self._type = TypedDict("Config_td", types, total=False)
        recipe = [
            loader(P[set, list, tuple], lambda s: s.split(","), Chain.FIRST),
        ]
        if error_mode in (ErrorMode.SKIP_FIELD, ErrorMode.FAIL_NOT_PARSED):
            recipe.append(SkipErrorProvider())

        self.loading_retort = Retort(
            recipe=recipe,
            strict_coercion=False,
        )

        self.dumping_retort = Retort(
            recipe=[
                name_mapping(self._type, map=names),
                as_is_dumper(~P[self._type]),
            ],
        )
        return self._make_loader(
            loading_retort=self.loading_retort,
            dumping_retort=self.dumping_retort,
            config_type=self._type,
        )

    @abstractmethod
    def _load_raw(self) -> dict[str, Any]:
        raise NotImplementedError

    def _make_loader(
            self,
            loading_retort: Retort,
            dumping_retort: Retort,
            config_type: type,
    ) -> FlatSourceLoader:
        return FlatSourceLoader(
            loading_retort=loading_retort,
            dumping_retort=dumping_retort,
            config_type=config_type,
            raw_loader=self._load_raw,
        )
