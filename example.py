from dataclasses import dataclass

from adaptix import P

from fuente import parse
from fuente.merger.simple import UseFirst, Unite, UseLast
from fuente.merger_provider import MergeProvider, FixedMergeProvider, merge
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource


@dataclass
class DbConfig:
    uri: str


@dataclass
class Config:
    log_level: str
    database: DbConfig
    blacklist: set[str]


cfg = parse(
    EnvSource("MYAPP"),
    YamlSource("config.yaml"),
    YamlSource("config2.yaml"),
    recipe=[
        merge(P[Config].log_level, UseFirst()),
        merge(P[DbConfig].uri, UseFirst()),
        merge(P[Config].blacklist, Unite()),
        MergeProvider(),
        FixedMergeProvider(UseLast()),
    ],
    type=Config
)
print(cfg)
