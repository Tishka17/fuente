import os
from pathlib import Path

import yaml
from adaptix import name_mapping, Retort


class EnvSource:
    def __init__(self, prefix: str = ""):
        self.retort = Retort(recipe=[
            name_mapping(map=[(".*", lambda x, y: f"{prefix}{y.id.upper()}")]),
        ])

    def load(self, type):
        return [self.retort.load(os.environ, type)]


class YamlSource:
    def __init__(self, name: str = "", paths: list[str] | None = None):
        self.name = name
        self.paths = paths or (
            Path("/etc/") / self.name / "config.yaml",
            Path("~/.config").expanduser() / self.name / "config.yaml",
            Path(".") / "config.yaml",
        )
        self.retort = Retort(recipe=[])

    def load(self, type):
        res = []
        for location in self.paths:
            location = Path(location).expanduser()
            if location.exists():
                with location.open(encoding="utf-8") as f:
                    contents = yaml.safe_load(f)
                res.append(self.retort.load(contents, type))
        return res
