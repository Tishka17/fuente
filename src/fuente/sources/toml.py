import sys
from datetime import date, datetime, time
from pathlib import Path

from adaptix import Provider, as_is_loader

from .nested import NestedSource

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

class TomlSource(NestedSource):
    def __init__(self, path: str, recipe: list[Provider] | None = None):
        super().__init__()
        self._path = path
        self._recipe = recipe or []

    def _loading_recipe(self) -> list[Provider]:
        return [
            *self._recipe,
            as_is_loader(datetime),
            as_is_loader(date),
            as_is_loader(time),
        ]

    def _load_raw(self):
        location = Path(self._path).expanduser()
        with location.open("rb") as f:
            return tomllib.load(f)
