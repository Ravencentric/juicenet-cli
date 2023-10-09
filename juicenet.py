import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path

import yaml
from alive_progress import alive_it, config_handler
from colorama import Fore
from loguru import logger
from rich.traceback import install
from rich_argparse import RichHelpFormatter

# Install rich traceback
install(show_locals=True)

# Set up logger
logger = logger.opt(colors=True)

# Customize progress bar strings
# Making them blend in with loguru
title_parpar = f"{Fore.GREEN}Processing Files{Fore.RESET}    | PARPAR   |"
current_parpar = f"{Fore.GREEN}Current File{Fore.RESET}        | PARPAR   |"
title_nyuu = f"{Fore.GREEN}Uploading Files{Fore.RESET}     | NYUU     |"
current_nyuu = f"{Fore.GREEN}Current File{Fore.RESET}        | NYUU     |"
title_raw = f"{Fore.GREEN}Reposting Articles{Fore.RESET}  | NYUU     |"
current_raw = f"{Fore.GREEN}Current Article{Fore.RESET}     | NYUU     |"


def get_version() -> str:
    """
    Get the version
    """
    return metadata.version("juicenet-cli")


def get_config(path: Path) -> Path:
    """
    Get the path of the config file

    This can be present in three locations:

    1. `--config <path>`
    2. env variable called `JUICENET_CONFIG`
    3. CurrentWorkingDir/juicenet.yaml

    The order of precedence, if all three are present, is:
    `--config > env variable > CurrentWorkingDir/juicenet.yaml`
    """

    if path.is_file():
        return path

    else:
        return Path(os.getenv("JUICENET_CONFIG", path / "juicenet.yaml"))


def read_config(path: Path) -> dict:
    """
    Reads the yaml config file
    """
    return yaml.safe_load(path.read_text())


def get_dump_failed_posts(conf: Path) -> Path:
    """
    Get the value of `dump-failed-posts` from Nyuu config
    """
    data = json.loads(conf.read_text())
    return Path(data["dump-failed-posts"])


def get_files(path: Path, exts: list[str]) -> list[Path]:
    """
    Get all the files with the relevant extensions
    """
    files = []

    for ext in exts:
        ext = ext.strip(".")
        matches = list(path.rglob(f"*.{ext}"))
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
            for item in file.iterdir():
                if item.is_file() and item.stat().st_size > 0:
                    non_empty.append(file)
                    break

    return non_empty


def map_file_to_pars(files: list[Path]) -> dict[Path, list[Path]]:
    """
    For each file, get it's corresponding .par2 files as such:

    `{'foo/01.ext': ['foo/01.ext.par2', 'foo/01.ext.vol12+10.par2', ...]}`
    """
    mapping = {}

    for file in files:
        parent = file.parent
        par2_files = list(parent.glob(f"{glob.escape(file.name)}*.par2"))
        mapping[file] = par2_files

    return mapping


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


def move_nzb(path: Path, subdir: Path, nzb: str, out: Path, scope: str) -> None:
    """
    Move NZB to a specified output path in a somewhat sorted manner
    """
    src = path / nzb  # ./foo/01.nzb
    dst = out / scope / subdir  # ./out/private/foo
    dst.mkdir(parents=True, exist_ok=True)
    dst = dst / nzb  # ./out/private/foo/01.nzb
    shutil.move(src, dst)  # ./foo/01.nzb -> ./out/private/foo/01.nzb

    logger.debug(f"NZB Move: {src} -> {dst}")


def move_files(files: list[Path]) -> None:
    """
    Moves files into their own directories
    Example: foo/01.mkv -> foo/01/01.mkv
    """
    for file in files:
        src = file  # ./foo/01.mkv
        dst = file.parent / file.stem  # ./foo/01/
        dst.mkdir(parents=True, exist_ok=True)
        dst = dst / file.name  # ./foo/01/01.mkv
        src.rename(dst)  # ./foo/01.mkv -> ./foo/01/01.mkv

        logger.debug(f"File Move: {src} -> {dst}")


def cleanup(par2_files: list[Path]) -> None:
    """
    Clean up par2 files after they are uploaded
    """
    for par2 in par2_files:
        par2.unlink(missing_ok=True)


def gen_par2(path: Path, bin: Path, args: list[str], files: list[Path], debug: bool = False) -> None:
    """
    Generate .par2 files with ParPar
    """
    sink = None if debug else subprocess.DEVNULL

    bar = alive_it(files, title=title_parpar)

    format = map_filepath_formats(files)

    for file in bar:
        parpar = [bin] + args + ["--filepath-format", format[file]] + ["--out", file, file]

        bar.text(f"{current_parpar} {file.name} (format: {format[file]})")
        logger.debug(parpar)

        subprocess.run(parpar, cwd=path, stdout=sink, stderr=sink)


def upload(
    path: Path,
    bin: Path,
    conf: Path,
    files: dict[Path, list[Path]],
    out: Path,
    scope: str,
    debug: bool = False,
) -> None:
    """
    Upload files to usenet with Nyuu
    """
    sink = None if debug else subprocess.DEVNULL

    keys = files.keys()
    bar = alive_it(keys, title=title_nyuu)

    for key in bar:
        nzb = f"{key.name}.nzb"
        nyuu = [bin] + ["--config", conf] + ["--out", nzb] + [key] + files[key]

        bar.text(f"{current_nyuu} {key.name} ({scope})")
        logger.debug(nyuu)

        subprocess.run(nyuu, cwd=path, stdout=sink, stderr=sink)

        # Move each completed upload as they are done
        move_nzb(path, key.relative_to(path).parent, nzb, out, scope)

        # Cleanup par2 files for the uploaded file
        cleanup(files[key])


