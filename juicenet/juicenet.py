import json
import signal
import sys
from pathlib import Path

from alive_progress import config_handler
from loguru import logger
from rich.traceback import install

from .config import get_config, get_dump_failed_posts, read_config
from .files import get_files, get_glob_matches, map_file_to_pars, move_files, rm_empty_paths
from .nyuu import repost_raw, upload
from .parpar import gen_par2
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
):
    """
    Do stuff here
    """

    # Configure logger
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    level = "DEBUG" if debug else "INFO"
    logger.remove(0)
    logger.add(sys.stderr, format=fmt, level=level)

    # Progress bar config
    disable = True if debug else False  # Disable progress bar if --debug is used
    config_handler.set_global(length=50, theme="classic", dual_line=True, disable=disable)

    # if --version is passed, print and exit
    if version:
        logger.info(f"Version: {get_version()}")
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
        nyuu = Path(config["NYUU"])
        parpar = Path(config["PARPAR"])
        priv_conf = Path(config["NYUU_CONFIG_PRIVATE"])
        nzb_out = Path(config["NZB_OUTPUT_PATH"])
        exts = list(extensions if extensions else config["EXTENSIONS"])
        parpar_args = list(config["PARPAR_ARGS"])
    except KeyError as key:
        logger.error(f"{key} is missing in {conf_path}")
        sys.exit()

    # Get optional value from config
    pub_conf = Path(config.get("NYUU_CONFIG_PUBLIC", priv_conf))

    # Decide which config file to use
    configurations = {"public": pub_conf, "private": priv_conf}
    scope = "public" if public else "private"
    conf = configurations[scope]

    logger.info(f"Config: {conf_path}")
    logger.info(f"Nyuu: {nyuu}")
    logger.info(f"ParPar: {parpar}")
    logger.info(f"Nyuu Config: {conf}")
    logger.info(f"NZB Output: {nzb_out}")

    if match:
        logger.info(f"Pattern: {pattern}")
    else:
        logger.info(f"Extension: {exts}")

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

    # Check if there are any raw files from previous runs
    raw_count = len(get_glob_matches(dump, ["*"]))

    # --only-raw
    if only_raw:
        if raw_count != 0:
            repost_raw(path, dump, nyuu, conf, debug)
        else:
            logger.info("No raw articles available for reposting")
        sys.exit()

    if match:  # --match --pattern
        files = get_glob_matches(path, pattern)
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
    files = rm_empty_paths(files)

    if not files:
        logger.error(
            "Matching files or patterns found, but they are either empty or "
            "contain only 0-byte files, making them effectively empty"
        )
        sys.exit()

    if only_parpar:  # --parpar
        gen_par2(path, parpar, parpar_args, files, debug)
        sys.exit()

    if only_nyuu:  # --nyuu
        mapping = map_file_to_pars(files)
        upload(path, nyuu, conf, mapping, nzb_out, scope, debug)
        sys.exit()

    if skip_raw:  # --skip-raw
        logger.warning("Raw article checking and reposting is being skipped")
        gen_par2(path, parpar, parpar_args, files, debug)
        mapping = map_file_to_pars(files)
        upload(path, nyuu, conf, mapping, nzb_out, scope, debug)
        sys.exit()

    else:  # default
        if raw_count != 0:
            repost_raw(path, dump, nyuu, conf, debug)

        gen_par2(path, parpar, parpar_args, files, debug)
        mapping = map_file_to_pars(files)
        upload(path, nyuu, conf, mapping, nzb_out, scope, debug)
