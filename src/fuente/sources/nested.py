from typing import Any, TypedDict

from adaptix import CannotProvide, Retort
from adaptix._internal.provider.loc_stack_filtering import LocStack
from adaptix._internal.provider.location import TypeHintLoc
from adaptix._internal.provider.shape_provider import InputShapeRequest

from fuente.error_mode import ErrorMode
from fuente.skip_error_provider import SkipErrorProvider


class NestedSource:
    def __init__(self):
        self.retort = Retort()
        self.loading_retort = None
        self._type = None
        self._types: dict[Any, Any] = {}

    def _convert_type(self, t: Any) -> Any:
        if t in self._types:
            return self._types[t]

        try:
            shape = self.retort._provide_from_recipe(
                InputShapeRequest(LocStack(TypeHintLoc(type=t))),
            )
        except CannotProvide:
            return t

        types = {}
        for field in shape.fields:
            types[field.id] = self._convert_type(field.type)
        new_t = TypedDict("Config_td", types, total=False)
        self._types[t] = new_t
        return new_t

    def _init_type(self, t: Any):
        self._type  = self._convert_type(t)

    def _init_retorts(self, t: Any, error_mode: ErrorMode):
        recipe = []
        if error_mode in (ErrorMode.SKIP_FIELD, ErrorMode.FAIL_NOT_PARSED):
            recipe.append(SkipErrorProvider())
        self.loading_retort = Retort(recipe=recipe)

    def _load_raw(self):
        raise NotImplementedError

    def load(self, t: Any, error_mode: ErrorMode):
        if self.loading_retort is None:
            self._init_type(t)
            self._init_retorts(t, error_mode)

        raw = self._load_raw()
        return self.loading_retort.load(raw, self._type)
