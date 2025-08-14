from typing import Any

from ruamel.yaml import YAML, Node

from fuente.entities import FileMarker, SourceType, SrcMetadata
from fuente.error_mode import ErrorMode
from fuente.protocols import (
    ConfigDictT,
    ConfigSourceLoader,
    ConfigT,
    ConfigWrapper,
    Source,
)


class YamlSourceLoader(ConfigSourceLoader):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def load(self):
        root, lines = self.raw_load()
        metadata = SrcMetadata()
        self.walk(root, lines, metadata)
        return ConfigWrapper(
            config=root,
            metadata=metadata,
        )

    def raw_load(self) -> tuple[Node, list[str]]:
        yaml = YAML()
        with open(self._filepath) as f:
            lines = f.readlines()
            f.seek(0)
            root = yaml.load(f)
        return root, lines

    def walk(
        self,
        node: Any,
        source_lines,
        metadata: SrcMetadata,
        path=(),
        marker: FileMarker | None = None,
    ) -> None:
        if hasattr(node, "lc"):
            if isinstance(node, dict):
                for key, value in node.items():
                    val_line, val_column = node.lc.value(key)
                    marker = FileMarker(
                        source_type=SourceType("yaml"),
                        path="config.yaml",
                        line=val_line,
                        column=val_column,
                        snippet=source_lines[val_line],
                    )
                    self.walk(value, source_lines, path + (key,), marker)
                return
            elif isinstance(node, list):
                for idx, item in enumerate(node):
                    item_line, item_col = node.lc.item(idx)
                    marker = FileMarker(
                        source_type=SourceType("yaml"),
                        path="config.yaml",
                        line=item_line,
                        column=item_col,
                        snippet=source_lines[item_line],
                    )
                    self.walk(item, source_lines, path + (idx,), marker)
                return
        metadata[path] = marker


class YamlSource(Source):
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def make_loader(
        self, config_type: ConfigT, error_mode: ErrorMode,
    ) -> ConfigSourceLoader[ConfigDictT]:
        return YamlSourceLoader(filepath=self._filepath)
