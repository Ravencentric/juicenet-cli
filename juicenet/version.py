from importlib import metadata
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # Python 3.10 compatibility


def get_version() -> str:
    """
    Get the version
    """
    try:
        return metadata.version("juicenet-cli")

    except metadata.PackageNotFoundError:
        pyproject = Path(__file__).parent.with_name("pyproject.toml").read_text()
        version = tomllib.loads(pyproject)["tool"]["poetry"]["version"]

        return version
