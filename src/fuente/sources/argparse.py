from argparse import SUPPRESS, ArgumentParser
from collections.abc import Iterable
from typing import get_type_hints

from adaptix import Retort

from .flat import FlatSource, FlatSourceLoader


class ArgParseSource(FlatSource):
    def __init__(
            self,
            *,
            parser: ArgumentParser,
            sep: str = "_",
            names: dict[str, Iterable[str]] | None = None,
    ):
        super().__init__(prefix="", sep=sep, names=names)
        self._parser = parser

    def _gen_key(self, prefix: str, path: list[str]):
        return prefix + "_".join(x.lower() for x in path)

    def _patch_parser(self, type_: type):
        types = get_type_hints(type_)
        for field, typehint in types.items():
            self._parser.add_argument(
                "--" + field.replace("_", "-"),
                dest=field,
                default=SUPPRESS,
            )

    def _make_loader(
            self,
            loading_retort: Retort,
            dumping_retort: Retort,
            config_type: type,
    ) -> FlatSourceLoader:
        self._patch_parser(config_type)
        return super()._make_loader(
            loading_retort=loading_retort,
            dumping_retort=dumping_retort,
            config_type=config_type,
        )

    def _load_raw(self):
        ns = self._parser.parse_args()
        return vars(ns)
