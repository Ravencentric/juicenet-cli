import json
import os
from pathlib import Path

import yaml


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
