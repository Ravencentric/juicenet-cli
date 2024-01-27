from pathlib import Path
from typing import Annotated, Optional

from cyclopts import App, Group, Parameter, validators
from cyclopts.types import ResolvedExistingFile, ResolvedExistingPath

from .main import main
from .version import get_version

app = App(
    name="juicenet",
    help="CLI tool designed to simplify the process of uploading files to Usenet",
    usage="Usage: juicenet [PATH] [PARAMETERS]",
    version=get_version(),
    default_parameter=Parameter(negative="", show_default=False),
)

# Mutually exclusive group to handle mutually exclusive options in cli
exclusive = (app.group_parameters, Group(validator=validators.LimitedChoice()))

# Change the default command group
app["--help"].group = exclusive
app["--help"].help = "display this message and exit"

app["--version"].group = exclusive
app["--version"].help = "display application version"


@app.default
def cli(
    path: Annotated[
        ResolvedExistingPath,
        Parameter(
            help="file or directory.",
            show_default=True,
        ),
    ] = Path.cwd(),
    /,
    *,
    config: Annotated[
        ResolvedExistingFile,
        Parameter(
            help="path to your juicenet config file",
            env_var="JUICENET_CONFIG",
        ),
    ] = Path.cwd() / "juicenet.yaml",
    public: Annotated[
        bool,
        Parameter(
            help="use your public/secondary nyuu config",
        ),
    ] = False,
    nyuu: Annotated[
        bool,
        Parameter(
            help="only run nyuu",
            group=exclusive,
        ),
    ] = False,
    parpar: Annotated[
        bool,
        Parameter(
            help="only run parpar",
            group=exclusive,
        ),
    ] = False,
    raw: Annotated[
        bool,
        Parameter(
            help="only repost raw articles",
            group=exclusive,
        ),
    ] = False,
    skip_raw: Annotated[
        bool,
        Parameter(
            help="skip raw article reposting",
            group=exclusive,
        ),
    ] = False,
    clear_raw: Annotated[
        bool,
        Parameter(
            help="delete existing raw articles",
            group=exclusive,
        ),
    ] = False,
    exts: Annotated[
        Optional[list[str]],
        Parameter(
            help="file extensions to be matched, overrides config",
        ),
    ] = None,
    glob: Annotated[
        Optional[list[str]],
        Parameter(
            help="glob pattern(s) to be matched instead of extensions",
        ),
    ] = None,
    bdmv: Annotated[
        bool,
        Parameter(
            help="search for BDMVs in path, can be used with --glob",
        ),
    ] = False,
    debug: Annotated[
        bool,
        Parameter(
            env_var="JUICENET_DEBUG",
            help="show debug logs",
        ),
    ] = False,
    move: Annotated[
        bool,
        Parameter(
            help="move foobar.ext to foobar/foobar.ext",
            group=exclusive,
        ),
    ] = False,
    only_move: Annotated[
        bool,
        Parameter(
            help="move foobar.ext to foobar/foobar.ext and exit",
            group=exclusive,
        ),
    ] = False,
    no_resume: Annotated[
        bool,
        Parameter(
            help="ignore existing resume data",
        ),
    ] = False,
    clear_resume: Annotated[
        bool,
        Parameter(
            help="delete existing resume data",
            group=exclusive,
        ),
    ] = False,
) -> None:
    """
    CLI for juicenet. Does a bit of input validation thanks to cyclopts and then passes it over to juicenet.
    """

    main(
        path=path,
        config=config,
        public=public,
        only_nyuu=nyuu,
        only_parpar=parpar,
        only_raw=raw,
        skip_raw=skip_raw,
        clear_raw=clear_raw,
        glob=glob,
        bdmv=bdmv,
        debug=debug,
        move=move,
        only_move=only_move,
        extensions=exts,
        no_resume=no_resume,
        clear_resume=clear_resume,
    )
