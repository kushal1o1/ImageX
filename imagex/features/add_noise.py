import random
from pathlib import Path
from typing import Any

import questionary
from PIL import Image

NAME = "Add Noise"
DESCRIPTION = "Add subtle pixel noise (helps bypass AI detection)"


def ask_args(files: list[Path]) -> dict[str, Any]:
    intensity_val = questionary.text(
        "Noise intensity (1-100, higher = more visible):",
        default="5",
        validate=lambda v: v.isdigit() and 1 <= int(v) <= 100 or "Enter 1-100",
    ).ask()

    noise_type = questionary.select(
        "Noise type:",
        choices=[
            "Gaussian (subtle, uniform)",
            "Salt & Pepper (random pixels)",
        ],
    ).ask()

    return {
        "intensity": int(intensity_val),
        "noise_type": "gaussian" if "Gaussian" in noise_type else "salt_pepper",
    }


def run(file: Path, output_path: Path, args: dict[str, Any] | None = None) -> bool:
    if args is None:
        msg = "args required for add_noise"
        raise ValueError(msg)

    intensity = args["intensity"]
    noise_type = args.get("noise_type", "gaussian")
    img = Image.open(file)

    if noise_type == "gaussian":
        _add_gaussian_noise(img, intensity)
    else:
        _add_salt_pepper(img, intensity)

    img.save(str(output_path), format=img.format or "JPEG")
    return True


def _add_gaussian_noise(img: Image.Image, intensity: int):
    pixels = img.load()
    w, h = img.size
    scale = intensity / 100
    noise_range = int(scale * 60)
    num_pixels = int(w * h * scale * 0.8)

    for _ in range(num_pixels):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        px = list(pixels[x, y])
        for c in range(min(len(px), 3)):
            px[c] = max(0, min(255, px[c] + random.randint(-noise_range, noise_range)))
        pixels[x, y] = tuple(px)


def _add_salt_pepper(img: Image.Image, intensity: int):
    pixels = img.load()
    w, h = img.size
    scale = intensity / 100
    num_pixels = int(w * h * scale * 0.3)

    for _ in range(num_pixels):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        px = list(pixels[x, y])
        val = 255 if random.random() < 0.5 else 0
        for c in range(min(len(px), 3)):
            px[c] = val
        pixels[x, y] = tuple(px)
