import argparse
import glob
import subprocess
import os
import yaml
import json
import shutil
import sys
from loguru import logger

logger = logger.opt(colors=True)
fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
logger.remove()
logger.add(sys.stderr, format=fmt)


script_config = f"{os.path.splitext(__file__)[0]}.yaml"

try:
    with open(script_config) as file:
        data = yaml.safe_load(file)
except FileNotFoundError:
    logger.error(
        f"Could not find {script_config}. Make sure it exists.",
    )
    exit()


PARPAR = data["PARPAR"]
NYUU = data["NYUU"]
NYUU_CONFIG_PRIVATE = data["NYUU_CONFIG_PRIVATE"]
NYUU_CONFIG_PUBLIC = data["NYUU_CONFIG_PUBLIC"]
NZB_OUTPUT_PATH = data["NZB_OUTPUT_PATH"]


@logger.catch
def get_mkv_files(input_path: str) -> list[str]:
    """
    Utility function to get the .mkv files

    Argument:

    `input_path`:    String. Path where the mkv files are.
    """
    mkv_files = list(glob.glob(pathname="**/*.mkv", root_dir=input_path, recursive=True))

    if len(mkv_files) == 0:
        logger.error(f"No .mkv files found in {input_path}")
        exit()

    return mkv_files


@logger.catch
def get_par2_files(input_path: str) -> list[str]:
    """
    Utility function to get the .par2 files

    Argument:

    `input_path`:    String. Path where the par2 files are.
    """
    par2_files = list(glob.glob(pathname="**/*.par2", root_dir=input_path, recursive=True))

    if len(par2_files) == 0:
        logger.error(f"No .par2 files found in {input_path}")
        exit()

    return par2_files


@logger.catch
def get_raw_articles(input_path: str) -> list[str]:
    """
    Utility function to get the raw articles.
    These are articles that failed to post last Nyuu run.
    They have no extension.

    Argument:

    `input_path`:   String. Path where the raw articles are.

    """
    raw_articles = list(glob.glob(pathname="*", root_dir=input_path, recursive=True))
    return raw_articles


@logger.catch
def move_files(input_path: str) -> None:
    """
    Utility function to move files.

    This will move foobar.mkv to foobar/foobar.mkv

    Serves no practical function for this script but
    you may use this if you plan to upload manually later.

    Argument:

    `input_path`:   String. Path where the files to be moved are.

    """
    for file in get_mkv_files(input_path):
        file_without_ext = os.path.splitext(file)[0]
        basename = os.path.basename(file_without_ext)
        destination_path = os.path.join(input_path, basename)
        os.makedirs(destination_path, exist_ok=True)
        current_path = os.path.join(input_path, file)

        try:
            shutil.move(current_path, destination_path)
        except PermissionError:
            logger.error(f"Cannot move {current_path} because it is being used by another process")
            exit()


@logger.catch
def nzb_output(input_path: str, relative_path: str, basename: str, public: bool = False) -> None:
    """
    Utility function to move the nzb files into a somewhat organized manner

    `input_path`:    String. Path where the nzb files to be moved are.

    `relative_path`: String. Path of the file relative to input_path.

    `basename`:      String. Basename of the file.

    `privacy`:        String. Sort output nzbs into /Private or /Public.
    """
    privacy = "PUBLIC" if public else "PRIVATE"

    current_path = os.path.join(input_path, f"{basename}.nzb")

    if len(relative_path.split((os.path.sep))) > 1:
        # foo/bar/foobar.mkv. Make a folder for each top subdirectory in input_path
        output_dir = os.path.join(
            NZB_OUTPUT_PATH, privacy, os.path.basename(input_path), relative_path.split(os.path.sep)[0]
        )
        # output/PRIVATE/basename/foo/foobar.mkv
    else:
        # foobar.mkv. Don't make a folder for each mkv file if input_path has no subdirectories
        output_dir = os.path.join(NZB_OUTPUT_PATH, privacy, os.path.basename(input_path))
        # output/PRIVATE/basename/foobar.mkv

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{basename}.nzb")
    shutil.move(current_path, output_path)


