from adaptix import Retort

from .converter import to_cfg_model


def parse(first_source, *sources, merger, type):
    retort = Retort()
    typed_dict_model = to_cfg_model(type)
    first = retort.load(first_source, typed_dict_model)
    for n, source in enumerate(sources, 1):
        next = retort.load(source, typed_dict_model)
        first = merger(n, first, next)
    return retort.load(first, type)
