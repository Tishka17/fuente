from adaptix import Mediator, CannotProvide, bound
from adaptix._internal.model_tools.definitions import InputShape
from adaptix._internal.provider.fields import input_field_to_loc
from adaptix._internal.provider.located_request import LocatedRequest, \
    LocatedRequestMethodsProvider
from adaptix._internal.provider.methods_provider import method_handler
from adaptix._internal.provider.shape_provider import \
    provide_generic_resolved_shape, InputShapeRequest

from fuente.merger.base import Merger
from fuente.merger.nested import TypedDictMerge
from fuente.merger.simple import UseLast


class MergeRequest(LocatedRequest):
    pass


class MergeProvider(LocatedRequestMethodsProvider):
    @method_handler
    def provide_loader(self, mediator: Mediator[Merger],
                       request: MergeRequest) -> Merger:
        shape = self._fetch_shape(mediator, request)
        if not shape:
            raise CannotProvide()
        field_mergers = self._fetch_field_mergers(mediator, request, shape)

        return mediator.cached_call(
            self._make_merger,
            field_mergers=field_mergers,
        )

    def _fetch_shape(self, mediator: Mediator,
                     request: LocatedRequest) -> InputShape | None:
        try:
            return provide_generic_resolved_shape(mediator, InputShapeRequest(
                loc_stack=request.loc_stack))
        except CannotProvide:
            return None

    def _fetch_field_mergers(
            self,
            mediator: Mediator,
            request: MergeRequest,
            shape: InputShape,
    ) -> tuple[tuple[str, Merger], ...]:
        return tuple(
            (
                field.id,
                mediator.provide(
                    request.append_loc(input_field_to_loc(field))
                ) or UseLast(),
            )
            for field in shape.fields
        )

    def _make_merger(self, field_mergers) -> Merger:
        return TypedDictMerge(
            value_mergers=dict(field_mergers),
        )


class FixedMergeProvider(LocatedRequestMethodsProvider):
    def __init__(self, merger: Merger) -> None:
        self.merger = merger

    @method_handler
    def provide_loader(self, mediator: Mediator[Merger],
                       request: MergeRequest) -> Merger:
        return self.merger


def merge(predicat, merger):
    return bound(predicat, FixedMergeProvider(merger))
