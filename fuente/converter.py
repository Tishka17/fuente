from dataclasses import fields, is_dataclass
from typing import TypedDict


def to_cfg_model(model: type):
    if not is_dataclass(model):
        return model
    all_fields: dict[str, type] = {}
    for field in fields(model):
        all_fields[field.name] = to_cfg_model(field.type)

    return TypedDict(model.__name__ + "_td", all_fields, total=False)
