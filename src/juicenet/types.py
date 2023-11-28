from .compat import NotRequired, TypedDict


class JuicenetConfig(TypedDict):
    """TypedDict for yaml.safe_load output since it simply returns `any` and leaves"""

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
    PAR2_OUTPUT_PATH: NotRequired[str]
    """The path where PAR2 files will be saved (cwd if not specified)"""
    NYUU_CONFIG_PUBLIC: NotRequired[str]
    """The path to the public Nyuu configuration file (falls back to private config if not specified)"""
