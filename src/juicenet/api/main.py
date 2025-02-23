from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.traceback import install

from ..config import get_dump_failed_posts, read_config
from ..exceptions import JuicenetInputError
from ..model import JuicenetConfig
from ..nyuu import Nyuu
from ..parpar import ParPar
from ..resume import Resume
from ..types import JuiceBox, NyuuOutput, ParParOutput, StrPath
from ..utils import filter_empty_files, get_glob_matches, get_related_files

# Install rich traceback
install()

# Console object, used by both progressbar and loguru
console = Console()


def juicenet(
    path: StrPath,
    /,
    *,
    config: StrPath | JuicenetConfig,
    public: bool = False,
    bdmv_naming: bool = False,
    resume: bool = True,
    skip_raw: bool = False,
    debug: bool = False,
) -> JuiceBox:
    """
    Upload a file or folder to usenet. This will always produce one NZB for one input.

    Parameters
    ----------
    path : str or pathlib.Path
        The path to an existing file. This can either be a string representing the path or a pathlib.Path object.
    config : str or pathlib.Path or JuicenetConfig
        The configuration to use when processing the file or directory.
        This can either be a string representing the path to a YAML configuration file,
        a `pathlib.Path` object pointing to a YAML configuration file,
        or a `juicenet.JuicenetConfig` dataclass.
    public : bool, optional
        Whether the upload is meant to be public or not. Uses the public config if specified,
        falls back to using the private one if not. Default is False.
    bdmv_naming : bool, optional
        Whether to use an alternate naming for BDMVs.
        This will try to fix the awful BDMV disc naming in some cases, i.e, if you pass `/BDMVs/Big Buck Bunny [Vol.1]/DISC_01`,
        then the resulting NZB will be renamed to `Big Buck Bunny [Vol.1]_DISC_01.nzb` instead of `DISC_01.nzb`.
        Recommended if your input is a BDMV disc and you're uncertain about how they are named. Keep it `False` if you're
        certain that your BDMV discs are named appropriately. Only works on directory input,
        does nothing (i.e, `False`) if your input is a file.
    resume: bool, optional
        Whether to enable resumability. Files uploaded by previous runs will be skipped if True. Default is True.
    skip_raw: bool, optional
        Skip checking and reposting failed raw articles. Default is False.
    debug : bool, optional
        Whether to enable debug logs. Default is False.

    Returns
    -------
    JuiceBox
        Dataclass used to represent the output of Juicenet.

    Raises
    ------
    JuicenetInputError
        Invalid input.

    Notes
    -----
    - You should never upload an entire directory consisting of several files as a single NZB.
      Use `juicenet.get_files` or `juicenet.get_glob_matches` to first get the relevant files and
      then pass each one to juicenet.

    - You should never upload an entire BDMV consisting of several discs as a single NZB.
      Use `juicenet.get_bdmv_discs` to first get each individual disc and then pass each one to juicenet.

    Examples
    --------
    ```python
    from pathlib import Path

    from juicenet import JuicenetConfig, juicenet

    file = Path("C:/Users/raven/Videos/Big Buck Bunny.mkv") # Path works

    config = "D:/data/usenet/config/juicenet.yaml" # string also works

    # Convenient config class instead of a config file
    config = JuicenetConfig(
        nyuu_config_private="D:/data/usenet/juicenetConfig/nyuu-config.json",
        nzb_output_path=Path("D:/data/usenet/nzbs"),
    )

    upload = juicenet(file, config=config)

    print(upload.nyuu.nzb)
    # D:/data/usenet/nzbs/private/Videos/Big Buck Bunny.mkv.nzb
    ```
    """

    if isinstance(path, str):
        _path = Path(path).resolve()
    elif isinstance(path, Path):
        _path = path.resolve()
    else:
        raise JuicenetInputError("Path must be a string or pathlib.Path")

    if not _path.exists():
        raise JuicenetInputError(f"{_path} must be an existing file or directory")

    filelist = filter_empty_files([_path])

    if len(filelist) == 1:
        file = filelist[0]
    else:
        raise JuicenetInputError(f"{_path} is empty (0-byte)!")

    if isinstance(config, str):
        _config = Path(config).resolve()
    elif isinstance(config, Path):
        _config = config.resolve()
    elif isinstance(config, JuicenetConfig):
        _config = config  # type: ignore
    else:
        raise JuicenetInputError("Config must be a path or a juicenet.JuicenetConfig")

    # Read config file
    config_data = read_config(_config)

    # Get the values from config
    nyuu_bin = config_data.nyuu
    parpar_bin = config_data.parpar
    priv_conf = config_data.nyuu_config_private
    pub_conf = config_data.nyuu_config_public or priv_conf
    nzb_out = config_data.nzb_output_path
    parpar_args = config_data.parpar_args
    related_exts = config_data.related_extensions

    appdata_dir = config_data.appdata_dir_path
    appdata_dir.mkdir(parents=True, exist_ok=True)
    resume_file = appdata_dir / "juicenet.resume"
    resume_file.touch(exist_ok=True)

    if config_data.use_temp_dir:
        work_dir = config_data.temp_dir_path
    else:
        work_dir = None

    # Decide which config file to use
    configurations = {"public": pub_conf, "private": priv_conf}
    scope = "public" if public else "private"
    conf = configurations[scope]

    # Check and get `dump-failed-posts` as defined in Nyuu config
    dump = get_dump_failed_posts(conf)
    raw_articles = get_glob_matches(dump, ["*"])
    raw_count = len(raw_articles)

    # Initialize Resume class
    no_resume = not resume
    _resume = Resume(resume_file, scope, no_resume)

    # Initialize ParPar class for generating par2 files ahead
    parpar = ParPar(parpar_bin, parpar_args, work_dir, debug)

    # Force disable BDMV naming for file input
    if file.is_file():
        bdmv_naming = False

    # Initialize Nyuu class for uploading stuff ahead
    nyuu = Nyuu(file.parent.parent, nyuu_bin, conf, work_dir, nzb_out, scope, debug, bdmv_naming)

    if raw_count and (not skip_raw):
        rawoutput = {}
        for article in raw_articles:
            raw_out = nyuu.repost_raw(article=article)
            rawoutput[article] = raw_out

    else:
        rawoutput = {}

    if _resume.already_uploaded(file):
        return JuiceBox(
            nyuu=NyuuOutput(nzb=None, success=False, args=[], returncode=1, stdout="", stderr=""),
            parpar=ParParOutput(
                par2files=[],
                success=False,
                filepathbase=file.parent,
                filepathformat="basename" if file.is_file() else "path",
                args=[],
                returncode=1,
                stdout="",
                stderr="",
            ),
            raw={},
            skipped=True,
        )
    else:
        related_files = None

        if file.is_file():
            related_files = get_related_files(file, exts=related_exts)

        parpar_out = parpar.generate_par2_files(file, related_files=related_files)
        nyuu_out = nyuu.upload(file=file, related_files=related_files, par2files=parpar_out.par2files)

        if nyuu_out.success:
            # Only save it to resume if it was successful
            _resume.log_file_info(file)

    return JuiceBox(nyuu=nyuu_out, parpar=parpar_out, raw=rawoutput, skipped=False)
