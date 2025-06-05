from dataclasses import dataclass

from fuente import parse
from fuente.merger import TypedDictMerge, UseLast, Unite
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource


@dataclass
class Config:
    log_level: str
    database_uri: str
    blacklist: set[str]


cfg = parse(
    EnvSource("MYAPP"),
    YamlSource("config.yaml"),
    YamlSource("config2.yaml"),
    merger=TypedDictMerge({
        "log_level": UseLast(),
        "database_uri": UseLast(),
        "blacklist": Unite(),
    }),
    type=Config
)
print(cfg)
