from typing import Optional

from .compat import NotRequired, TypedDict


class JuicenetConfig(TypedDict):
    """TypedDict for `yaml.safe_load()` output since it simply returns `Any` and leaves"""

    # Required keys
    PARPAR: str
    """The path to the ParPar binary"""
    NYUU: str
    """The path to the Nyuu executable"""
    NZB_OUTPUT_PATH: str
    """The path where NZB files will be saved"""
    NYUU_CONFIG_PRIVATE: str
    """The path to the private Nyuu configuration file"""
    EXTENSIONS: list[str]
    """The list of file extensions to be processed"""
    PARPAR_ARGS: list[str]
    """The arguments to be passed to the ParPar binary"""

    # Optional keys
    USE_TEMP_DIR: NotRequired[bool]
    """Whether or not to use a temporary directory for processing"""
    TEMP_DIR_PATH: NotRequired[Optional[str]]
    """Path to a specific temporary directory if USE_TEMP_DIR is True. If unspecified, it uses %Temp% or /tmp"""
    NYUU_CONFIG_PUBLIC: NotRequired[str]
    """The path to the public Nyuu configuration file (falls back to private config if not specified)"""
    APPDATA_DIR_PATH: NotRequired[str]
    """The path to the folder where juicenet will store it's resume data, defaults to ~/.juicenet/"""
