from .compat import metadata


def get_version() -> str:
    """
    Get the version of juicenet
    """
    try:
        return metadata.version("juicenet-cli")

    except metadata.PackageNotFoundError:
        return "0.0.0"
