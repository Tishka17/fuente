from adaptix import Retort

from fuente.sources.merge_source import MergeSource


def _raw(sources, type):
    for source in sources:
        yield source.load(type)


def parse(*sources, recipe, type):
    source = MergeSource(sources=sources, recipe=recipe)
    retort = Retort(recipe=recipe)
    config = source.load(type)
    return retort.load(config, type)
