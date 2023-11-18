from pathlib import Path

from .compat import metadata, tomllib


def get_version() -> str:
    """
    Get the version
    """
    try:
        return metadata.version("juicenet-cli")

    except metadata.PackageNotFoundError:
        pyproject = Path(__file__).parent.with_name("pyproject.toml").read_text()
        version = tomllib.loads(pyproject)["tool"]["poetry"]["version"]

        return version  # type: ignore
