from collections import UserDict
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceType:
    name: str

@dataclass
class Marker:
    source_type: SourceType
    snippet: str | None

    def __str__(self):
        if self.snippet:
            return f"{self.source_type.name}\n{self.snippet}"
        return f"{self.source_type}"


@dataclass
class FileMarker(Marker):
    line: int | None
    column: int | None
    path: str | None

    def __str__(self):
        res = f"{self.source_type.name} {self.path!r}, line {self.line}"
        if self.snippet:
            res += f": {self.snippet.rstrip()}"
        return res

Path = Sequence[object]


class SrcMetadata(UserDict):
    def __getitem__(self, item: Path) -> Marker:
        for x in range(len(item), 0, -1):
            try:
                return self.data[item[:x]]
            except KeyError:
                continue
        raise KeyError(item)
