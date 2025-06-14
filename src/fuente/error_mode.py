from enum import Enum


class ErrorMode(Enum):
    # field skipped during last parsing
    SKIP_FIELD = "SKIP_FIELD"
    # source skipped on error
    SKIP_SOURCE = "SKIP_SOURCE"
    # field has Special value, checked during last parsing
    FAIL_NOT_PARSED = "FAIL_NOT_PARSED"
    # just nothing
    FAIL_ALWAYS = "FAIL_ALWAYS"
