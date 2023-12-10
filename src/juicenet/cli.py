import argparse
from pathlib import Path

from rich_argparse import RichHelpFormatter

from .juicenet import juicenet


def cli() -> None:
    """
    CLI. Passes the arguments to juicenet()
    """
    parser = argparse.ArgumentParser(
        prog="juicenet",
        description="CLI tool designed to simplify the process of uploading files to usenet",
        formatter_class=RichHelpFormatter,
    )

    parser.add_argument(
        "path",
        metavar="<path>",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="directory containing your files (default: CWD)",
    )

    parser.add_argument(
        "--config",
        default=Path.cwd(),
        type=Path,
        help="specify the path to your juicenet config file",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="print juicenet version",
    )

    parser.add_argument(
        "--public",
        action="store_true",
        help="use your public config",
    )

    parser.add_argument(
        "--nyuu",
        action="store_true",
        help="only run Nyuu in <path>",
    )

    parser.add_argument(
        "--parpar",
        action="store_true",
        help="only run ParPar in <path>",
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="only repost raw articles",
    )

    parser.add_argument(
        "--skip-raw",
        action="store_true",
        help="skip reposting raw articles",
    )

    parser.add_argument(
        "--glob",
        nargs="*",
        default=[],
        metavar="*/",
        help="specify the glob pattern(s) to be matched instead of extensions",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="show logs",
    )

    parser.add_argument(
        "--move",
        action="store_true",
        help="move files into their own directories (foobar.ext -> foobar/foobar.ext)",
    )

    parser.add_argument(
        "--only-move",
        action="store_true",
        help="move files into their own directories (foobar.ext -> foobar/foobar.ext) and exit",
    )

    parser.add_argument(
        "--exts",
        default=[],
        nargs="*",
        metavar="mkv mp4",
        help="look for these extensions in <path> (ignores config)",
    )

    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="ignore resume data",
    )

    parser.add_argument(
        "--clear-resume",
        action="store_true",
        help="delete resume data",
    )

    args = parser.parse_args()

    juicenet(
        path=args.path.resolve(),  # Resolve and pass the absolute path
        conf_path=args.config,
        version=args.version,
        public=args.public,
        only_nyuu=args.nyuu,
        only_parpar=args.parpar,
        only_raw=args.raw,
        skip_raw=args.skip_raw,
        glob=args.glob,
        debug=args.debug,
        move=args.move,
        only_move=args.only_move,
        extensions=args.exts,
        no_resume=args.no_resume,
        clear_resume=args.clear_resume,
    )
