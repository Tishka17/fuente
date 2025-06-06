import os

from .flat import FlatSource


class EnvSource(FlatSource):
    def __init__(self, prefix: str):
        super().__init__(prefix)


    def _load_raw(self):
        return os.environ
