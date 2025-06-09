from collections.abc import Iterable

import dotenv

from .flat import FlatSource


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
        self.path = path

    def _load_raw(self):
        return dotenv.dotenv_values(self.path)
