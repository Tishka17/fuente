from pathlib import Path

import yaml

from .nested import NestedSource


class YamlSource(NestedSource):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def _load_raw(self):
        location = Path(self.name).expanduser()
        with location.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
