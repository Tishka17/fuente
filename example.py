from dataclasses import dataclass

from fuente import parse
from fuente.merger import TypedDictMerge, UseLast, Concat

@dataclass
class A:
    a: int
    b: str
    c: int

source1 = {"a": 1, "b": "x", "c": 2, "d": "skip"}
source2 = {"a": 2, "b": "y"}


merger = TypedDictMerge({"a": UseLast(), "b": Concat()})
res = parse(source1, source2, merger=merger, type=A)

print(res)
