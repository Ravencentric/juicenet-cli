import glob
import shlex
import subprocess
from pathlib import Path
from typing import Literal, Optional
from uuid import uuid4

from loguru import logger

from .types import ParParOutput


class ParPar:
    """
    A class representing ParPar.

    Attributes:
        - `bin (Path)`: The path to ParPar binary.
        - `args (list[str])`: The list of arguments to be passed to ParPar.
        - `workdir (Optional[Path])`: Path to the directory for ParPar execution and par2 file generation.
        - `debug (bool)`:  Debug mode for extra logs.

    Methods:
        - `map_filepath_formats(files: list[Path]) -> dict[Path, str]`: Checks if the path is a directory or file
           and maps it to the corresponding value of `--filepath-format` for ParPar.
        - `get_workdir(self, file: Path) -> Path`: Get the working directory. This is where ParPar
           will be executed and `.par2` files will be generated.
        - `generate_par2_files(files: list[Path]) -> None`: Generates .par2 files with ParPar.

    This class is used to manage the generation of .par2 files using ParPar.
    """

    def __init__(self, bin: Path, args: list[str], workdir: Optional[Path], debug: bool = False) -> None:
        self.bin = bin
        self.args = args
        self.workdir = workdir
        self.debug = debug

    @staticmethod
    def _get_filepath_format(file: Path) -> Literal["basename", "path"]:
        """
        Check if the path is a directory or file and map it to the
        corresponding value of `--filepath-format` for ParPar
        https://github.com/animetosho/ParPar/blob/master/help.txt#L118C39-L128

        This is required to preserve folder structure where it matters (BDMVs)
        OR discard folders where it does not (common mkv files)
        """
        if file.is_file():
            return "basename"
        else:
            return "path"

    def _get_workdir(self, file: Path) -> Path:
        """
        Get the working directory. This is where ParPar
        will be executed and `.par2` files will be generated

        Files can often have duplicate names when located in
        different folders. This isn't an issue if `.par2` files
        are being generated right next to the input file but can
        be a problem when using a seperate working and/or temporary
        directory. So this'll create unique folder names for this case.
        """
        if self.workdir:
            cwd = self.workdir / uuid4().hex.upper()[:10]
            cwd.mkdir(parents=True, exist_ok=True)
            return cwd
        else:
            return file.parent

    def generate_par2_files(self, file: Path) -> ParParOutput:
        """
        Generate `.par2` files with ParPar and return a dictionary of the
        resulting `.par2` files where the key is the input file and value is
        a list of it's `.par2` files
        """
        capture_output = not self.debug

        filepathformat = self._get_filepath_format(file)
        filepathbase = file.parent

        parpar = (
            [self.bin]
            + self.args
            + ["--filepath-base", filepathbase, "--filepath-format", filepathformat]
            + ["--out", file.name, file]
        )

        logger.debug(shlex.join(str(arg) for arg in parpar))

        # Get the working directory
        cwd = self._get_workdir(file)

        # Execute ParPar and generate `.par2` files
        process = subprocess.run(parpar, cwd=cwd, capture_output=capture_output, encoding="utf-8")

        if process.returncode == 0:
            return ParParOutput(
                par2files=list(cwd.glob(f"{glob.escape(file.name)}*.par2")),
                filepathformat=filepathformat,
                filepathbase=filepathbase,
                success=True,
                args=process.args,
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )
        else:
            return ParParOutput(
                par2files=list(cwd.glob(f"{glob.escape(file.name)}*.par2")),
                filepathformat=filepathformat,
                filepathbase=filepathbase,
                success=False,
                args=process.args,
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )
