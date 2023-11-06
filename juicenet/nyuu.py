import shutil
import subprocess
from pathlib import Path

from alive_progress import alive_it
from loguru import logger

from .enums import BarTitle, CurrentFile
from .files import get_glob_matches


def move_nzb(path: Path, subdir: Path, nzb: str, out: Path, scope: str) -> None:
    """
    Move NZB to a specified output path in a somewhat sorted manner
    """
    subdir = path.name if subdir == Path(".") else subdir

    src = path / nzb  # ./foo/01.nzb
    dst = out / scope / subdir  # ./out/private/foo
    dst.mkdir(parents=True, exist_ok=True)
    dst = dst / nzb  # ./out/private/foo/01.nzb
    shutil.move(src, dst)  # ./foo/01.nzb -> ./out/private/foo/01.nzb

    logger.debug(f"NZB Move: {src} -> {dst}")


def cleanup(par2_files: list[Path]) -> None:
    """
    Clean up par2 files after they are uploaded
    """
    for par2 in par2_files:
        par2.unlink(missing_ok=True)


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
    bar = alive_it(keys, title=BarTitle.NYUU)

    for key in bar:
        nzb = f"{key.name}.nzb"
        nyuu = [bin] + ["--config", conf] + ["--out", nzb] + [key] + files[key]

        logger.debug(nyuu)
        bar.text(f"{CurrentFile.NYUU} {key.name} ({scope})")

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

    bar = alive_it(articles, title=BarTitle.RAW)

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

        bar.text(f"{CurrentFile.RAW} {article.name}")
        logger.debug(nyuu)

        subprocess.run(nyuu, cwd=path, stdout=sink, stderr=sink)

    raw_final_count = len(get_glob_matches(dump, ["*"]))
    if raw_final_count == 0:
        logger.success("All raw articles reposted")
    else:
        logger.info(f"Reposted {raw_count-raw_final_count} articles")
        logger.warning(f"Failed to repost {raw_final_count} articles. Either retry or delete these manually")
