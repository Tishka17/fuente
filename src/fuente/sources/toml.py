import sys
from datetime import date, datetime, time
from pathlib import Path

from adaptix import Provider

from fuente.check_type_provider import check_type_loader
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
            check_type_loader(datetime),
            check_type_loader(date),
            check_type_loader(time),
            check_type_loader(bool),
        ]

    def _load_raw(self):
        location = Path(self._path).expanduser()
        with location.open("rb") as f:
            return tomllib.load(f)
