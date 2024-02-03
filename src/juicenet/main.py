import json
import signal
import sys
from pathlib import Path
from typing import Any, Optional, Union

from loguru import logger as _loguru_logger
from pydantic import ValidationError
from rich.console import Console
from rich.traceback import install

from .bar import progress_bar
from .config import get_dump_failed_posts, read_config
from .log import get_logger
from .nyuu import Nyuu
from .parpar import ParPar
from .resume import Resume
from .types import InternalJuicenetOutput, SubprocessOutput
from .utils import (
    delete_files,
    filter_empty_files,
    filter_par2_files,
    get_bdmv_discs,
    get_files,
    get_glob_matches,
    map_file_to_pars,
    move_files,
)
from .version import get_version

# Supress keyboardinterrupt traceback because I hate it
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))

# Install rich traceback
install()

# Console object, used by both progressbar and loguru
console = Console()


def main(
    path: Path,
    config: Union[Path, dict[str, Any]],
    public: bool = False,
    only_nyuu: bool = False,
    only_parpar: bool = False,
    only_raw: bool = False,
    skip_raw: bool = False,
    clear_raw: bool = False,
    glob: Optional[list[str]] = None,
    bdmv: bool = False,
    debug: bool = False,
    move: bool = False,
    only_move: bool = False,
    extensions: Optional[list[str]] = None,
    no_resume: bool = False,
    clear_resume: bool = False,
) -> InternalJuicenetOutput:
    """
    Do stuff here
    """

    # Configure logger
    level = "DEBUG" if debug else "INFO"
    logger = get_logger(logger=_loguru_logger, level=level, sink=console)  # type: ignore

    # Read config file
    try:
        config_data = read_config(config)
    except FileNotFoundError as error:
        logger.error(f"Config file not found: {error.filename}")
        sys.exit()
    except ValidationError as errors:
        logger.error(f"{errors.error_count()} error(s) in config")
        for err in errors.errors():
            logger.error(f"{err.get('loc')[0]}: {err.get('msg')}")  # type: ignore
        sys.exit()

    # Get the values from config
    nyuu_bin = config_data.NYUU
    parpar_bin = config_data.PARPAR
    priv_conf = config_data.NYUU_CONFIG_PRIVATE
    pub_conf = config_data.NYUU_CONFIG_PUBLIC or priv_conf
    nzb_out = config_data.NZB_OUTPUT_PATH
    exts = extensions or config_data.EXTENSIONS
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
    try:
        dump = get_dump_failed_posts(conf)
    except json.JSONDecodeError as error:
        logger.error(error)
        logger.error("Please check your Nyuu config and ensure it is valid")
        sys.exit()
    except KeyError as key:
        logger.error(f"{key} is not defined in your Nyuu config")
        sys.exit()
    except FileNotFoundError as error:
        logger.error(f"No such file: {error.filename}")
        sys.exit()

    logger.debug(f"Version: {get_version()}")
    logger.info(f"Config: {config}")
    logger.info(f"Nyuu: {nyuu_bin}")
    logger.info(f"ParPar: {parpar_bin}")
    logger.info(f"Nyuu Config: {conf}")
    logger.info(f"NZB Output: {nzb_out}")
    logger.info(f"Raw Articles: {dump}")
    logger.info(f"Appdata Directory: {appdata_dir}")
    logger.info(f"Working Directory: {work_dir or path}")

    if glob or bdmv:
        logger.info(f"Glob Pattern: {glob or ['*/']}")
    else:
        logger.info(f"Extensions: {exts}")

    # --clear-raw
    if clear_raw:
        raw = get_glob_matches(dump, ["*"])
        count = len(raw)
        delete_files(raw)
        logger.info(f"Deleted {count} raw articles(s)")
        sys.exit()

    # Initialize Resume class
    resume = Resume(resume_file, scope, no_resume)

    # Initialize ParPar class for generating par2 files ahead
    parpar = ParPar(parpar_bin, parpar_args, work_dir, debug)

    # Initialize Nyuu class for uploading stuff ahead
    nyuu = Nyuu(path, nyuu_bin, conf, work_dir, nzb_out, scope, debug, bdmv)

    if clear_resume:  # --clear-resume
        resume.clear_resume()  # Delete resume data
        sys.exit()

    # Check if there are any raw files from previous runs
    raw_articles = get_glob_matches(dump, ["*"])
    raw_count = len(raw_articles)

    # --only-raw
    if only_raw:
        if raw_count == 0:
            logger.info("No raw articles available for reposting")
        else:
            output = {}

            with progress_bar(console=console, disable=debug) as progress:
                task_raw = progress.add_task("Raw...", total=raw_count)

                for article in raw_articles:
                    raw_out = nyuu.repost_raw(article=article)

                    if raw_out.returncode == 0:
                        logger.success(article.name)
                    else:
                        logger.error(article.name)

                    progress.update(task_raw, advance=1)
                    output[article] = SubprocessOutput(raw=raw_out)

            return InternalJuicenetOutput(articles=output)

    if path.is_file():  # juicenet "file.mkv"
        files = [path]

    elif bdmv:  # --bdmv
        pattern = glob or ["*/"]
        files = get_bdmv_discs(path, pattern)

    elif glob:  # --glob
        try:
            files = get_glob_matches(path, glob)
        except NotImplementedError as error:
            logger.error(error)
            sys.exit()
    else:
        files = get_files(path, exts)

    # Remove any par2 files present in the input
    # trying to run ParPar on a par2 file doesn't go well
    files = filter_par2_files(files)

    if not files:
        logger.error("No matching files/folders found in:")
        logger.error(path)
        sys.exit()

    if only_move:  # --only-move
        logger.info("Moving file(s)")
        move_files(files)
        logger.success("File(s) moved successfully")
        sys.exit()

    if move:  # --move
        logger.info("Moving file(s)")
        move_files(files)
        logger.success("File(s) moved successfully")

        # Get the new path of files
        files = get_files(path, exts)

    total = len(files)
    logger.debug(f"Total files: {total}")

    # Filter out empty paths and remove anything that isn't a directory or file
    files = filter_empty_files(files)

    non_empty_count = len(files)
    logger.debug(f"Empty files: {total-non_empty_count}")
    logger.debug(f"Total files left: {non_empty_count}")

    if not files:
        logger.error(
            "Matching files/folders found, but they are either empty or "
            "contain only 0-byte files, making them effectively empty"
        )
        sys.exit()

    files = sorted(resume.filter_uploaded_files(files))

    if not files:
        logger.info(
            "Matching files/folders found, but they were already uploaded before. "
            "You can force upload these with --no-resume"
        )
        sys.exit()

    if only_parpar:  # --parpar
        logger.debug("Only running ParPar")

        # If you're using parpar only then you probably don't want it going in temp
        parpar.workdir = None  # Generate par2 files next to the input files

        output = {}

        with progress_bar(console=console, disable=debug) as progress:
            total = len(files)
            task_parpar = progress.add_task("ParPar...", total=total)

            for file in files:
                if resume.already_uploaded(file):
                    logger.info(f"Skipping: {file.name} - Already uploaded")
                    progress.update(task_parpar, advance=1)
                else:
                    parpar_out = parpar.generate_par2_files(file)

                    if parpar_out.returncode == 0:
                        logger.success(file.name)
                    else:
                        logger.error(file.name)

                    progress.update(task_parpar, advance=1)
                    resume.log_file_info(file)
                    output[file] = SubprocessOutput(parpar=parpar_out)

        return InternalJuicenetOutput(files=output)

    if only_nyuu:  # --nyuu
        logger.debug("Only running Nyuu")

        # Try to find any pre-existing `.par2` files
        par2files = map_file_to_pars(None, files)
        # Same logic as for --parpar
        nyuu.workdir = None

        output = {}

        with progress_bar(console=console, disable=debug) as progress:
            total = len(files)
            task_nyuu = progress.add_task("Nyuu...", total=total)

            for file in files:
                if resume.already_uploaded(file):
                    logger.info(f"Skipping: {file.name} - Already uploaded")
                    progress.update(task_nyuu, advance=1)
                else:
                    nyuu_out = nyuu.upload(file=file, par2files=par2files[file])

                    if nyuu_out.returncode == 0:
                        logger.success(file.name)
                    else:
                        logger.error(file.name)

                    progress.update(task_nyuu, advance=1)
                    resume.log_file_info(file)
                    output[file] = SubprocessOutput(nyuu=nyuu_out)

        return InternalJuicenetOutput(files=output)

    if skip_raw:  # --skip-raw
        logger.warning("Raw article checking and reposting is being skipped")
        output = {}

        with progress_bar(console=console, disable=debug) as progress:
            total = len(files)

            task_parpar = progress.add_task("ParPar...", total=total)
            task_nyuu = progress.add_task("Nyuu...", total=total)

            for file in files:
                if resume.already_uploaded(file):
                    logger.info(f"Skipping: {file.name} - Already uploaded")
                    progress.update(task_parpar, advance=1)
                    progress.update(task_nyuu, advance=1)
                else:
                    parpar_out = parpar.generate_par2_files(file)
                    progress.update(task_parpar, advance=1)
                    nyuu_out = nyuu.upload(file=file, par2files=parpar_out.par2files)

                    if nyuu_out.returncode in [0, 32]:
                        logger.success(file.name)
                    else:
                        logger.error(file.name)

                    progress.update(task_nyuu, advance=1)
                    resume.log_file_info(file)
                    output[file] = SubprocessOutput(nyuu=nyuu_out, parpar=parpar_out)

        return InternalJuicenetOutput(files=output)

    else:  # default
        output = {}

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
                    rawoutput[article] = SubprocessOutput(raw=raw_out)
        else:
            rawoutput = None

        with progress_bar(console=console, disable=debug) as progress:
            total = len(files)

            task_parpar = progress.add_task("ParPar...", total=total)
            task_nyuu = progress.add_task("Nyuu...", total=total)

            for file in files:
                if resume.already_uploaded(file):
                    logger.info(f"Skipping: {file.name} - Already uploaded")
                    progress.update(task_parpar, advance=1)
                    progress.update(task_nyuu, advance=1)
                else:
                    parpar_out = parpar.generate_par2_files(file)
                    progress.update(task_parpar, advance=1)
                    nyuu_out = nyuu.upload(file=file, par2files=parpar_out.par2files)

                    if nyuu_out.returncode in [0, 32]:
                        logger.success(file.name)
                    else:
                        logger.error(file.name)

                    progress.update(task_nyuu, advance=1)
                    resume.log_file_info(file)
                    output[file] = SubprocessOutput(nyuu=nyuu_out, parpar=parpar_out)

        return InternalJuicenetOutput(files=output, articles=rawoutput)
