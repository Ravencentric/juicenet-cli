from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import loguru

if TYPE_CHECKING:
    from rich.console import Console


def _log_formatter(record: loguru.Record) -> str:
    """
    Log message formatter
    https://github.com/Textualize/rich/issues/2416#issuecomment-1193773381

    Slightly modified to match loguru's default color scheme and my own preference

    Output:

    ```log
    2024-01-20 00:03:47 | TRACE    | hello
    2024-01-20 00:03:47 | DEBUG    | hello
    2024-01-20 00:03:47 | INFO     | hello
    2024-01-20 00:03:47 | SUCCESS  | hello
    2024-01-20 00:03:47 | WARNING  | hello
    2024-01-20 00:03:47 | ERROR    | hello
    2024-01-20 00:03:47 | CRITICAL | hello
    ```
    """
    colors = {
        # default loguru colors
        # loguru also bolds by default
        "TRACE": "bold cyan",
        "DEBUG": "bold blue",
        "INFO": "bold white",
        "SUCCESS": "bold green",
        "WARNING": "bold yellow",
        "ERROR": "bold red",
        "CRITICAL": "bold white on red",
    }
    level = colors.get(record["level"].name, "bold white")
    return (
        # loguru does not bold timestamp by default
        "[not bold green]{time:YYYY-MM-DD HH:mm:ss}[/not bold green]"
        " | "
        f"[{level}]{{level: <8}}[/{level}]"
        " | "
        f"[{level}]{{message}}[/{level}]"
    )


def get_logger(
    logger: loguru.Logger,
    level: Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"],
    sink: Console,
    *,
    disable: bool = False,
) -> loguru.Logger:
    """
    Configure loguru
    """
    # Remove all existing handlers
    logger.remove()

    if not disable:
        logger = logger.opt(colors=True)

        config = {
            "handlers": [
                {
                    "sink": sink.print,
                    "format": _log_formatter,
                    "colorize": True,
                    "level": level,
                },
            ],
        }

        logger.configure(**config)  # type: ignore

    return logger
