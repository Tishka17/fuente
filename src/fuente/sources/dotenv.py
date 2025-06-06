import dotenv

from .flat import FlatSource


class DotenvSource(FlatSource):
    def __init__(self, path: str, prefix: str):
        super().__init__(prefix)
        self.path = path

    def _load_raw(self):
        return dotenv.dotenv_values(self.path)
