from collections.abc import Sequence
from typing import TypeVar

from adaptix._internal.morphing.load_error import LoadError
from adaptix._internal.morphing.request_cls import LoaderRequest
from adaptix._internal.provider.essential import (
    Mediator,
    Provider,
    Request,
    RequestChecker,
    RequestHandler,
)
from adaptix._internal.provider.request_checkers import (
    AlwaysTrueRequestChecker,
)

from fuente.merger.base import Special

T = TypeVar("T")

RequestT = TypeVar("RequestT", bound=Request)
ResponseT = TypeVar("ResponseT")


class SkipErrorProvider(Provider):
    def _wrap_handler(
            self,
            mediator: Mediator[ResponseT],
            request: RequestT,
    ) -> RequestHandler[ResponseT, RequestT]:
        next_processor = mediator.provide_from_next()

        def chain_processor(data):
            try:
                return next_processor(data)
            except LoadError:
                return Special.NOT_LOADED

        return chain_processor

    def get_request_handlers(self) -> Sequence[
        tuple[type[Request], RequestChecker, RequestHandler]
    ]:
        return [
            (LoaderRequest, AlwaysTrueRequestChecker(), self._wrap_handler),
        ]
