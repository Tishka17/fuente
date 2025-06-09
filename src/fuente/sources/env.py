import os

from .flat import FlatSource


class EnvSource(FlatSource):
    def _load_raw(self):
        return os.environ
