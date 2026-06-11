from pathlib import Path

import pytest
from PIL import Image
from PIL.ExifTags import Base


@pytest.fixture
def tmp_images(tmp_path: Path) -> Path:
    img = Image.new("RGB", (50, 50), color="red")
    img.save(str(tmp_path / "test.jpg"))

    rgba = Image.new("RGBA", (50, 50), (255, 0, 0, 128))
    rgba.save(str(tmp_path / "with_alpha.png"))

    blue = Image.new("RGB", (50, 50), color="blue")
    blue.save(str(tmp_path / "image.webp"))

    white = Image.new("RGB", (30, 30), color="white")
    white.save(str(tmp_path / "small.bmp"))

    return tmp_path


@pytest.fixture
def jpg_with_exif(tmp_path: Path) -> Path:
    path = tmp_path / "exif.jpg"
    img = Image.new("RGB", (50, 50), color="green")
    exif = img.getexif()
    exif[Base.Make] = "TestCamera"
    exif[Base.Model] = "AI-Gen-9000"
    exif[Base.Software] = "StableDiffusion"
    exif[Base.XResolution] = 72
    img.save(str(path), exif=exif)
    return path


@pytest.fixture
def single_jpg(tmp_path: Path) -> Path:
    path = tmp_path / "single.jpg"
    Image.new("RGB", (10, 10), color="red").save(str(path))
    return path


@pytest.fixture
def non_image(tmp_path: Path) -> Path:
    path = tmp_path / "notes.txt"
    path.write_text("not an image")
    return path
