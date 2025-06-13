from abc import abstractmethod
from typing import Protocol, TypeVar

from fuente.error_mode import ErrorMode

ConfigT = TypeVar("ConfigT")
ConfigDictT = TypeVar("ConfigDictT")


class ConfigSourceLoader(Protocol[ConfigDictT]):
    @abstractmethod
    def load(self) -> ConfigDictT:
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
