from datetime import date, datetime
from pathlib import Path

import yaml
from adaptix import Provider, as_is_loader

from .nested import NestedSource


class YamlSource(NestedSource):
    def __init__(self, path: str, recipe: list[Provider] | None = None):
        super().__init__()
        self._path = path
        self._recipe = recipe or []

    def _loading_recipe(self) -> list[Provider]:
        return [
            *self._recipe,
            as_is_loader(datetime),
            as_is_loader(date),
        ]

    def _load_raw(self):
        location = Path(self._path).expanduser()
        with location.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
