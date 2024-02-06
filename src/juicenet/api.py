from pathlib import Path
from typing import Any, Union

from .main import main
from .types import JuicenetOutput, StrPath

__all__ = [
    "juicenet",
]


def juicenet(
    path: StrPath,
    /,
    *,
    config: Union[StrPath, dict[str, Any]],
    is_public: bool = False,
    resume: bool = False,
    debug: bool = False,
) -> JuicenetOutput:
    """
    Upload a file to usenet

    Parameters
    ----------
    path : str or pathlib.Path
        The path to an existing file. This can either be a string representing the path or a pathlib.Path object.
    config : str, dict, or pathlib.Path
        The configuration to use when processing the file or directory.
        This can either be a dictionary, a string representing the path to a configuration file,
        or a pathlib.Path object pointing to a configuration file.
    is_public : bool, optional
        Whether the upload is meant to be public or not. Uses the public config if specified,
        falls back to using the private one if not. Default is False.
    resume: bool, optional
        Whether to enable resumability. Previously uploaded files will be skipped if True. Default is False.
    debug : bool, optional
        Whether to enable debug logs. Default is False.

    Returns
    -------
    JuicenetOutput
        Dataclass used to represent the output of Juicenet.

    Raises
    ------
    ValueError
        Raised if `path` is not a string or pathlib.Path, or if it does not point to an existing file
        or `config` is not a string, a dictionary, or a pathlib.Path, or if it does not point to an existing file.

    Examples
    --------
    >>> from pathlib import Path
    >>> from juicenet import juicenet
    >>> file = Path("C:/Users/raven/Videos/Big Buck Bunny.mkv").resolve() # Recommended to always use resolved pathlib.Path
    >>> config = "D:/data/usenet/juicenetConfig/ENVjuicenet.yaml" # String also works, but not recommended
    >>> upload = juicenet(file, config=config)
    >>> upload.nyuu.nzb # You can access the `.nyuu.nzb` attribute to get the resolved pathlib.Path to the resulting nzb
    WindowsPath('D:/data/usenet/nzbs/private/Big Buck Bunny.mkv/Big Buck Bunny.mkv.nzb')
    """

    if isinstance(path, str):
        _path = Path(path).resolve()
    elif isinstance(path, Path):
        _path = path.resolve()
    else:
        raise ValueError("Path must be a string or pathlib.Path")

    if not _path.is_file():
        ValueError(f"{_path} must be an existing file")

    if isinstance(config, str):
        _config = Path(config).resolve()
    elif isinstance(config, Path):
        _config = config.resolve()
    elif isinstance(config, dict):
        _config = config  # type: ignore
    else:
        raise ValueError("Config must be a path or a dictonary")

    _resume = not resume

    _upload = main(path=_path, config=_config, no_resume=_resume, public=is_public, debug=debug)

    return JuicenetOutput(nyuu=_upload.files[_path].nyuu, parpar=_upload.files[_path].parpar)  # type: ignore
