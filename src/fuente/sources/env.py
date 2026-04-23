import os
from typing import Any

from ..entities import Marker, SourceType
from .flat import FlatSource

ENV_SOURCE_TYPE = SourceType("ENV")

class EnvSource(FlatSource):
    def _load_raw(self) -> dict[str, Any]:
        return os.environ

    def _load_metadata(self) -> dict[str, Any]:
        return {
            item: Marker(
                source_type=ENV_SOURCE_TYPE,
                snippet=f"{item}={value}",
            ) for item,value in self.__dict__.items()
        }
