from datetime import datetime
from typing import Any, TypedDict

from adaptix import (
    CannotProvide,
    Chain,
    Retort,
    as_is_dumper,
    loader,
    name_mapping,
)
from adaptix._internal.provider.loc_stack_filtering import LocStack
from adaptix._internal.provider.location import TypeHintLoc
from adaptix._internal.provider.shape_provider import InputShapeRequest


class FlatSource:
    def __init__(self, prefix: str):
        self.retort = Retort()
        self._prefix = prefix
        self.loading_retort = None
        self.dumping_retort = None
        self._type = None

    def _gen_key(self, prefix: str, path: list[str]):
        return prefix + "_".join(x.upper() for x in path)

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
            field_path = path + [field.id]
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

    def _init_retorts(self, t: Any, prefix: str):
        names, types = self._convert_type(t, prefix)
        self._type = TypedDict("Config_td", types, total=False)

        self.loading_retort = Retort(
            recipe=[
                loader(set[str], lambda s: s.split(","), Chain.FIRST),
            ],
            strict_coercion=False,
        )

        self.dumping_retort = Retort(
            recipe=[
                name_mapping(self._type, map=names),
                as_is_dumper(set[str]),
                as_is_dumper(datetime),
            ],
        )

    def _load_raw(self):
        raise NotImplementedError

    def load(self, t: Any):
        if self.loading_retort is None:
            self._init_retorts(t, self._prefix)

        raw = self._load_raw()
        return self.dumping_retort.dump(
            self.loading_retort.load(raw, self._type),
            self._type,
        )
