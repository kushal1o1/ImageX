from pathlib import Path

from PIL import Image
from PIL.ExifTags import Base

from imagex.features.remove_metadata import run


def test_remove_jpeg_exif(jpg_with_exif: Path, tmp_path: Path):
    out = tmp_path / "cleaned.jpg"
    assert run(jpg_with_exif, out)

    reopened = Image.open(out)
    exif = reopened.getexif()
    exif_dict = dict(exif)

    assert Base.Make not in exif_dict
    assert Base.Model not in exif_dict
    assert Base.Software not in exif_dict


def test_remove_metadata_preserves_image(jpg_with_exif: Path, tmp_path: Path):
    original = Image.open(jpg_with_exif)
    out = tmp_path / "cleaned.jpg"
    run(jpg_with_exif, out)

    cleaned = Image.open(out)
    assert cleaned.size == original.size
    assert cleaned.mode == original.mode


def test_png_no_exif_is_noop(tmp_images: Path, tmp_path: Path):
    src = tmp_images / "with_alpha.png"
    out = tmp_path / "out.png"
    assert run(src, out)

    reopened = Image.open(out)
    assert reopened.format == "PNG"


def test_webp_no_exif_is_noop(tmp_images: Path, tmp_path: Path):
    src = tmp_images / "image.webp"
    out = tmp_path / "out.webp"
    assert run(src, out)

    reopened = Image.open(out)
    assert reopened.format == "WEBP"


def test_jpeg_without_exif_stays_clean(tmp_images: Path, tmp_path: Path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.jpg"
    assert run(src, out)

    reopened = Image.open(out)
    assert len(dict(reopened.getexif())) == 0


def test_bmp_metadata_removal(tmp_images: Path, tmp_path: Path):
    src = tmp_images / "small.bmp"
    out = tmp_path / "out.bmp"
    assert run(src, out)

    reopened = Image.open(out)
    assert reopened.format == "BMP"
