import glob
from pathlib import Path
from typing import Optional

from loguru import logger
from natsort import natsorted

from .types import PAR2FilePath


def get_files(path: Path, exts: list[str]) -> list[Path]:
    """
    Get all the files with the relevant extensions
    """
    files = []

    for ext in exts:
        matches = list(path.rglob(f"*.{ext.strip('.')}"))
        files.extend(matches)

    return natsorted(files)


def get_glob_matches(path: Path, patterns: list[str]) -> list[Path]:
    """
    Get files/folders in path matching the glob pattern
    """
    files = []

    for pattern in patterns:
        matches = list(path.glob(pattern))
        files.extend(matches)

    return natsorted(files)


def get_related_files(file: Path, exts: list[str]) -> Optional[list[Path]]:
    """
    Sometimes releasers include unmuxed files
    with their releases that are important
    such as unmuxed subtitles. These files usually
    share the same name as the original filename but with a
    different extension.

    We will simply glob all files that match the original
    filename, as these are usually intended to be watched
    together.
    """

    matching_files: set[Path] = set()

    # Grab all the files which share the exact name
    # BUT different suffix
    for ext in exts:
        matches = set(file.parent.rglob(f"{glob.escape(file.stem)}*.{ext.strip('.')}"))
        matching_files.update(matches)

    # These often satisfy the above conditions
    # but we don't want them
    junk = [".nzb", ".par2", ".torrent"]

    # Remove any items that aren't files or junk
    filtered = {
        match
        for match in matching_files
        if match.is_file()  # MUST be an existing file
        and match.suffix.lower() not in junk  # Extension MUST NOT be in junk extensions
        and match.name != file.name  # Filename MUST NOT be identical to input
    }

    # Remove the input file itself
    files = filtered - {file}

    if files:
        return natsorted(files)

    return None


def get_bdmv_discs(path: Path, patterns: list[str]) -> list[Path]:
    """
    Finds individual discs in BDMVs by looking for `BDMV/index.bdmv`

    The choice to use `BDMV/index.bdmv` is arbitrary,
    I just needed something unique enough.

    A typical BDMV might look like this:

    ```
    [BDMV] Big Buck Bunny [US]
    ├──  Big Buck Bunny [Vol.1]
    │   └── DISC_01
    │       └── BDMV
    │           ├── BACKUP
    │           ├── CLIPINF
    │           ├── META
    │           ├── PLAYLIST
    │           ├── index.bdmv
    │           └── MovieObject.bdmv
    └── Big Buck Bunny [Vol.2]
        └── DISC_01
            └── BDMV
                ├── BACKUP
                ├── CLIPINF
                ├── META
                ├── PLAYLIST
                ├── index.bdmv
                └── MovieObject.bdmv
    ```
    From the above example, this function finds the
    `BDMV/index.bdmv` file and then goes 1 directory up
    relative to `BDMV/index.bdmv` which ends up being `DISC_01`

    Practical Examples:

    - Found:
        - `Big Buck Bunny [Vol.1]/DISC_01/BDMV/index.bdmv`
        - `Big Buck Bunny [Vol.2]/DISC_01/BDMV/index.bdmv`

    - Return:
        - `Big Buck Bunny [Vol.1]/DISC_01`
        - `Big Buck Bunny [Vol.2]/DISC_01`

    """

    bdmvs = []

    folders = get_glob_matches(path, patterns)

    for folder in folders:
        if folder.is_dir():
            index = list(folder.rglob("BDMV/index.bdmv"))
            for file in index:
                bdmvs.append(file.parents[1])
                logger.info(f"BDMV: {file.parents[1].relative_to(path)}")

    return natsorted(bdmvs)


