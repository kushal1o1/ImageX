import sys
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel

from imagex import __version__
from imagex.features import get_features
from imagex.utils.file_ops import find_images
from imagex.utils.progress import process_files

console = Console()


def fmt_size(size: int) -> str:
    for unit in ("B", "KB", "MB"):
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def show_banner():
    text = (
        f"[bold cyan]ImageX[/bold cyan] [white]v{__version__}[/white]\n"
        "[dim]Image processing, right in ur CLI[/dim]"
    )
    console.print(Panel(text, width=50))


def select_features() -> list[str] | None:
    features = get_features()

    if not features:
        console.print("[red]No features found! Add a .py file to imagex/features/.[/red]")
        return None

    choices = []
    for name, info in features.items():
        label = f"{info['name']:<30} {info['description']}"
        choices.append(questionary.Choice(title=label, value=name))

    choices.append(questionary.Choice(title="[Done] Quit", value="__quit__"))

    selected = questionary.checkbox(
        "What do you want to do? (↑↓ to move, Space to toggle, Enter to confirm)",
        choices=choices,
    ).ask()

    if not selected:
        return None

    if "__quit__" in selected:
        return None

    return selected


def ask_output_mode() -> tuple[str, Path | None]:
    mode = questionary.select(
        "Where should the processed images go?",
        choices=[
            questionary.Choice(
                title="Overwrite originals (backup created in .imagex_backup/)",
                value="overwrite",
            ),
            questionary.Choice(
                title="Save to ./output/ folder",
                value="output",
            ),
            questionary.Choice(
                title="Save to custom folder",
                value="custom",
            ),
        ],
    ).ask()

    output_dir = None
    if mode == "custom":
        custom = questionary.text(
            "Enter output folder path:",
            validate=lambda p: len(p.strip()) > 0 or "Path cannot be empty",
        ).ask()
        output_dir = Path(custom.strip())

    return mode, output_dir


def select_files(all_files: list[Path]) -> list[Path] | None:
    if not all_files:
        return None

    if len(all_files) == 1:
        return all_files

    all_choice = questionary.Choice(
        title=f"All images ({len(all_files)} files)",
        value="__all__",
    )

    file_choices = []
    for f in all_files:
        size_str = fmt_size(f.stat().st_size)
        label = f"{f.name:<50} {size_str:>8}"
        file_choices.append(questionary.Choice(title=label, value=str(f)))

    selected = questionary.checkbox(
        "Which images to process? (Space to toggle, Enter to confirm)",
        choices=[all_choice] + file_choices,
    ).ask()

    if not selected:
        return None

    if "__all__" in selected:
        return all_files

    return [Path(f) for f in selected]


def main():
    try:
        show_banner()

        selected = select_features()
        if selected is None:
            console.print("[yellow]No feature selected. Exiting.[/yellow]")
            return

        all_files = find_images(Path.cwd())
        if not all_files:
            console.print("[red]No image files found in current directory.[/red]")
            console.print("[dim]Supported: .jpg .jpeg .png .webp .tiff .tif .bmp .gif .ico[/dim]")
            return

        files = select_files(all_files)
        if not files:
            console.print("[yellow]No files selected. Exiting.[/yellow]")
            return

        console.print(f"[green]Selected {len(files)} image(s)[/green]")

        features = get_features()
        any_needs_output = any(
            info.get("needs_output", True)
            for name, info in features.items()
            if name in selected
        )

        if any_needs_output:
            mode, output_dir = ask_output_mode()
        else:
            mode, output_dir = "overwrite", None

        for feature_name in selected:
            info = features[feature_name]
            ask_args = info.get("ask_args")
            feature_args = ask_args(files) if ask_args else {}
            console.print(f"\n[bold]→ {info['name']}[/bold]")
            process_files(
                files=files,
                process_func=info["run"],
                feature_name=info["name"],
                output_mode=mode,
                output_dir=output_dir,
                args=feature_args,
            )

        console.print("\n[bold green]✓ All done![/bold green]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Exiting.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)
