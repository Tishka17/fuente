from datetime import date, datetime
from pathlib import Path

import yaml
from adaptix import Retort, as_is_loader

from fuente.error_mode import ErrorMode
from fuente.skip_error_provider import SkipErrorProvider
from .nested import NestedSource


class YamlSource(NestedSource):
    def __init__(self, path: str):
        super().__init__()
        self._path = path

    def _make_loading_retort(self, config_type: type, error_mode: ErrorMode):
        recipe = [
            as_is_loader(datetime),
            as_is_loader(date),
        ]
        if error_mode in (ErrorMode.SKIP_FIELD, ErrorMode.FAIL_NOT_PARSED):
            recipe.append(SkipErrorProvider())
        return Retort(recipe=recipe)

    def _load_raw(self):
        location = Path(self._path).expanduser()
        with location.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
