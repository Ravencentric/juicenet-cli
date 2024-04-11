from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from typing import Annotated, Optional

from pydantic import BaseModel, DirectoryPath, Field, FilePath, field_validator


# fmt: off
class JuicenetConfig(BaseModel):
    """
    Pydantic model for setting defaults and validating Juicenet's config

    Attributes
    ----------
    parpar : FilePath
        The path to the ParPar executable
    nyuu : FilePath
        The path to the Nyuu executable
    nyuu_config_private : FilePath
        The path to the private Nyuu configuration file
    nzb_output_path : DirectoryPath
        The path where output NZBs will be saved
    nyuu_config_public : FilePath, optional
        The path to the public Nyuu configuration file
    extensions : list[str], optional
        The list of file extensions to be processed. Default is `["mkv"]`
    related_extensions : list[str], optional
        The list of file extensions associated with an input file.
        For example, if you have a file named `Big Buck Bunny The Movie (2023).mkv`,
        another file named `Big Buck Bunny The Movie (2023).srt` is considered related.
        Default is `["*"]`
    parpar_args : list[str], optional
        The arguments to be passed to the ParPar executable
        Ddefault is `["--overwrite", "-s700k", "--slice-size-multiple=700K", "--max-input-slices=4000", "-r1n*1.2", "-R"]`
    use_temp_dir : bool, optional
        Whether or not to use a temporary directory for processing. Default is `True`
    temp_dir_path : DirectoryPath, optional
        Path to a specific temporary directory if `use_temp_dir` is `True`. If unspecified, it uses `%Temp%` or `/tmp`
    appdata_dir_path : Path, optional
        The path to the folder where Juicenet will store its data. Default is `~/.juicenet`
    """

    parpar: Annotated[FilePath, Field(validate_default=True)] = which("parpar") # type: ignore
    """The path to the ParPar executable"""

    nyuu: Annotated[FilePath, Field(validate_default=True)] = which("nyuu") # type: ignore
    """The path to the Nyuu executable"""

    nyuu_config_private: FilePath
    """The path to the private Nyuu configuration file"""

    nzb_output_path: DirectoryPath
    """The path where output NZBs will be saved"""

    nyuu_config_public: Optional[FilePath] = None
    """The path to the public Nyuu configuration file"""

    extensions: list[str] = ["mkv"]
    """The list of file extensions to be processed"""

    related_extensions: list[str] = ["ass", "srt"]
    """
    The list of file extensions associated with an input file. 
    For example, if you have a file named `Big Buck Bunny The Movie (2023).mkv`, 
    another file named `Big Buck Bunny The Movie (2023).srt` is considered related
    """

    parpar_args: list[str] = ["--overwrite", "-s700k", "--slice-size-multiple=700K", "--max-input-slices=4000", "-r1n*1.2", "-R"]
    """The arguments to be passed to the ParPar executable"""

    use_temp_dir: bool = True
    """Whether or not to use a temporary directory for processing"""

    temp_dir_path: DirectoryPath = Path(TemporaryDirectory(prefix=".JUICENET_").name).resolve()
    """Path to a specific temporary directory if use_temp_dir is True. If unspecified, it uses %Temp% or /tmp"""

    appdata_dir_path: Path = Path.home() / ".juicenet"
    """The path to the folder where juicenet will store it's data"""

    @field_validator("parpar", "nyuu", "nyuu_config_private", "nzb_output_path", "nyuu_config_public", "temp_dir_path", "appdata_dir_path")
    @classmethod
    def resolve_path(cls, path: Path) -> Path:
            """Resolve all given Path fields"""
            return path.expanduser().resolve()
