import sys

if sys.version_info[0:2] < (3, 11):
    from strenum import StrEnum
else:
    from enum import StrEnum


if sys.version_info[0:2] < (3, 10):
    import importlib_metadata as metadata
else:
    from importlib import metadata

__all__ = ["metadata", "StrEnum"]
