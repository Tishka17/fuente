from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar

from fuente.entities import SrcMetadata
from fuente.error_mode import ErrorMode

ConfigT = TypeVar("ConfigT")
ConfigDictT = TypeVar("ConfigDictT")


@dataclass
class ConfigWrapper(Generic[ConfigDictT]):
    config: ConfigDictT
    metadata: SrcMetadata


class ConfigSourceLoader(Protocol[ConfigDictT]):
    @abstractmethod
    def load(self) -> ConfigWrapper[ConfigDictT]:
        raise NotImplementedError


class Source(Protocol[ConfigT, ConfigDictT]):
    @abstractmethod
    def make_loader(
            self,
            config_type: ConfigT,
            error_mode: ErrorMode,
    ) -> ConfigSourceLoader[ConfigDictT]:
        raise NotImplementedError


class Loader(Protocol[ConfigT]):
    @abstractmethod
    def load(self) -> ConfigT:
        raise NotImplementedError


class RawConfigSourceLoader(Protocol):
    @abstractmethod
    def __call__(self) -> dict[str, Any]:
        raise NotImplementedError
