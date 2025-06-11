from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from adaptix import Retort, as_is_loader

from ..error_mode import ErrorMode
from ..skip_error_provider import SkipErrorProvider
from .nested import NestedSource


class YamlSource(NestedSource):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def _init_retorts(self, t: Any, error_mode: ErrorMode):
        recipe = [
            as_is_loader(datetime),
            as_is_loader(date),
        ]
        if error_mode in (ErrorMode.SKIP_FIELD, ErrorMode.FAIL_NOT_PARSED):
            recipe.append(SkipErrorProvider())
        self.loading_retort = Retort(recipe=recipe)

    def _load_raw(self):
        location = Path(self.name).expanduser()
        with location.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
