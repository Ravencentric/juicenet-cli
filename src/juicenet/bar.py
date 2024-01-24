from __future__ import annotations

from typing import TYPE_CHECKING

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

if TYPE_CHECKING:
    from rich.console import Console


def progress_bar(console: Console, transient: bool = False, disable: bool = False) -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TaskProgressColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        console=console,
        transient=transient,
        disable=disable,
    )


# The above progress_bar ends up looking like this:
# Nyuu... ⠼ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1000/1000 • 100% • 0:00:10
