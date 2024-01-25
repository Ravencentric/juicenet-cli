from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from typing_extensions import TypeAlias

NZBFilePath: TypeAlias = Path
PAR2FilePath: TypeAlias = Path
ArticleFilePath: TypeAlias = Path


@dataclass(order=True)
class NyuuOutput:
    """
    A class used to represent the output of the Nyuu subprocess.

    Attributes
    ----------
    nzb : NZBFilePath, optional
        Absolute pathlib.Path to the resulting `NZB` file or `None` if the upload failed.
    success : bool
        `True` if Nyuu exited successfully with code 0 or 32, `False` otherwise.
    args : list[str]
        List of arguments passed to Nyuu.
    returncode : int
        Nyuu's exit code.
    stdout : str
        Nyuu's stdout.
    stderr : str
        Nyuu's stderr.
    """

    nzb: Optional[NZBFilePath]
    """Absolute pathlib.Path to the resulting `NZB` file or `None` if the upload failed."""

    success: bool
    """`True` if Nyuu exited successfully with code 0 or 32, `False` otherwise."""

    args: list[str]
    """List of arguments passed to Nyuu."""

    returncode: int
    """Nyuu's exit code."""

    stdout: str
    """Nyuu's stdout."""

    stderr: str
    """Nyuu's stderr."""


@dataclass(order=True)
class RawOutput:
    """
    A class used to represent the output of the raw article upload process.

    Attributes
    ----------
    article : ArticleFilePath
        Absolute pathlib.Path to the raw article.
    success : bool
        `True` if Nyuu exited successfully with code 0 or 32, `False` otherwise.
    args : list[str]
        List of arguments passed to Nyuu.
    returncode : int
        Nyuu's exit code.
    stdout : str
        Nyuu's stdout.
    stderr : str
        Nyuu's stderr.
    """

    article: ArticleFilePath
    """Absolute pathlib.Path to the raw article"""

    success: bool
    """`True` if Nyuu exited successfully with code 0 or 32, `False` otherwise."""

    args: list[str]
    """List of arguments passed to Nyuu."""

    returncode: int
    """Nyuu's exit code."""

    stdout: str
    """Nyuu's stdout."""

    stderr: str
    """Nyuu's stderr."""


@dataclass(order=True)
class ParParOutput:
    """
    A class used to represent the output of the ParPar subprocess.

    Attributes
    ----------
    par2files : list[PAR2FilePath]
        List of absolute pathlib.Path objects pointing to the generated `PAR2` files.
    filepathformat : Literal["basename", "path"]
        The `--filepath-format` used to generate the `PAR2` files.
    filepathbase : Path
        The `--filepath-base` used to generate the `PAR2` files.
    success : bool
        `True` if ParPar exited successfully with code 0, `False` otherwise.
    args : list[str]
        List of arguments passed to ParPar.
    returncode : int
        ParPar's exit code.
    stdout : str
        ParPar's stdout.
    stderr : str
        ParPar's stderr.
    """

    par2files: list[PAR2FilePath]
    """List of absolute pathlib.Path objects pointing to the generated `PAR2` files."""

    filepathformat: Literal["basename", "path"]
    """The `--filepath-format` used to generate the `PAR2` files"""

    filepathbase: Path
    """The `--filepath-base` used to generate the `PAR2` files"""

    success: bool
    """`True` if ParPar exited successfully with code 0, `False` otherwise."""

    args: list[str]
    """List of arguments passed to ParPar."""

    returncode: int
    """ParPar's exit code."""

    stdout: str
    """ParPar's stdout."""

    stderr: str
    """ParPar's stderr."""


@dataclass(order=True)
class SubprocessOutput:
    """
    A class used to represent the combined output of the Nyuu, Raw, and ParPar subprocesses for every processed file or article.
    Each attribute in this class is an instance of the corresponding output class (`NyuuOutput`, `RawOutput`, `ParParOutput`) and
    captures the output of the respective subprocess. If the output for a particular subprocess is not available,
    the corresponding attribute will be None.

    Attributes
    ----------
    nyuu : NyuuOutput, optional
        juicenet.types.NyuuOutput object for the processed file or `None` if not available.
    raw : RawOutput, optional
        juicenet.types.RawOutput object for the processed file or `None` if not available.
    parpar : ParParOutput, optional
        juicenet.types.ParParOutput object for the processed file or `None` if not available.

    """

    nyuu: Optional[NyuuOutput] = None
    """juicenet.types.NyuuOutput object for the processed file or `None` if not available"""

    raw: Optional[RawOutput] = None
    """juicenet.types.RawOutput object for the processed file or `None` if not available"""

    parpar: Optional[ParParOutput] = None
    """juicenet.types.ParParOutput object for the processed file or `None` if not available"""


@dataclass(order=True)
class JuicenetOutput:
    """
    A class used to represent the output of Juicenet.

    Attributes
    ----------
    files : dict[Path, SubprocessOutput], optional
        A dictionary where each key is a file path (as a pathlib.Path object),
        and the corresponding value is a juicenet.types.SubprocessOutput object.
        The SubprocessOutput object contains the outputs of Nyuu, Raw, and ParPar related to that file.
        If there are no files processed, this attribute is `None`.
    articles : dict[Path, SubprocessOutput], optional
        A dictionary where each key is an article path (as a Path object),
        and the corresponding value is a juicenet.types.SubprocessOutput object. object.
        The SubprocessOutput object contains the outputs of Nyuu, Raw, and ParPar related to that article.
        If there are no articles processed, this attribute is `None`.
    """

    files: Optional[dict[Path, SubprocessOutput]] = None
    """
    A dictionary where each key is a file path (as a pathlib.Path object), 
    and the corresponding value is a juicenet.types.SubprocessOutput object. 
    The SubprocessOutput object contains the outputs of Nyuu, Raw, and ParPar related to that file. 
    If there are no files processed, this attribute is `None`.
    """

    articles: Optional[dict[Path, SubprocessOutput]] = None
    """
    A dictionary where each key is an article path (as a Path object), 
    and the corresponding value is a juicenet.types.SubprocessOutput object. object. 
    The SubprocessOutput object contains the outputs of Nyuu, Raw, and ParPar related to that article. 
    If there are no articles processed, this attribute is `None`.
    """
