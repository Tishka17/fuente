from collections.abc import Iterable

import dotenv
from adaptix import Retort

from .flat import FlatSource, FlatSourceLoader


class DotenvSourceLoader(FlatSourceLoader):
    def __init__(
            self,
            loading_retort: Retort,
            dumping_retort: Retort,
            config_type: type,
            path: str,
    ):
        super().__init__(loading_retort, dumping_retort, config_type)
        self.path = path

    def _load_raw(self):
        return dotenv.dotenv_values(self.path)


class DotenvSource(FlatSource):
    def __init__(
            self,
            *,
            path: str,
            prefix: str,
            sep: str = "_",
            names: dict[str, Iterable[str]] | None = None,
    ):
        super().__init__(prefix=prefix, sep=sep, names=names)
        self._path = path

    def _make_loader(
            self,
            loading_retort: Retort,
            dumping_retort: Retort,
            config_type: type,
    ) -> FlatSourceLoader:
        return DotenvSourceLoader(
            loading_retort=loading_retort,
            dumping_retort=dumping_retort,
            config_type=config_type,
            path=self._path,
        )
