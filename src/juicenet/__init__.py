"""
Library designed to simplify the process of uploading files to Usenet.

One for All Function
--------------------
- juicenet

Helper Functions
----------------
- get_files
- get_bdmv_discs
- get_dvd_discs
- get_glob_matches

Types
-----
- JuicenetConfig
- ArticleFilePath
- JuiceBox
- NyuuOutput
- NZBFilePath
- PAR2FilePath
- ParParOutput
- RawOutput
"""

from .api.main import juicenet
from .api.utils import get_bdmv_discs, get_dvd_discs, get_files, get_glob_matches
from .model import JuicenetConfig
from .types import (
    ArticleFilePath,
    JuiceBox,
    NyuuOutput,
    NZBFilePath,
    PAR2FilePath,
    ParParOutput,
    RawOutput,
)
from .version import get_version

__all__ = [
    # main
    "juicenet",
    # helpers
    "get_files",
    "get_bdmv_discs",
    "get_dvd_discs",
    "get_glob_matches",
    # types
    "JuicenetConfig",
    "ArticleFilePath",
    "JuiceBox",
    "NyuuOutput",
    "NZBFilePath",
    "PAR2FilePath",
    "ParParOutput",
    "RawOutput",
]

__version__ = get_version()
