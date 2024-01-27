from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from typing import Annotated, Optional

from pydantic import BaseModel, DirectoryPath, Field, FilePath, field_validator


# fmt: off
class JuicenetConfig(BaseModel):
    """Pydantic model for setting defaults and validating juicenet's config"""

    PARPAR: Annotated[FilePath, Field(validate_default=True)] = which("parpar") # type: ignore
    """The path to the ParPar binary"""

    NYUU: Annotated[FilePath, Field(validate_default=True)] = which("nyuu") # type: ignore
    """The path to the Nyuu binary"""

    NYUU_CONFIG_PRIVATE: FilePath
    """The path to the private Nyuu configuration file"""

    NZB_OUTPUT_PATH: DirectoryPath
    """The path where output NZBs will be saved"""

    NYUU_CONFIG_PUBLIC: Optional[FilePath] = None
    """The path to the public Nyuu configuration file"""

    EXTENSIONS: list[str] = ["mkv"]
    """The list of file extensions to be processed"""

    PARPAR_ARGS: list[str] = ["--overwrite", "-s700k", "--slice-size-multiple=700K", "--max-input-slices=4000", "-r1n*1.2", "-R"]
    """The arguments to be passed to the ParPar binary"""

    USE_TEMP_DIR: bool = True
    """Whether or not to use a temporary directory for processing"""

    TEMP_DIR_PATH: DirectoryPath = Path(TemporaryDirectory(prefix=".JUICENET_").name).resolve()
    """Path to a specific temporary directory if USE_TEMP_DIR is True. If unspecified, it uses %Temp% or /tmp"""

    APPDATA_DIR_PATH: Path = Path.home() / ".juicenet"
    """The path to the folder where juicenet will store it's data"""

    @field_validator("PARPAR", "NYUU", "NYUU_CONFIG_PRIVATE", "NZB_OUTPUT_PATH", "NYUU_CONFIG_PUBLIC", "TEMP_DIR_PATH", "APPDATA_DIR_PATH")
    @classmethod
    def resolve_path(cls, path: Path) -> Path:
            """Resolve all given Path fields"""
            return path.resolve()
