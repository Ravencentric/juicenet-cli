from pathlib import Path

from ..exceptions import JuicenetInputError
from ..types import StrPath
from ..utils import get_bdmv_discs as _get_bdmv_discs
from ..utils import get_dvd_discs as _get_dvd_discs


def get_files(path: StrPath, /, *, exts: list[str] = ["mkv"]) -> list[Path]:
    """
    Get a list of files with specified extensions from the given path. This is recursive.

    Parameters
    ----------
    path : str or pathlib.Path
        The path to an existing file. This can either be a string representing the path or a pathlib.Path object.
    exts : list[str], optional
        List of file extensions to match. Default will match all `mkv` files in base path.

    Returns
    -------
    list[Path]
        A list of Path objects representing the files with the specified extensions.

    Raises
    ------
    JuicenetInputError
        Invalid input.

    Examples
    --------
    >>> get_files(Path('/path/to/directory'))
    [PosixPath('/path/to/directory/Big Buck Bunny S01E01.mkv'), PosixPath('/path/to/directory/Big Buck Bunny S01E02.mkv')]

    >>> get_files(Path('/path/to/directory'), ['txt', 'csv'])
    [PosixPath('/path/to/directory/file1.txt'), PosixPath('/path/to/directory/file2.csv')]
    """

    if isinstance(path, str):
        basepath = Path(path).resolve()
    elif isinstance(path, Path):
        basepath = path.resolve()
    else:
        raise JuicenetInputError(f"{path} must be a string or pathlib.Path")

    if not basepath.is_dir():
        raise JuicenetInputError(f"{basepath} must be an directory")

    files = []

    for ext in exts:
        matches = list(basepath.rglob(f"*.{ext.strip('.')}"))
        files.extend(matches)

    return files


def get_glob_matches(path: Path, /, *, globs: list[str] = ["*.mkv"]) -> list[Path]:
    """
    Get a list of files which match at least one of the given glob patterns in the specified path.

    Parameters
    ----------
    path : Path or str
        The path to an existing directory. This can either be a string representing the path or a pathlib.Path object.
    globs : list[str], optional
        List of glob patterns to match. Default will match all `mkv` files in the base path.

    Returns
    -------
    list[Path]
        A list of Path objects representing the files matching the given glob patterns.

    Raises
    ------
    JuicenetInputError
        Invalid input.

    Examples
    --------
    >>> get_glob_matches(Path('/path/to/directory'))
    [PosixPath('/path/to/directory/Big Buck Bunny S01E01.mkv'), PosixPath('/path/to/directory/Big Buck Bunny S01E02.mkv')]

    >>> get_glob_matches(Path('/path/to/directory'), globs=['*.txt', '*.csv'])
    [PosixPath('/path/to/directory/file1.txt'), PosixPath('/path/to/directory/file2.csv')]
    """

    if isinstance(path, str):
        basepath = Path(path).resolve()
    elif isinstance(path, Path):
        basepath = path.resolve()
    else:
        raise JuicenetInputError(f"{path} must be a string or pathlib.Path")

    if not basepath.is_dir():
        raise JuicenetInputError(f"{basepath} must be an directory")

    files = []

    for glob in globs:
        matches = list(basepath.glob(glob))
        files.extend(matches)

    return files


def get_bdmv_discs(path: StrPath, globs: list[str] = ["*/"]) -> list[Path]:
    """
    Finds individual discs in BDMVs by looking for `BDMV/index.bdmv`.

    Parameters
    ----------
    path : str or pathlib.Path
        The path to an existing file. This can either be a string representing the path or a pathlib.Path object.
    globs : list[str], optional
        List of glob patterns to match. Default will match all sub folders in base path.

    Returns
    -------
    list[Path]
        List of paths where each path is a BDMV disc.

    Raises
    ------
    JuicenetInputError
        Invalid input.

    Notes
    -----
    The choice to use `BDMV/index.bdmv` is arbitrary,
    I just needed something unique enough.

    There's two aspects to it, if the BDMV has multiple `BDMV/index.bdmv` files
    it means it's got multiple discs and each disc will be returned seperately
    and if there's only one `BDMV/index.bdmv` then return the folder as is
    because it's likely a movie BDMV

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

    Something like:

    - Found:
        - `Big Buck Bunny [Vol.1]/DISC_01/BDMV/index.bdmv`
        - `Big Buck Bunny [Vol.2]/DISC_01/BDMV/index.bdmv`

    - Returns:
        - `Big Buck Bunny [Vol.1]/DISC_01`
        - `Big Buck Bunny [Vol.2]/DISC_01`

    Examples
    --------
    ```python
    from pathlib import Path

    from juicenet import get_bdmv_discs

    folder = Path("C:/Users/raven/BDMVs")

    bdmvs = get_bdmv_discs(folder)

    print(bdmvs)
    # [
    #   WindowsPath('C:/Users/raven/BDMVs/[BDMV] Big Buck Bunny [US]/Big Buck Bunny [Vol.1]/DISC_01'),
    #   WindowsPath('C:/Users/raven/BDMVs/[BDMV] Big Buck Bunny [US]/Big Buck Bunny [Vol.2]/DISC_01'),
    #   WindowsPath('C:/Users/raven/BDMVs/[BDMV] Big Buck Bunny [US]/Big Buck Bunny [Vol.3]/DISC_01'),
    #   WindowsPath('C:/Users/raven/BDMVs/[BDMV] Big Buck Bunny [US]/Big Buck Bunny [Vol.4]/DISC_01'),
    #   WindowsPath('C:/Users/raven/BDMVs/[BDMV] Big Buck Bunny [US]/Big Buck Bunny [Vol.5]/DISC_01'),
    #   WindowsPath('C:/Users/raven/BDMVs/[BDMV] Big Buck Bunny [US]/Big Buck Bunny [Vol.6]/DISC_01'),
    # ]
    ```
    """

    if isinstance(path, str):
        basepath = Path(path).resolve()
    elif isinstance(path, Path):
        basepath = path.resolve()
    else:
        raise JuicenetInputError(f"{path} must be a string or pathlib.Path")

    if not basepath.exists():
        raise JuicenetInputError(f"{basepath} must be an existing file or directory")

    return _get_bdmv_discs(basepath, globs)


def get_dvd_discs(path: StrPath, globs: list[str] = ["*/"]) -> list[Path]:
    """
    Finds individual discs in DVDs by looking for `VIDEO_TS/VIDEO_TS.VOB`.

    Parameters
    ----------
    path : str or pathlib.Path
        The path to an existing file. This can either be a string representing the path or a pathlib.Path object.
    globs : list[str], optional
        List of glob patterns to match. Default will match all sub folders in base path.

    Returns
    -------
    list[Path]
        List of paths where each path is a BDMV disc.

    Raises
    ------
    JuicenetInputError
        Invalid input.

    Notes
    -----
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

    if isinstance(path, str):
        basepath = Path(path).resolve()
    elif isinstance(path, Path):
        basepath = path.resolve()
    else:
        raise JuicenetInputError(f"{path} must be a string or pathlib.Path")

    if not basepath.exists():
        raise JuicenetInputError(f"{basepath} must be an existing file or directory")

    return _get_dvd_discs(basepath, globs)
