from datetime import date, datetime
from pathlib import Path

import yaml
from adaptix import Provider

from fuente.check_type_provider import check_type_loader
from .nested import NestedSource


class YamlSource(NestedSource):
    def __init__(self, path: str, recipe: list[Provider] | None = None):
        super().__init__()
        self._path = path
        self._recipe = recipe or []

    def _loading_recipe(self) -> list[Provider]:
        return [
            *self._recipe,
            check_type_loader(datetime),
            check_type_loader(date),
            check_type_loader(bool),
        ]

    def _load_raw(self):
        location = Path(self._path).expanduser()
        with location.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
