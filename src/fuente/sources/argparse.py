from argparse import ArgumentParser, SUPPRESS
from typing import get_type_hints

from .flat import FlatSource


class ArgParseSource(FlatSource):
    def __init__(self, parser: ArgumentParser, args: list[str]):
        super().__init__(prefix="")
        self.args = args
        self.parser = parser
        self._parser_patched = False

    def _gen_key(self, prefix: str, path: list[str]):
        return prefix + "_".join(x.lower() for x in path)

    def _patch_parser(self):
        types = get_type_hints(self._type)
        for field, typehint in types.items():
            self.parser.add_argument("--" + field, dest=field,
                                     default=SUPPRESS)
        self._parser_patched = True

    def _load_raw(self):
        if not self._parser_patched:
            self._patch_parser()

        ns = self.parser.parse_args(self.args[1:])
        return vars(ns)
