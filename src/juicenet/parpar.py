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
        - `path (Path)`: The path to the directory containing the files to be processed
        - `bin (Path)`: The path to ParPar binary
        - `args (list[str])`: The list of arguments to be passed to ParPar
        - `outdir (Optional[Path])`: The optional path to the output directory where ParPar will create par2 files,
           defaults to generating par2 right next to the files
        - `debug (bool)`:  Debug mode for extra logs

    Methods:
        - `map_filepath_formats(files: list[Path]) -> dict[Path, str]`: Checks if the path is a directory or file
           and maps it to the corresponding value of `--filepath-format` for ParPar.
        - `generate_par2_files(files: list[Path]) -> None`: Generates .par2 files with ParPar.

    This class is used to manage the generation of .par2 files using ParPar.
    """

    def __init__(self, path: Path, bin: Path, args: list[str], outdir: Optional[Path], debug: bool = False) -> None:
        self.path = path
        self.bin = bin
        self.args = args
        self.outdir = outdir
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
                mapping[file] = "outrel"

        return mapping

    def generate_par2_files(self, files: list[Path]) -> None:
        """
        Generate .par2 files with ParPar
        """
        sink = None if self.debug else subprocess.DEVNULL

        bar = alive_it(files, title=BarTitle.PARPAR)

        format = self.map_filepath_formats(files)

        for file in bar:
            # Generare par2 files in CWD if outdir is not specified
            outfile = file if self.outdir is None else self.outdir / file.name

            parpar = [self.bin] + self.args + ["--filepath-format", format[file]] + ["--out", outfile, file]

            logger.debug(parpar)
            bar.text(f"{CurrentFile.PARPAR} {file.name} (format: {format[file]})")

            subprocess.run(parpar, cwd=self.path, stdout=sink, stderr=sink)