def repost_raw(path: Path, dump: Path, bin: Path, conf: Path, debug: bool) -> None:
    """
    Try to repost failed articles from last run
    """
    sink = None if debug else subprocess.DEVNULL

    articles = get_glob_matches(dump, ["*"])
    raw_count = len(articles)
    logger.info(f"Found {raw_count} raw articles. Attempting to repost")

    bar = alive_it(articles, title=title_raw)

    for article in bar:
        nyuu = (
            [bin]
            + ["--config", conf]
            + [
                "--skip-errors",
                "all",
                "--delete-raw-posts",
                "--input-raw-posts",
                article,
            ]
        )

        bar.text(f"{current_raw} {article.name}")
        logger.debug(nyuu)

        subprocess.run(nyuu, cwd=path, stdout=sink, stderr=sink)

    raw_final_count = len(get_glob_matches(dump, ["*"]))
    if raw_final_count == 0:
        logger.success("All raw articles reposted")
    else:
        logger.info(f"Reposted {raw_count-raw_final_count} articles")
        logger.warning(f"Failed to repost {raw_final_count} articles. Either retry or delete these manually")


def main(
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
    extensions: list[str] | None,
):
    """
    Do stuff here
    """

    # if --version is passed, print and exit
    if version:
        print(get_version())
        sys.exit()

    # Configure logger
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    level = "DEBUG" if debug else "INFO"
    logger.remove(0)
    logger.add(sys.stderr, format=fmt, level=level)

    # Progress bar config
    disable = True if debug else False  # Disable progress bar if --debug is used
    config_handler.set_global(length=50, theme="classic", dual_line=True, disable=disable)

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
    logger.info(f"├── Nyuu: {nyuu}")
    logger.info(f"├── ParPar: {parpar}")
    logger.info(f"├── Nyuu config: {conf}")
    logger.info(f"├── NZB Output: {nzb_out}")
    logger.info(f"├── Extensions: {exts}")
    logger.info(f"├── Pattern: {pattern}")
    logger.info(f"└── Use Pattern: {match}")

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

    raw_count = len(get_glob_matches(dump, ["*"]))

    if only_raw:
        if raw_count != 0:
            repost_raw(path, dump, nyuu, conf, debug)
        else:
            logger.info("No raw articles available for reposting")
        sys.exit()

    if match:
        files = get_glob_matches(path, pattern)
    else:
        files = get_files(path, exts)

    if not files:
        logger.error("No matching files or patterns found with the given extension in:")
        logger.error(path)
        sys.exit()

    if not match and move:  # Do not move if --match was used
        logger.info(f"Moving {len(files)} file(s)")
        move_files(files)
        logger.success(f"Files moved successfully")

        # Get the new path of files
        files = get_files(path, exts)

    # Remove empty directories
    files = rm_empty_paths(files)

    if only_parpar:
        gen_par2(path, parpar, parpar_args, files, debug)
        sys.exit()

    if only_nyuu:
        mapping = map_file_to_pars(files)
        upload(path, nyuu, conf, mapping, nzb_out, scope, debug)
        sys.exit()

    if skip_raw:
        gen_par2(path, parpar, parpar_args, files, debug)
        mapping = map_file_to_pars(files)
        upload(path, nyuu, conf, mapping, nzb_out, scope, debug)
        sys.exit()

    else:
        if raw_count != 0:
            repost_raw(path, dump, nyuu, conf, debug)

        gen_par2(path, parpar, parpar_args, files, debug)
        mapping = map_file_to_pars(files)
        upload(path, nyuu, conf, mapping, nzb_out, scope, debug)


def CLI():
    """
    CLI. Passes the arguments to main()
    """
    parser = argparse.ArgumentParser(
        description="Crude CLI tool to upload files to Usenet using Nyuu and ParPar",
        formatter_class=RichHelpFormatter,
    )

    parser.add_argument(
        "path",
        metavar="path",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Directory containing your files (default: CWD)",
    )

    parser.add_argument(
        "--config",
        default=Path.cwd(),
        type=Path,
        help="Use your public config",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Print juicenet version",
    )

    parser.add_argument(
        "--public",
        action="store_true",
        help="Use your public config",
    )

    parser.add_argument(
        "--nyuu",
        action="store_true",
        help="Only run Nyuu",
    )

    parser.add_argument(
        "--parpar",
        action="store_true",
        help="Only run ParPar",
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="Only repost raw articles",
    )

    parser.add_argument(
        "--skip-raw",
        action="store_true",
        help="Skip reposting raw articles",
    )

    parser.add_argument(
        "--match",
        action="store_true",
        help="Enable pattern matching mode",
    )

    parser.add_argument(
        "--pattern",
        nargs="*",
        default=["*/"],  # glob pattern for subfolders in root of path
        metavar="*/",
        help="Specify the glob pattern(s) to be matched in pattern matching mode",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show logs",
    )

    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files into their own directories. This will move foobar.ext to foobar/foobar.ext",
    )

    parser.add_argument(
        "--exts",
        default=None,
        nargs="*",
        metavar="mkv mp4",
        help="Look for these extensions in <path> (ignores config)",
    )

    args = parser.parse_args()

    main(
        path=args.path,
        conf_path=args.config,
        version=args.version,
        public=args.public,
        only_nyuu=args.nyuu,
        only_parpar=args.parpar,
        only_raw=args.raw,
        skip_raw=args.skip_raw,
        match=args.match,
        pattern=args.pattern,
        debug=args.debug,
        move=args.move,
        extensions=args.exts,
    )


if __name__ == "__main__":
    CLI()
