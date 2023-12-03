import json
import signal
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from alive_progress import config_handler
from loguru import logger
from rich.traceback import install

from .config import get_config, get_dump_failed_posts, read_config
from .files import get_files, get_glob_matches, map_file_to_pars, move_files, rm_empty_paths
from .nyuu import Nyuu
from .parpar import ParPar
from .version import get_version

# Supress keyboardinterrupt traceback because I hate it
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))

# Install rich traceback
install(show_locals=True)

# Set up logger
logger = logger.opt(colors=True)


def juicenet(
    path: Path,
    conf_path: Path,
    version: bool,
    public: bool,
    only_nyuu: bool,
    only_parpar: bool,
    only_raw: bool,
    skip_raw: bool,
    match: bool,
    pattern: list[str],
    debug: bool,
    move: bool,
    only_move: bool,
    extensions: list[str],
) -> None:
    """
    Do stuff here
    """

    # Configure logger
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    level = "DEBUG" if debug else "INFO"
    logger.remove(0)
    logger.add(sys.stderr, format=fmt, level=level)

    # Progress bar config
    # Disable progress bar if --debug is used
    config_handler.set_global(length=50, theme="classic", dual_line=True, disable=debug)

    # if --version is passed, print and exit
    if version:
        print(get_version())
        sys.exit()

    # print version when --debug is used
    logger.debug(f"Version: {get_version()}")

    # Read config file
    try:
        conf_path = get_config(conf_path)
        config = read_config(conf_path)
    except FileNotFoundError as error:
        logger.error(f"No such file: {error.filename}")
        logger.error("You can provide the config in 3 ways:")
        logger.error("1. Explicitly pass --config")
        logger.error("2. Set the 'JUICENET_CONFIG' env variable")
        logger.error("3. Place 'juicenet.yaml' in the current working directory")
        sys.exit()

    # Get the required values from config
    try:
        nyuu_bin = Path(config["NYUU"])
        parpar_bin = Path(config["PARPAR"])
        priv_conf = Path(config["NYUU_CONFIG_PRIVATE"])
        nzb_out = Path(config["NZB_OUTPUT_PATH"])
        exts = list(extensions if extensions else config["EXTENSIONS"])
        parpar_args = list(config["PARPAR_ARGS"])
    except KeyError as key:
        logger.error(f"{key} is missing in {conf_path}")
        sys.exit()

    # Get optional value from config
    pub_conf = Path(config.get("NYUU_CONFIG_PUBLIC", priv_conf))
    use_tempdir = config.get("USE_TEMPDIR", True)
    tempdir_path = config.get("TEMPDIR_PATH")

    if use_tempdir:
        temp_dir = TemporaryDirectory(prefix=".JUICENET_", ignore_cleanup_errors=True)
        work_dir = Path(temp_dir.name)
        if tempdir_path is not None:
            work_dir = Path(tempdir_path)
    else:
        work_dir = None

    # Decide which config file to use
    configurations = {"public": pub_conf, "private": priv_conf}
    scope = "public" if public else "private"
    conf = configurations[scope]

    logger.info(f"Config: {conf_path}")
    logger.info(f"Nyuu: {nyuu_bin}")
    logger.info(f"ParPar: {parpar_bin}")
    logger.info(f"Nyuu Config: {conf}")
    logger.info(f"NZB Output: {nzb_out}")
    logger.info(f"Working Directory: {work_dir if work_dir else path}")
    logger.info(f"Pattern: {pattern}" if match else f"Extension: {exts}")

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

    # Initialize ParPar class for generating par2 files ahead
    parpar = ParPar(parpar_bin, parpar_args, work_dir, debug)

    # Initialize Nyuu class for uploading stuff ahead
    nyuu = Nyuu(path, nyuu_bin, conf, work_dir, nzb_out, scope, debug)

    # Check if there are any raw files from previous runs
    raw_count = len(get_glob_matches(dump, ["*"]))

    # --only-raw
    if only_raw:
        if raw_count != 0:
            nyuu.repost_raw(dump)
        else:
            logger.info("No raw articles available for reposting")
        sys.exit()

    if match:  # --match --pattern
        try:
            files = get_glob_matches(path, pattern)
        except NotImplementedError as error:
            logger.error(error)
            sys.exit()
    else:
        files = get_files(path, exts)

    if not files:
        logger.error("No matching files or patterns found with the given extension in:")
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

    # Remove empty paths
    logger.debug("Filtering out empty paths")
    files = rm_empty_paths(files)
    logger.debug("Filtering complete")

    if not files:
        logger.error(
            "Matching files or patterns found, but they are either empty or "
            "contain only 0-byte files, making them effectively empty"
        )
        sys.exit()

    if only_parpar:  # --parpar
        logger.debug("Only running ParPar")
        # If you're using parpar only then you probably don't want it going in temp
        parpar.workdir = None  # Generate par2 files next to the input files
        parpar.generate_par2_files(files)
        sys.exit()

    if only_nyuu:  # --nyuu
        logger.debug("Only running Nyuu")

        logger.debug("Mapping files to their corresponding par2 files")
        mapping = map_file_to_pars(work_dir, files)
        logger.debug(f"Mapped {len(mapping.keys())} files")

        nyuu.upload(mapping)
        sys.exit()

    if skip_raw:  # --skip-raw
        logger.warning("Raw article checking and reposting is being skipped")
        parpar.generate_par2_files(files)

        logger.debug("Mapping files to their corresponding par2 files")
        mapping = map_file_to_pars(work_dir, files)
        logger.debug(f"Mapped {len(mapping.keys())} files")

        nyuu.upload(mapping)
        sys.exit()

    else:  # default
        if raw_count != 0:
            nyuu.repost_raw(dump)

        parpar.generate_par2_files(files)

        logger.debug("Mapping files to their corresponding par2 files")
        mapping = map_file_to_pars(work_dir, files)
        logger.debug(f"Mapped {len(mapping.keys())} files")

        nyuu.upload(mapping)
