from __future__ import annotations

import sys
from pathlib import Path
from typing import Union

from loguru import logger as _loguru_logger
from rich.console import Console
from rich.traceback import install

from ..bar import progress_bar
from ..config import get_dump_failed_posts, read_config
from ..exceptions import JuicenetInputError
from ..log import get_logger
from ..nyuu import Nyuu
from ..parpar import ParPar
from ..resume import Resume
from ..types import APIConfig, JuiceBox, StrPath
from ..utils import filter_empty_files, get_glob_matches
from ..version import get_version

# Install rich traceback
install()

# Console object, used by both progressbar and loguru
console = Console()


def juicenet(
    path: StrPath,
    /,
    *,
    config: Union[StrPath, APIConfig],
    public: bool = False,
    bdmv_naming: bool = False,
    resume: bool = True,
    debug: bool = False,
) -> JuiceBox:
    """
    Upload a file or folder to usenet. This will always produce one NZB for one input.

    Parameters
    ----------
    path : str or pathlib.Path
        The path to an existing file. This can either be a string representing the path or a pathlib.Path object.
    config : str or pathlib.Path or APIConfig
        The configuration to use when processing the file or directory.
        This can either be a string representing the path to a YAML configuration file,
        a `pathlib.Path` object pointing to a YAML configuration file,
        or a `juicenet.APIConfig` dataclass.
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

    from juicenet import APIConfig, juicenet

    file = Path("C:/Users/raven/Videos/Big Buck Bunny.mkv") # Path works

    config = "D:/data/usenet/config/juicenet.yaml" # string also works

    # Convenient config class instead of a config file
    config = APIConfig(
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
    elif isinstance(config, APIConfig):
        _config = config  # type: ignore
    else:
        raise JuicenetInputError("Config must be a path or a juicenet.Config")

    # Configure logger
    level = "DEBUG" if debug else "INFO"
    logger = get_logger(logger=_loguru_logger, level=level, sink=console)  # type: ignore

    # Read config file
    config_data = read_config(_config)

    # Get the values from config
    nyuu_bin = config_data.NYUU
    parpar_bin = config_data.PARPAR
    priv_conf = config_data.NYUU_CONFIG_PRIVATE
    pub_conf = config_data.NYUU_CONFIG_PUBLIC or priv_conf
    nzb_out = config_data.NZB_OUTPUT_PATH
    parpar_args = config_data.PARPAR_ARGS

    appdata_dir = config_data.APPDATA_DIR_PATH
    appdata_dir.mkdir(parents=True, exist_ok=True)
    resume_file = appdata_dir / "juicenet.resume"
    resume_file.touch(exist_ok=True)

    if config_data.USE_TEMP_DIR:
        work_dir = config_data.TEMP_DIR_PATH
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

    logger.info(f"Version: {get_version()}")

    if isinstance(config, Path):
        logger.info(f"Config: {config}")

    logger.info(f"Nyuu: {nyuu_bin}")
    logger.info(f"ParPar: {parpar_bin}")
    logger.info(f"Nyuu Config: {conf}")
    logger.info(f"NZB Output: {nzb_out}")
    logger.info(f"Raw Articles: {dump}")
    logger.info(f"Appdata Directory: {appdata_dir}")
    logger.info(f"Working Directory: {work_dir or _path.parent}")

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

    if raw_count:
        logger.info(f"Found {raw_count} raw article(s). Attempting to Repost...")

        rawoutput = {}

        with progress_bar(console=console, transient=True, disable=debug) as progress:
            task_raw = progress.add_task("Raw...", total=raw_count)

            for article in raw_articles:
                raw_out = nyuu.repost_raw(article=article)

                if raw_out.returncode == 0:
                    logger.success(article.name)
                else:
                    logger.error(article.name)

                progress.update(task_raw, advance=1)
                rawoutput[article] = raw_out
    else:
        rawoutput = {}

    with progress_bar(console=console, disable=debug) as progress:
        total = 1

        task_parpar = progress.add_task("ParPar...", total=total)
        task_nyuu = progress.add_task("Nyuu...", total=total)

        if _resume.already_uploaded(file):
            logger.info(f"Skipping: {file.name} - Already uploaded")
            progress.update(task_parpar, advance=1)
            progress.update(task_nyuu, advance=1)
            # return JuiceBox(
            #     nyuu=NyuuOutput(nzb=None, success=False, args=[], returncode=1, stdout="", stderr=""),
            #     parpar=ParParOutput(
            #         par2files=[],
            #         success=False,
            #         filepathbase=file.parent,
            #         filepathformat="basename" if file.is_file() else "path",
            #         args=[],
            #         returncode=1,
            #         stdout="",
            #         stderr="",
            #     ),
            #     raw={},
            # )
            sys.exit(0)
        else:
            parpar_out = parpar.generate_par2_files(file)
            progress.update(task_parpar, advance=1)
            nyuu_out = nyuu.upload(file=file, par2files=parpar_out.par2files)

            if nyuu_out.success:
                logger.success(file.name)
            else:
                logger.error(file.name)

            progress.update(task_nyuu, advance=1)
            _resume.log_file_info(file)

    return JuiceBox(nyuu=nyuu_out, parpar=parpar_out, raw=rawoutput)