@logger.catch
def repost_raw(public: bool = False, verbose: bool = False) -> None:
    """
    Function to repost the raw articles, uses the path from `dump-failed-posts`
    in your Nyuu config.

    These are articles that failed to post last Nyuu run.
    They have no extension.

    Arguments:

    `public`:     Boolean. Uses your public config if true otherwise will use your private config.

    `verbose`:    Boolean. Print extra info in terminal.
    """
    NYUU_CONFIG = NYUU_CONFIG_PUBLIC if public else NYUU_CONFIG_PRIVATE

    base_args = "--skip-errors all --delete-raw-posts --input-raw-posts"
    args = base_args if verbose else f"--log-level 1 {base_args}"

    with open(NYUU_CONFIG) as file:
        data = json.load(file)
        try:
            raw_articles_path = data["dump-failed-posts"]
        except KeyError:
            logger.error(f"dump-failed-posts is not defined in your Nyuu config")
            exit()

        initial_count = len(get_raw_articles(raw_articles_path))

        if initial_count == 0:
            logger.info(f"No raw articles found (This is a good thing)")
            return None

        logger.info(f"Found {initial_count} raw articles. Trying to repost.")

        nyuu_cmd = f'"{NYUU}" -C "{NYUU_CONFIG}" {args} "{raw_articles_path}"'
        subprocess.run(nyuu_cmd)

        final_count = len(get_raw_articles(raw_articles_path))

        if final_count == 0:
            logger.success(f"All raw articles reposted")
        else:
            logger.info(f"Reposted {initial_count-final_count} articles")
            logger.warning(f"Failed to repost {final_count} articles. Either retry or delete these manually.")


@logger.catch
def parpar(input_path: str, verbose: bool = False) -> None:
    """
    Function to generate par2 files for every mkv file

    Arguments:

    `input_path`:    String. Path to a directory that contains mkv files

    `verbose`:       Boolean. Print extra info in terminal.
    """
    base_args = "--overwrite -s700k --slice-size-multiple=700K --max-input-slices=4000 -r1n*1.2 -R --filepath-format basename -o"
    args = base_args if verbose else f"--quiet {base_args}"
    for file in get_mkv_files(input_path):
        file_without_ext = os.path.splitext(file)[0]
        parpar_cmd = f'"{PARPAR}" {args} "{file_without_ext}" "{file}"'
        logger.info(f"Generating PAR2 files for {file}")
        subprocess.run(parpar_cmd, cwd=input_path)
    logger.success(f"Finished generating PAR2 files")


@logger.catch
def nyuu(input_path: str, public: bool = False, verbose: bool = False) -> None:
    """
    Function to upload the mkv files along with par2 files.

    This gets the .mkv file and it's corresponding par2 files
    and passes them individually to the `-o`. Doing it like this
    means you don't have to move the files into a parent folder.

    Arguments:

    `input_path`:    String. Path to a directory that contains mkv files

    `public`:        Boolean. Uses your public config if true otherwise will use your private config.

    `verbose`:       Boolean. Print extra info in terminal.
    """
    par2_files = get_par2_files(input_path)

    NYUU_CONFIG = NYUU_CONFIG_PUBLIC if public else NYUU_CONFIG_PRIVATE
    privacy = "PUBLIC" if public else "PRIVATE"

    args = f'-C "{NYUU_CONFIG}" --overwrite -o' if verbose else f'--log-level 1 -C "{NYUU_CONFIG}" --overwrite -o'

    for file in get_mkv_files(input_path):
        file_without_ext = os.path.splitext(file)[0]
        basename = os.path.basename(file_without_ext)
        filtered_par2_files = [par2_file for par2_file in par2_files if file_without_ext in par2_file]
        par2_files_str = " ".join([f'"{par2_file}"' for par2_file in filtered_par2_files])

        nyuu_cmd = f'"{NYUU}" {args} "{basename}.nzb" "{file}" {par2_files_str}'

        logger.info(f"Uploading {file} along with {len(filtered_par2_files)} PAR2 files ({privacy})")

        logger.info(nyuu_cmd) if verbose else None

        subprocess.run(nyuu_cmd, cwd=input_path)
        logger.success(f"Successfully uploaded {basename}.nzb")

        nzb_output(input_path, file, basename, public)


@logger.catch
def main() -> None:
    """CLI"""
    parser = argparse.ArgumentParser(description="A script for conveniently uploading .mkv files to usenet")
    parser.add_argument("path", type=str, help="Path to directory containing .mkv files")
    parser.add_argument("-P", "--public", action="store_true", help="Use your public config. Default: private")
    parser.add_argument("-p", "--parpar", action="store_true", help="Only run Parpar")
    parser.add_argument("-n", "--nyuu", action="store_true", help="Only run Nyuu")
    parser.add_argument("-r", "--raw", action="store_true", help="Only repost raw articles")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show everything in terminal")
    parser.add_argument(
        "-m", "--move", action="store_true", help="Move files into their own directories (not required)"
    )
    args = parser.parse_args()

    if args.move:
        move_files(args.path)

    elif args.parpar:
        parpar(args.path, args.verbose)

    elif args.nyuu:
        nyuu(args.path, args.public, args.verbose)

    elif args.raw:
        repost_raw(args.public, args.verbose)

    else:
        repost_raw(args.public, args.verbose)
        parpar(args.path, args.verbose)
        nyuu(args.path, args.public, args.verbose)


if __name__ == "__main__":
    main()
