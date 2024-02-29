import json
from pathlib import Path
from typing import Union

import yaml

from .exceptions import JuicenetInputError
from .model import JuicenetConfig


def read_config(config: Union[Path, JuicenetConfig]) -> JuicenetConfig:
    """
    Reads the yaml config file

    Returns a JuicenetConfig object with the data validated and type casted
    """
    if isinstance(config, Path):
        data = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
        lower = {key.lower(): value for key, value in data.items() if value is not None}
        return JuicenetConfig.model_validate(lower)

    elif isinstance(config, JuicenetConfig):
        return config

    else:
        raise JuicenetInputError("Config must be a pathlib.Path or juicenet.JuicenetConfig")


def get_dump_failed_posts(conf: Path) -> Path:
    """
    Get the value of `dump-failed-posts` from Nyuu config
    """
    data = json.loads(conf.read_text(encoding="utf-8"))
    return Path(data["dump-failed-posts"]).resolve()
