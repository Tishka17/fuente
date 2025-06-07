import sys
from argparse import ArgumentParser
from dataclasses import dataclass

from adaptix import P

from fuente import parse
from fuente.merger.simple import Unite, UseFirst
from fuente.merger_provider import merge
from fuente.sources.dotenv import DotenvSource
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource
from fuente.sources.argparse import ArgParseSource


@dataclass
class DbConfig:
    uri: str


@dataclass
class Config:
    log_level: str
    database: DbConfig
    blacklist: set[str]
    default_param: str = "default"


arg_parser = ArgumentParser()
cfg = parse(
    EnvSource(prefix="MYAPP_"),
    DotenvSource(path=".env.example", prefix="MYAPP_"),
    YamlSource("config.yaml"),
    YamlSource("config2.yaml"),
    ArgParseSource(arg_parser, args=sys.argv),
    recipe=[
        merge(P[Config].log_level, UseFirst()),
        merge(P[DbConfig].uri, UseFirst()),
        merge(P[Config].blacklist, Unite()),
    ],
    type=Config,
)
print(cfg)
