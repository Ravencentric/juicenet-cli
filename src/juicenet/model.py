from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from typing import Annotated, Optional

from pydantic import BaseModel, DirectoryPath, Field, FilePath, field_validator


# fmt: off
class JuicenetConfig(BaseModel):
    """Pydantic model for setting defaults and validating juicenet's config"""

    parpar: Annotated[FilePath, Field(validate_default=True)] = which("parpar") # type: ignore
    """The path to the ParPar binary"""

    nyuu: Annotated[FilePath, Field(validate_default=True)] = which("nyuu") # type: ignore
    """The path to the Nyuu binary"""

    nyuu_config_private: FilePath
    """The path to the private Nyuu configuration file"""

    nzb_output_path: DirectoryPath
    """The path where output NZBs will be saved"""

    nyuu_config_public: Optional[FilePath] = None
    """The path to the public Nyuu configuration file"""

    extensions: list[str] = ["mkv"]
    """The list of file extensions to be processed"""

    related_extensions: list[str] = ["*"]
    """
    The list of file extensions associated with an input file. 
    For example, if you have a file named `Big Buck Bunny The Movie (2023).mkv`, 
    another file named `Big Buck Bunny The Movie (2023).srt` is considered related
    """

    parpar_args: list[str] = ["--overwrite", "-s700k", "--slice-size-multiple=700K", "--max-input-slices=4000", "-r1n*1.2", "-R"]
    """The arguments to be passed to the ParPar binary"""

    use_temp_dir: bool = True
    """Whether or not to use a temporary directory for processing"""

    temp_dir_path: DirectoryPath = Path(TemporaryDirectory(prefix=".JUICENET_").name).resolve()
    """Path to a specific temporary directory if USE_TEMP_DIR is True. If unspecified, it uses %Temp% or /tmp"""

    appdata_dir_path: Path = Path.home() / ".juicenet"
    """The path to the folder where juicenet will store it's data"""

    @field_validator("parpar", "nyuu", "nyuu_config_private", "nzb_output_path", "nyuu_config_public", "temp_dir_path", "appdata_dir_path")
    @classmethod
    def resolve_path(cls, path: Path) -> Path:
            """Resolve all given Path fields"""
            return path.expanduser().resolve()
