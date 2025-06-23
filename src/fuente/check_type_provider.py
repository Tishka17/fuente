from adaptix import loader
from adaptix._internal.morphing.load_error import TypeLoadError


def check_type_loader(cls):
    def as_is_stub(data):
        if type(data) is cls:
            return data
        raise TypeLoadError(
            expected_type=cls,
            input_value=data,
        )
    return loader(cls, as_is_stub)
