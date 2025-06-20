from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from pprint import pprint

from adaptix import P

from fuente import config_loader
from fuente.error_mode import ErrorMode
from fuente.merger.simple import Max, Unite, UseFirst
from fuente.merger_provider import merge
from fuente.sources.argparse import ArgParseSource
from fuente.sources.dotenv import DotenvSource
from fuente.sources.env import EnvSource
from fuente.sources.toml import TomlSource
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
loader = config_loader(
    EnvSource(prefix="MYAPP_", names={"DB_URI": ["database", "uri"]}),
    DotenvSource(path=".env.example", prefix="MYAPP_"),
    YamlSource("config.yaml"),
    YamlSource("config2.yaml"),
    TomlSource("config.toml"),
    ArgParseSource(parser=arg_parser),
    recipe=[
        merge(P[Config].log_level, UseFirst()),
        merge(P[DbConfig].uri, UseFirst()),
        merge(P[Config].blacklist, Unite()),
        merge(P[Config].min_date, Max()),
    ],
    config=Config,
    error_mode=ErrorMode.FAIL_ALWAYS,
)
cfg = loader.load()
pprint(cfg)
