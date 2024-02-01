import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from loguru import logger

from .types import ArticleFilePath, NyuuOutput, NZBFilePath, PAR2FilePath, RawOutput
from .utils import delete_files


class Nyuu:
    """
    Nyuu class for handling Usenet uploads and reposting raw articles.

    Attributes
    ----------
    path : Path
        The base path for organizing files.
    bin : Path
        Path to the Nyuu binary executable.
    conf : Path
        Path to the Nyuu configuration file.
    workdir : Path, optional
        Working directory for Nyuu execution.
    outdir : Path
        Output directory for storing NZB files.
    scope : str
        Scope identifier for organizing output files.
    debug : bool
        Flag indicating whether to enable debug mode.
    bdmv_naming : bool
        Flag indicating whether to use different naming for BDMVs.

    Methods
    -------
    upload(file: Path, par2files: list[PAR2FilePath], delete_par2files: bool = True) -> NyuuOutput
        Upload files to Usenet with Nyuu.
    repost_raw(article: ArticleFilePath) -> RawOutput
        Repost failed articles from the last run.
    """

    def __init__(
        self,
        path: Path,
        bin: Path,
        conf: Path,
        workdir: Optional[Path],
        outdir: Path,
        scope: str,
        debug: bool,
        bdmv_naming: bool,
    ) -> None:
        self.path = path
        self.bin = bin
        self.conf = conf
        self.workdir = workdir
        self.outdir = outdir
        self.scope = scope
        self.debug = debug
        self.bdmv_naming = bdmv_naming

    def _move_nzb(self, file: Path, basedir: Path, clean_nzb: str, nzb: str) -> NZBFilePath:
        """
        Move NZB to a specified output path in a somewhat sorted manner
        """
        # self.path = /data/raven/videos/show/
        # file = /data/raven/videos/show/extras/specials/episode.mkv
        subdir = file.relative_to(self.path)  # /extras/specials/episode.mkv
        subdir = subdir.parent  # /extras/specials/

        src = self.workdir / clean_nzb if self.workdir else basedir / clean_nzb
        dst = self.outdir / self.scope / self.path.name / subdir  # ./out/private/show/extras/specials/
        dst.mkdir(parents=True, exist_ok=True)
        dst = dst / nzb  # ./out/private/show/extras/specials/episode.mkv.nzb
        shutil.move(src, dst)  # ./workdir/01.nzb -> ./out/private/show/extras/specials/episode.mkv.nzb

        logger.debug(f"NZB Move: {src} -> {dst}")

        return dst.resolve()

    def upload(self, file: Path, par2files: list[PAR2FilePath], *, delete_par2files: bool = True) -> NyuuOutput:
        """
        Upload files to Usenet with Nyuu
        """

        capture_output = not self.debug

        nzb = f"{file.name}.nzb"
        clean_nzb = nzb.replace("`", "'")  # Nyuu doesn't like backticks

        if self.bdmv_naming:
            parent = file.relative_to(self.path).parent.name
            clean_parent = parent.replace("`", "'")
            if parent:
                nzb = f"{parent}_{nzb}"
                clean_nzb = f"{clean_parent}_{clean_nzb}"

        nyuu = [self.bin] + ["--config", self.conf] + ["--out", clean_nzb] + [file] + par2files

        logger.debug(shlex.join(str(arg) for arg in nyuu))

        cwd = self.workdir if self.workdir else file.parent  # this is where nyuu will be executed
        process = subprocess.run(nyuu, cwd=cwd, capture_output=capture_output, encoding="utf-8")  # type: ignore

        if process.returncode in [0, 32]:
            # move completed nzb to output dir
            outpath = self._move_nzb(file=file, basedir=cwd, clean_nzb=clean_nzb, nzb=nzb)

            # Cleanup par2 files for the uploaded file
            if delete_par2files:
                delete_files(par2files)

            return NyuuOutput(
                nzb=outpath,
                success=True,
                args=process.args,
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )
        else:
            return NyuuOutput(
                nzb=None,
                success=False,
                args=process.args,
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )

    def repost_raw(self, article: ArticleFilePath) -> RawOutput:
        """
        Try to repost failed articles from last run
        """
        capture_output = not self.debug

        nyuu = (
            [self.bin]
            + ["--config", self.conf]
            + [
                "--delete-raw-posts",
                "--input-raw-posts",
                article.resolve(),
            ]
        )

        logger.debug(shlex.join(str(arg) for arg in nyuu))

        process = subprocess.run(nyuu, capture_output=capture_output, encoding="utf-8")  # type: ignore

        if process.returncode in [0, 32]:
            return RawOutput(
                article=article,
                success=True,
                args=process.args,
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )
        else:
            return RawOutput(
                article=article,
                success=False,
                args=process.args,
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )
