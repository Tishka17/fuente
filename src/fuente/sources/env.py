import os
from typing import Any

from .flat import FlatSource


class EnvSource(FlatSource):
    def _load_raw(self) -> dict[str, Any]:
        return os.environ
