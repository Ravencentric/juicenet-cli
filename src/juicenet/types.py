from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from typing_extensions import TypeAlias

NZBFilePath: TypeAlias = Path
PAR2FilePath: TypeAlias = Path
ArticleFilePath: TypeAlias = Path


@dataclass(order=True)
class NyuuOutput:
    nzb: Optional[NZBFilePath]
    success: bool
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


@dataclass(order=True)
class RawOutput:
    article: ArticleFilePath
    success: bool
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


@dataclass(order=True)
class ParParOutput:
    par2files: list[PAR2FilePath]
    filepathformat: Literal["basename", "path"]
    filepathbase: Path
    success: bool
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


@dataclass(order=True)
class JuicenetOutput:
    nyuu: Optional[NyuuOutput] = None
    raw: Optional[RawOutput] = None
    parpar: Optional[ParParOutput] = None


@dataclass(order=True)
class JuicenetOutputDict:
    filesdict: dict[Path, JuicenetOutput]
    articlesdict: Optional[dict[Path, JuicenetOutput]] = None
