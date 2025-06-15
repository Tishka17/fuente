import collections
from typing import Generic, TypeVar

from adaptix import Chain, P, Provider, Retort, as_is_loader, bound, loader
from adaptix._internal.morphing.constant_length_tuple_provider import (
    ConstantLengthTupleProvider,
)
from adaptix._internal.morphing.iterable_provider import IterableProvider
from adaptix._internal.morphing.model.loader_provider import (
    ModelLoaderProvider,
)
from adaptix._internal.morphing.model.request_filtering import AnyModelLSC
from adaptix._internal.provider.loc_stack_filtering import VarTupleLSC

from fuente.error_mode import ErrorMode
from fuente.merger.base import Special
from fuente.protocols import ConfigSourceLoader, Loader, Source
from fuente.sources.merge_source import MergeSource

ConfigT = TypeVar("ConfigT")
ConfigDictT = TypeVar("ConfigDictT")


class LoaderImpl(Generic[ConfigT]):
    def __init__(
            self,
            config_type: type[ConfigT],
            source: ConfigSourceLoader[ConfigDictT],
            retort: Retort,
    ):
        self._config_type = config_type
        self._source = source
        self._retort = retort

    def load(self) -> ConfigT:
        config = self._source.load()
        return self._retort.load(config, self._config_type)


def clean_not_parsed_fields(data):
    return {
        k: v
        for k, v in data.items()
        if v is not Special.NOT_LOADED
    }


def check_not_parsed_fields(data):
    if any(v is Special.NOT_LOADED for k, v in data.items()):
        raise ValueError
    return data


reload_recipe = [
    bound(list, IterableProvider(dump_as=list)),
    bound(VarTupleLSC(), IterableProvider(dump_as=tuple)),
    bound(
        set,
        IterableProvider(dump_as=list, json_schema_unique_items=True),
    ),
    bound(
        frozenset,
        IterableProvider(dump_as=tuple, json_schema_unique_items=True),
    ),
    bound(collections.deque, IterableProvider(dump_as=list)),
    ConstantLengthTupleProvider(),
    ModelLoaderProvider(),
    as_is_loader(P[~AnyModelLSC()]),
]


def config_loader(
        *config_sources: Source[ConfigT, ConfigDictT],
        config: type[ConfigT],
        recipe: list[Provider] | None = None,
        error_mode: ErrorMode = ErrorMode.FAIL_NOT_PARSED,
) -> Loader[ConfigT]:
    if error_mode is ErrorMode.FAIL_NOT_PARSED:
        err_recipe = [
            loader(AnyModelLSC(), check_not_parsed_fields, Chain.FIRST),
        ]
    elif error_mode is ErrorMode.SKIP_FIELD:
        err_recipe = [
            loader(AnyModelLSC(), clean_not_parsed_fields, Chain.FIRST),
        ]
    else:
        err_recipe = []
    recipe = recipe or []
    retort = Retort(
        recipe=recipe + err_recipe + reload_recipe,
        strict_coercion=False,
    )

    source = MergeSource(sources=config_sources, recipe=recipe)
    return LoaderImpl(
        config_type=config,
        source=source.make_loader(config_type=config, error_mode=error_mode),
        retort=retort,
    )


def load(
        *config_sources: Source[ConfigT, ConfigDictT],
        config: type[ConfigT],
        recipe: list[Provider] | None = None,
        error_mode: ErrorMode = ErrorMode.FAIL_NOT_PARSED,
) -> ConfigT:
    return config_loader(
        *config_sources,
        config=config,
        recipe=recipe,
        error_mode=error_mode,
    ).load()
