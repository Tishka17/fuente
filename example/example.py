import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime

from adaptix import P

from fuente import parse
from fuente.error_mode import ErrorMode
from fuente.merger.simple import Max, Unite, UseFirst
from fuente.merger_provider import merge
from fuente.sources.argparse import ArgParseSource
from fuente.sources.dotenv import DotenvSource
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
    min_date: datetime
    default_param: str = "default"


arg_parser = ArgumentParser()
cfg = parse(
    EnvSource(prefix="MYAPP_", names={"DB_URI": ["database", "uri"]}),
    DotenvSource(path=".env.example", prefix="MYAPP_"),
    YamlSource("config.yaml"),
    YamlSource("config2.yaml"),
    ArgParseSource(arg_parser, args=sys.argv),
    recipe=[
        merge(P[Config].log_level, UseFirst()),
        merge(P[DbConfig].uri, UseFirst()),
        merge(P[Config].blacklist, Unite()),
        merge(P[Config].min_date, Max()),
    ],
    type=Config,
    error_mode=ErrorMode.FAIL_ALWAYS,
)
print(cfg)
