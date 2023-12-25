import glob
import shlex
import subprocess
from pathlib import Path
from typing import Optional
from uuid import uuid4

from alive_progress import alive_it
from loguru import logger

from .enums import BarTitle, CurrentFile


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

    def map_filepath_formats(self, files: list[Path]) -> dict[Path, str]:
        """
        Check if the path is a directory or file and map it to the
        corresponding value of `--filepath-format` for ParPar
        https://github.com/animetosho/ParPar/blob/master/help.txt#L118C39-L128

        This is required to preserve folder structure where it matters (BDMVs)
        OR discard folders where it does not (common mkv files)
        """
        mapping = {}

        for file in files:
            if file.is_file():
                mapping[file] = "basename"
            else:
                mapping[file] = "path"

        return mapping

    def get_workdir(self, file: Path) -> Path:
        """
        Get the working directory. This is where ParPar
        will be executed and `.par2` files will be generated

        Files can often have duplicate names when located in
        different folders. This isn't an issue if `.par2` files
        are being generated right next to the input file but can
        be a problem when using a seperate working and/or temporary
        directory. So I'll create unique folder names for this case.
        """
        if self.workdir:
            cwd = self.workdir / uuid4().hex.upper()[:10]
            cwd.mkdir(parents=True, exist_ok=True)
            return cwd
        else:
            return file.parent

    def generate_par2_files(self, files: list[Path]) -> dict[Path, list[Path]]:
        """
        Generate `.par2` files with ParPar and return a dictionary of the
        resulting `.par2` files where the key is the input file and value is
        a list of it's `.par2` files
        """
        sink = None if self.debug else subprocess.DEVNULL

        bar = alive_it(files, title=BarTitle.PARPAR)

        format = self.map_filepath_formats(files)

        file_to_par_mapping = {}

        for file in bar:
            parpar = (
                [self.bin]
                + self.args
                + ["--filepath-base", file.parent, "--filepath-format", format[file]]
                + ["--out", file.name, file]
            )

            logger.debug(shlex.join(str(arg) for arg in parpar))
            bar.text(f"{CurrentFile.PARPAR} {file.name}")

            # Get the working directory
            cwd = self.get_workdir(file)

            # Execute ParPar and generate `.par2` files
            subprocess.run(parpar, cwd=cwd, stdout=sink, stderr=sink)

            # Finally map the generated par2 files to the input file that they belong to
            file_to_par_mapping[file] = list(cwd.glob(f"{glob.escape(file.name)}*.par2"))

        return file_to_par_mapping
