import os

from adaptix import Retort

from .flat import FlatSource, FlatSourceLoader


class EnvSourceLoader(FlatSourceLoader):
    def _load_raw(self):
        return os.environ


class EnvSource(FlatSource):
    def _make_loader(
            self,
            loading_retort: Retort,
            dumping_retort: Retort,
            config_type: type,
    ) -> FlatSourceLoader:
        return EnvSourceLoader(
            loading_retort=loading_retort,
            dumping_retort=dumping_retort,
            config_type=config_type,
        )
