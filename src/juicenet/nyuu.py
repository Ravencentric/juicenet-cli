import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Union

from alive_progress import alive_it
from loguru import logger

from .enums import BarTitle, CurrentFile
from .files import get_glob_matches


class Nyuu:
    """
    A class representing Nyuu

    Attributes:
        - `path (Path)`: The path to the directory containing the files to be uploaded
        - `bin (Path)`: The path to Nyuu binary
        - `conf (Path)`: The path to the Nyuu's configuration file
        - `out (Path)`: The path to the output directory where Nyuu will create nzbs
        - `scope (str)`: The scope of the nzbs made by Nyuu (Private or Public)
        - `debug (bool)`: Debug mode for extra logs

    Methods:
        - `nzb_output_path(key: Path) -> Union[Path, PurePosixPath]`: Constructs the output path of the NZB
        - `cleanup(par2_files: list[Path]) -> None`: Cleans up par2 files after they are uploaded
        - `upload(files: dict[Path, list[Path]]) -> None`: Uploads files to usenet with Nyuu
        - `repost_raw(dump: Path) -> None`: Tries to repost failed articles from the last run

    This class is used to manage the uploading and reposting of files to usenet using Nyuu
    """

    def __init__(self, path: Path, bin: Path, conf: Path, out: Path, scope: str, debug: bool) -> None:
        self.path = path
        self.bin = bin
        self.conf = conf
        self.out = out
        self.scope = scope
        self.debug = debug

    def nzb_output_path(self, key: Path) -> Union[Path, PurePosixPath]:
        """
        Construct the output path of the NZB. This is where Nyuu will make the
        NZB file in a somewhat sorted manner.
        Messy function because I can't think of a better solution

        Issues:
        - Nyuu throws SyntaxError when absolute WindowsPath is passed to `--out`
        - Nyuu doesn't like backticks (``)

        My hacky solution(s):
        - Force PurePosixPath on Windows
        - Replace all the bacticks (``) with apostrophe ('). Escaping with double backslashes still
          throws syntax error which is why I'm replacing them
        """
        dst = self.out / self.scope / self.path.name / key.relative_to(self.path).parent  # ./out/private/workdir/foo
        dst = Path(str(dst).replace("`", "'"))
        dst.mkdir(parents=True, exist_ok=True)
        dst = dst / f"{key.name}.nzb".replace("`", "'")  # ./out/private/workdir/foo/01.nzb

        if sys.platform == "win32":
            return PurePosixPath(dst)
        return dst

    @staticmethod
    def cleanup(par2_files: list[Path]) -> None:
        """
        Clean up par2 files after they are uploaded
        """
        for par2 in par2_files:
            par2.unlink(missing_ok=True)

    def upload(self, files: dict[Path, list[Path]]) -> None:
        """
        Upload files to usenet with Nyuu
        """
        sink = None if self.debug else subprocess.DEVNULL

        keys = files.keys()
        bar = alive_it(keys, title=BarTitle.NYUU)

        for key in bar:
            nyuu = [self.bin] + ["--config", self.conf] + ["--out", self.nzb_output_path(key)] + [key] + files[key]

            logger.debug(nyuu)
            bar.text(f"{CurrentFile.NYUU} {key.name} ({self.scope})")

            subprocess.run(nyuu, cwd=self.path, stdout=sink, stderr=sink)  # type: ignore

            # Cleanup par2 files for the uploaded file
            self.cleanup(files[key])

    def repost_raw(self, dump: Path) -> None:
        """
        Try to repost failed articles from last run
        """
        sink = None if self.debug else subprocess.DEVNULL

        articles = get_glob_matches(dump, ["*"])
        raw_count = len(articles)
        logger.info(f"Found {raw_count} raw articles. Attempting to repost")

        bar = alive_it(articles, title=BarTitle.RAW)

        for article in bar:
            nyuu = (
                [bin]
                + ["--config", self.conf]
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

            subprocess.run(nyuu, cwd=self.path, stdout=sink, stderr=sink)  # type: ignore

        raw_final_count = len(get_glob_matches(dump, ["*"]))
        if raw_final_count == 0:
            logger.success("All raw articles reposted")
        else:
            logger.info(f"Reposted {raw_count-raw_final_count} articles")
            logger.warning(f"Failed to repost {raw_final_count} articles. Either retry or delete these manually")
