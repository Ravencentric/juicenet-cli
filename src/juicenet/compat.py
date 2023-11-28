import sys

if sys.version_info[0:2] < (3, 11):
    import tomli as tomllib
    from strenum import StrEnum
    from typing_extensions import NotRequired, TypedDict
else:
    from enum import StrEnum
    from typing import NotRequired, TypedDict

    import tomllib

if sys.version_info[0:2] < (3, 10):
    import importlib_metadata as metadata
else:
    from importlib import metadata

__all__ = ["metadata", "tomllib", "StrEnum", "NotRequired", "TypedDict"]
