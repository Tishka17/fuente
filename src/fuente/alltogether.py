from adaptix import Provider, Retort
from adaptix._internal.common import VarTuple
from adaptix._internal.provider.loc_stack_filtering import LocStack
from adaptix._internal.provider.location import TypeHintLoc

from fuente.merger.simple import UseLast
from fuente.merger_provider import (
    FixedMergeProvider,
    MergeProvider,
    MergeRequest,
)


def _raw(sources, type):
    for source in sources:
        yield source.load(type)


class MergeRetort(Retort):
    def _get_recipe_tail(self) -> VarTuple[Provider]:
        return super()._get_recipe_tail() + (
            MergeProvider(),
            FixedMergeProvider(UseLast()),
        )

    def merger(self, type):
        return self._provide_from_recipe(
            MergeRequest(LocStack(TypeHintLoc(type=type))),
        )


def parse(*sources, recipe, type):
    cfgs = _raw(sources, type)

    retort = MergeRetort(recipe=recipe)
    merger = retort.merger(type)

    first_cfg = next(cfgs)
    for n, next_cfg in enumerate(cfgs, 1):
        first_cfg = merger(n, first_cfg, next_cfg)
    return retort.load(first_cfg, type)
