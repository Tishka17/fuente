import collections

from adaptix import P, Retort, as_is_loader, bound
from adaptix._internal.morphing.constant_length_tuple_provider import (
    ConstantLengthTupleProvider,
)
from adaptix._internal.morphing.iterable_provider import IterableProvider
from adaptix._internal.morphing.model.loader_provider import (
    ModelLoaderProvider,
)
from adaptix._internal.morphing.model.request_filtering import AnyModelLSC
from adaptix._internal.provider.loc_stack_filtering import VarTupleLSC

from fuente.sources.merge_source import MergeSource


def _raw(sources, type):
    for source in sources:
        yield source.load(type)


reload_recipe = [
    bound(list, IterableProvider(dump_as=list)),
    bound(VarTupleLSC(), IterableProvider(dump_as=tuple)),
    bound(set,
          IterableProvider(dump_as=list, json_schema_unique_items=True)),
    bound(frozenset,
          IterableProvider(dump_as=tuple, json_schema_unique_items=True)),
    bound(collections.deque, IterableProvider(dump_as=list)),
    ConstantLengthTupleProvider(),
    ModelLoaderProvider(),
    as_is_loader(P[~AnyModelLSC()]),
]


def parse(*sources, recipe, type):
    source = MergeSource(sources=sources, recipe=recipe)
    config = source.load(type)

    retort = Retort(recipe=recipe + reload_recipe, strict_coercion=False)
    return retort.load(config, type)
