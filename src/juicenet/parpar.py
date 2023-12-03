import subprocess
from pathlib import Path
from typing import Optional

from alive_progress import alive_it
from loguru import logger

from .enums import BarTitle, CurrentFile


class ParPar:
    """
    A class representing ParPar

    Attributes:
        - `bin (Path)`: The path to ParPar binary
        - `args (list[str])`: The list of arguments to be passed to ParPar
        - `workdir (Optional[Path])`: Path to the directory for ParPar execution and par2 file generation
        - `debug (bool)`:  Debug mode for extra logs

    Methods:
        - `map_filepath_formats(files: list[Path]) -> dict[Path, str]`: Checks if the path is a directory or file
           and maps it to the corresponding value of `--filepath-format` for ParPar.
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

    def generate_par2_files(self, files: list[Path]) -> None:
        """
        Generate .par2 files with ParPar
        """
        sink = None if self.debug else subprocess.DEVNULL

        bar = alive_it(files, title=BarTitle.PARPAR)

        format = self.map_filepath_formats(files)

        for file in bar:
            parpar = (
                [self.bin]
                + self.args
                + ["--filepath-base", file.parent, "--filepath-format", format[file]]
                + ["--out", file.name, file]
            )

            logger.debug(parpar)
            bar.text(f"{CurrentFile.PARPAR} {file.name}")

            cwd = self.workdir if self.workdir else file.parent  # this is where parpar will be executed
            subprocess.run(parpar, cwd=cwd, stdout=sink, stderr=sink)
