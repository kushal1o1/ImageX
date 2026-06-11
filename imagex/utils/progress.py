from pathlib import Path
from typing import Any, Callable

from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from imagex.utils.file_ops import backup_file, get_output_path


def process_files(
    files: list[Path],
    process_func: Callable[[Path, Path, dict[str, Any]], bool],
    feature_name: str,
    output_mode: str,
    output_dir: Path | None = None,
    args: dict[str, Any] | None = None,
):
    if args is None:
        args = {}

    with Progress(
        TextColumn(f"[bold blue]{feature_name}[/bold blue]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("• {task.completed}/{task.total}"),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Processing...", total=len(files))

        for file in files:
            try:
                output_path = get_output_path(file, output_mode, output_dir)

                if output_mode == "overwrite":
                    backup_file(file)

                output_path.parent.mkdir(parents=True, exist_ok=True)
                process_func(file, output_path, args)

            except Exception as e:
                progress.console.print(
                    f"[red]✗ {file.name}: {e}[/red]"
                )

            progress.advance(task)
