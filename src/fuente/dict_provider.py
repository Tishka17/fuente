from dataclasses import replace

from adaptix import Mediator
from adaptix._internal.model_tools.definitions import InputShape, ParamKind
from adaptix._internal.morphing.model.loader_provider import (
    ModelLoaderProvider,
)
from adaptix._internal.provider.located_request import LocatedRequest


class ModelToDictLoaderProvider(ModelLoaderProvider):
    def _fetch_shape(self, mediator: Mediator,
                     request: LocatedRequest) -> InputShape:
        shape = super()._fetch_shape(mediator, request)
        return replace(
            shape,
            constructor=dict,
            params=tuple(
                replace(param, kind=ParamKind.KW_ONLY, name=param.field_id)
                for param in shape.params
            ),
            fields=tuple(
                replace(field, is_required=False)
                for field in shape.fields
            ),
        )