def get_dvd_discs(path: Path, patterns: list[str]) -> list[Path]:
    """
    Finds individual discs in DVDs by looking for `VIDEO_TS/VIDEO_TS.VOB`

    The choice to use `VIDEO_TS/VIDEO_TS.VOB` is arbitrary,
    I just needed something unique enough.

    A typical DVD might look like this:

    ```
    Cowboy.Bebop.1998.DVDR.NTSC.R4.LATiNO
    ├── COWBOY_BEBOP_1
    │   └── VIDEO_TS
    │       ├── VIDEO_TS.BUP
    │       ├── VIDEO_TS.IFO
    │       └── VIDEO_TS.VOB
    └── COWBOY_BEBOP_2
        └── VIDEO_TS
            ├── VIDEO_TS.BUP
            ├── VIDEO_TS.IFO
            └── VIDEO_TS.VOB
    ```
    From the above example, this function finds the
    `VIDEO_TS/VIDEO_TS.VOB` file and then goes 1 directory up
    relative to `VIDEO_TS/VIDEO_TS.VOB` which ends up being `COWBOY_BEBOP_1`

    Practical Examples:

    - Found:
        - `Cowboy.Bebop.1998.DVDR.NTSC.R4.LATiNO/COWBOY_BEBOP_1/VIDEO_TS/VIDEO_TS.VOB`
        - `Cowboy.Bebop.1998.DVDR.NTSC.R4.LATiNO/COWBOY_BEBOP_2/VIDEO_TS/VIDEO_TS.VOB`

    - Return:
        - `Cowboy.Bebop.1998.DVDR.NTSC.R4.LATiNO/COWBOY_BEBOP_1`
        - `Cowboy.Bebop.1998.DVDR.NTSC.R4.LATiNO/COWBOY_BEBOP_2`

    """

    dvds = []

    folders = get_glob_matches(path, patterns)

    for folder in folders:
        if folder.is_dir():
            for file in folder.rglob("*"):
                if (
                    file.is_file()
                    and file.name.casefold().strip() in ("video_ts.vob", "video_ts.ifo", "video_ts.bup")
                    and file.parent.name.casefold().strip() == "video_ts"
                ):
                    dvds.append(file.parents[1])
                    logger.info(f"DVD: {file.parents[1].relative_to(path)}")

    return natsorted(dvds)


def get_file_info(file: Path) -> dict[str, str]:
    """
    Get the name, total size, and number of file(s) given a Path

    Returns `{"name": str, "size": str, "count": str}`

    `size` and `count` are string for easier comparison when reading
    these from a csv file
    """

    if file.is_file():
        size = str(file.stat().st_size)
        count = "1"
        return dict(name=file.name, size=size, count=count)

    else:  # it's a directory
        all_files = tuple(file.rglob("*"))
        count = str(len(all_files))
        size = str(sum(f.stat().st_size for f in all_files if f.is_file()))
        return dict(name=file.name, size=size, count=count)


def filter_par2_files(files: list[Path]) -> list[Path]:
    """
    Filter out any `.par2` files present in the given
    list of path. There's no reason to process these.
    """

    filtered = []

    for file in files:
        if not file.suffix.lower() == ".par2":
            filtered.append(file)

    return natsorted(filtered)


def filter_empty_files(files: list[Path]) -> list[Path]:
    """
    Filter out empty files and directories from a list of paths

    - Empty file is a file whose size is 0 bytes
    - Empty directory is a directory with 0 non empty files

    This step is necessary because Nyuu will skip empty files
    on it's own but `Nyuu.upload()` expects an nzb for every
    file passed. So I'll remove these before passing
    it further in the script.
    """
    filtered = []

    for file in files:
        if file.is_file() and file.stat().st_size > 0:
            filtered.append(file)

        elif file.is_dir():
            for item in list(file.rglob("*")):
                if item.is_file() and item.stat().st_size > 0:
                    filtered.append(file)
                    break

    return natsorted(filtered)


def map_file_to_pars(basedir: Optional[Path], files: list[Path]) -> dict[Path, list[PAR2FilePath]]:
    """
    For each file, get it's corresponding .par2 files as such:

    `{'foo/01.ext': ['foo/01.ext.par2', 'foo/01.ext.vol12+10.par2', ...]}`
    """
    mapping = {}

    for file in files:
        parent = file.parent if basedir is None else basedir
        par2_files = []
        # The first par2 file doesn't have the word `vol` in it
        first_par2_file = parent / f"{file.name}.par2"
        if first_par2_file.is_file():
            par2_files.append(first_par2_file)

        # Rest of the par2 files strictly follow the `foobar.mkv.vol01+02.par2` naming scheme
        par2_files.extend(list(parent.glob(f"{glob.escape(file.name)}.vol*.par2")))
        mapping[file] = natsorted(par2_files)

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


def delete_files(files: list[Path]) -> None:
    """
    Delete the files in the given list
    """
    for file in files:
        file.unlink(missing_ok=True)
        try:
            # Attempt to remove the parent dir
            # if and only if it's empty
            file.parent.rmdir()
        except FileNotFoundError:  # Doesn't Exist
            pass
        except OSError:  # Not empty
            pass
