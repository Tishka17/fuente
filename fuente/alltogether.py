from adaptix import Retort
from adaptix._internal.provider.loc_stack_filtering import LocStack
from adaptix._internal.provider.location import TypeHintLoc

from fuente.merger.simple import UseLast
from fuente.merger_provider import MergeProvider, FixedMergeProvider, \
    MergeRequest


def _raw(sources, type):
    for source in sources:
        yield source.load(type)


default_merge_retort = Retort(
    recipe=[
        MergeProvider(),
        FixedMergeProvider(UseLast()),
    ]
)

def parse(*sources, merge_recipe, type):

    retort = Retort()
    cfgs = _raw(sources, type)

    if not merge_recipe:
        merge_retort = default_merge_retort
    else:
        merge_retort = Retort(recipe=merge_recipe)
    merger = merge_retort._provide_from_recipe(
        MergeRequest(LocStack(TypeHintLoc(type=type))),
    )

    first_cfg = next(cfgs)
    for n, next_cfg in enumerate(cfgs, 1):
        first_cfg = merger(n, first_cfg, next_cfg)
    return retort.load(first_cfg, type)
