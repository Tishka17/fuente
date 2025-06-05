from adaptix import Retort


def _raw(sources, type):
    for source in sources:
        yield source.load(type)


def parse(*sources, merger, type):
    retort = Retort()
    cfgs = _raw(sources, type)
    first_cfg = next(cfgs)
    for n, next_cfg in enumerate(cfgs, 1):
        first_cfg = merger(n, first_cfg, next_cfg)
    return retort.load(first_cfg, type)
