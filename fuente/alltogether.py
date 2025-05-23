from adaptix import Retort

from .converter import to_cfg_model

def _raw(sources, type):
    for source in sources:
        for cfg in source.load(type):
            yield cfg

def parse(*sources, merger, type):
    retort = Retort()
    typed_dict_model = to_cfg_model(type)

    cfgs = _raw(sources, typed_dict_model)
    first_cfg = next(cfgs)
    for n, next_cfg in enumerate(cfgs, 1):
        first_cfg = merger(n, first_cfg, next_cfg)
    return retort.load(first_cfg, type)
