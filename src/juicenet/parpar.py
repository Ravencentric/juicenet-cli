import subprocess
from pathlib import Path

from alive_progress import alive_it
from loguru import logger

from .enums import BarTitle, CurrentFile


def map_filepath_formats(files: list[Path]) -> dict[Path, str]:
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


def gen_par2(path: Path, bin: Path, args: list[str], files: list[Path], debug: bool = False) -> None:
    """
    Generate .par2 files with ParPar
    """
    sink = None if debug else subprocess.DEVNULL

    bar = alive_it(files, title=BarTitle.PARPAR)

    format = map_filepath_formats(files)

    for file in bar:
        parpar = [bin] + args + ["--filepath-format", format[file]] + ["--out", file, file]

        logger.debug(parpar)
        bar.text(f"{CurrentFile.PARPAR} {file.name} (format: {format[file]})")

        subprocess.run(parpar, cwd=path, stdout=sink, stderr=sink)
