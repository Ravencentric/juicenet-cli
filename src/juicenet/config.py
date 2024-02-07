import json
from dataclasses import asdict
from pathlib import Path
from typing import Union

import yaml

from .model import JuicenetConfig
from .types import Config


def read_config(config: Union[Path, Config]) -> JuicenetConfig:
    """
    Reads the yaml config file

    Returns a JuicenetConfig object with the data validated and type casted
    """
    if isinstance(config, Path):
        data = yaml.safe_load(config.read_text()) or {}
    elif isinstance(config, Config):
        data = {key.upper(): value for key, value in asdict(config).items() if value is not None}
    else:
        raise ValueError("Config must be a pathlib.Path or juicenet.Config")

    return JuicenetConfig.model_validate(data)


def get_dump_failed_posts(conf: Path) -> Path:
    """
    Get the value of `dump-failed-posts` from Nyuu config
    """
    data = json.loads(conf.read_text())
    return Path(data["dump-failed-posts"]).resolve()
