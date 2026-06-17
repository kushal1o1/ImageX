from pathlib import Path
from typing import Any, Optional

import questionary
from PIL import Image

NAME = "Flip"
DESCRIPTION = "Mirror images horizontally or vertically"

OPTIONS = {
    "Horizontal (left ↔ right)": Image.FLIP_LEFT_RIGHT,
    "Vertical (top ↔ bottom)": Image.FLIP_TOP_BOTTOM,
}


def ask_args(files: list[Path]) -> dict[str, Any]:
    direction = questionary.select(
        "Flip direction:",
        choices=list(OPTIONS.keys()),
    ).ask()

    return {"method": OPTIONS[direction]}


def run(file: Path, output_path: Path, args: Optional[dict[str, Any]] = None) -> bool:
    if args is None:
        msg = "args required for flip"
        raise ValueError(msg)

    img = Image.open(file)
    flipped = img.transpose(args["method"])
    kw = {"format": img.format or "JPEG"}
    if exif := img.info.get("exif"):
        kw["exif"] = exif
    if icc := img.info.get("icc_profile"):
        kw["icc_profile"] = icc
    flipped.save(str(output_path), **kw)
    return True
