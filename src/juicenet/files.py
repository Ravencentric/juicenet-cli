import glob
from pathlib import Path
from typing import Optional

from loguru import logger


def get_files(path: Path, exts: list[str]) -> list[Path]:
    """
    Get all the files with the relevant extensions
    """
    files = []

    for ext in exts:
        matches = list(path.rglob(f"*.{ext.strip('.')}"))
        files.extend(matches)

    return files


def get_glob_matches(path: Path, patterns: list[str]) -> list[Path]:
    """
    Get files/folders in path matching the glob pattern
    """
    files = []

    for pattern in patterns:
        matches = list(path.glob(pattern))
        files.extend(matches)

    return files


def rm_empty_paths(files: list[Path]) -> list[Path]:
    """
    Removes empty files and directories from a list of paths

    Empty file is a file whose size is 0 bytes
    Empty directory is a directory with 0 non empty files

    This step is necessary because Nyuu will skip empty paths
    on it's own but the script expects an nzb for each path
    causing it to error. So I'll remove these before passing
    it further in the script.
    """
    non_empty = []

    for file in files:
        if file.is_file() and file.stat().st_size > 0:
            non_empty.append(file)

        elif file.is_dir():
            for item in list(file.rglob("*")):
                if item.is_file() and item.stat().st_size > 0:
                    non_empty.append(file)
                    break

    return non_empty


def map_file_to_pars(basedir: Optional[Path], files: list[Path]) -> dict[Path, list[Path]]:
    """
    For each file, get it's corresponding .par2 files as such:

    `{'foo/01.ext': ['foo/01.ext.par2', 'foo/01.ext.vol12+10.par2', ...]}`
    """
    mapping = {}

    for file in files:
        parent = file.parent if basedir is None else basedir
        par2_files = []
        par2_files.append(parent / f"{file.name}.par2")
        par2_files.extend(list(parent.glob(f"{glob.escape(file.name)}.vol*.par2")))
        mapping[file] = par2_files

    return mapping


def move_files(files: list[Path]) -> None:
    """
    Moves files into their own directories
    Example: foo/01.mkv -> foo/01/01.mkv
    """
    for src in files:
        if src.is_file():  # ./foo/01.mkv
            dst = src.parent / src.stem  # ./foo/01/
            dst.mkdir(parents=True, exist_ok=True)
            dst = dst / src.name  # ./foo/01/01.mkv
            src.rename(dst)  # ./foo/01.mkv -> ./foo/01/01.mkv

            logger.debug(f"File Move: {src} -> {dst}")
