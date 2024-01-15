import json
from pathlib import Path

import yaml

from .model import JuicenetConfig


def read_config(path: Path) -> JuicenetConfig:
    """
    Reads the yaml config file

    Returns a JuicenetConfig object with the data validated and type casted
    """
    data = yaml.safe_load(path.read_text()) or {}

    return JuicenetConfig.model_validate(data)


def get_dump_failed_posts(conf: Path) -> Path:
    """
    Get the value of `dump-failed-posts` from Nyuu config
    """
    data = json.loads(conf.read_text())
    return Path(data["dump-failed-posts"]).resolve()
