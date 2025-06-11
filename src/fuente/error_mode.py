from enum import Enum


class ErrorMode(Enum):
    SKIP_FIELD = "SKIP_FIELD"  # field skipped during parsing
    SKIP_SOURCE = "SKIP_SOURCE"  # source skipped on error
    FAIL_NOT_PARSED = "FAIL_NOT_PARSED"  # field has Special value
    FAIL_ALWAYS = "FAIL_ALWAYS"  # just nothing
