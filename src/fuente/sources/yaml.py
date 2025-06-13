from datetime import date, datetime
from pathlib import Path

import yaml
from adaptix import Retort, as_is_loader

from ..error_mode import ErrorMode
from ..protocols import ConfigDictT, ConfigSourceLoader
from ..skip_error_provider import SkipErrorProvider
from .nested import NestedSource, NestedSourceLoader


class YamlSourceLoader(NestedSourceLoader):
    def __init__(self, config_type: type, loading_retort: Retort, path: str):
        super().__init__(config_type, loading_retort)
        self.path = path

    def _load_raw(self):
        location = Path(self.path).expanduser()
        with location.open(encoding="utf-8") as f:
            return yaml.safe_load(f)


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

    def _make_loader(
            self,
            loading_retort: Retort,
            config_type: ConfigDictT,
    ) -> ConfigSourceLoader[ConfigDictT]:
        return YamlSourceLoader(config_type, loading_retort, self._path)
