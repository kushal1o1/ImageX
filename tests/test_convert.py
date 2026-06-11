import pytest
from PIL import Image

from imagex.features.convert import OUTPUT_FORMATS, run


def _args(target_fmt: str):
    return {
        "target_format": target_fmt,
        "target_ext": OUTPUT_FORMATS[target_fmt],
    }


JPEG_ARGS = _args("JPEG")
PNG_ARGS = _args("PNG")
WEBP_ARGS = _args("WEBP")
TIFF_ARGS = _args("TIFF")
BMP_ARGS = _args("BMP")
GIF_ARGS = _args("GIF")


def test_jpeg_to_png(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.png"
    assert run(src, out, PNG_ARGS)

    img = Image.open(out)
    assert img.format == "PNG"


def test_png_to_jpeg(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.png"
    assert run(src, out, PNG_ARGS)

    img = Image.open(out)
    assert img.format == "PNG"


def test_png_alpha_to_jpeg_handles_alpha(tmp_images, tmp_path):
    src = tmp_images / "with_alpha.png"
    out = tmp_path / "out.jpg"
    assert run(src, out, JPEG_ARGS)

    img = Image.open(out)
    assert img.format == "JPEG"
    assert img.mode == "RGB"


def test_jpeg_to_webp(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.webp"
    assert run(src, out, WEBP_ARGS)

    img = Image.open(out)
    assert img.format == "WEBP"


def test_webp_to_png(tmp_images, tmp_path):
    src = tmp_images / "image.webp"
    out = tmp_path / "out.png"
    assert run(src, out, PNG_ARGS)

    img = Image.open(out)
    assert img.format == "PNG"


def test_jpeg_to_tiff(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.tiff"
    assert run(src, out, TIFF_ARGS)

    img = Image.open(out)
    assert img.format == "TIFF"


def test_jpeg_to_bmp(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.bmp"
    assert run(src, out, BMP_ARGS)

    img = Image.open(out)
    assert img.format == "BMP"


def test_jpeg_to_gif(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.gif"
    assert run(src, out, GIF_ARGS)

    img = Image.open(out)
    assert img.format == "GIF"


def test_converted_image_preserves_content(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    original = Image.open(src)
    out = tmp_path / "out.png"
    run(src, out, PNG_ARGS)

    converted = Image.open(out)
    assert converted.size == original.size

def test_jpeg_to_heic(tmp_images, tmp_path):
    pytest.importorskip("pillow_heif")
    import pillow_heif  # noqa: F401

    heic_args = _args("HEIC")
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.heic"
    assert run(src, out, heic_args)

    img = Image.open(out)
    assert img.format == "HEIF"


def test_heic_to_jpeg(tmp_images, tmp_path):
    pytest.importorskip("pillow_heif")
    import pillow_heif  # noqa: F401

    pillow_heif.register_heif_opener()
    src = tmp_path / "src.heic"
    Image.new("RGB", (50, 50), color="green").save(str(src), format="HEIF")

    out = tmp_path / "out.jpg"
    assert run(src, out, JPEG_ARGS)

    img = Image.open(out)
    assert img.format == "JPEG"


def test_run_without_args_raises(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.png"
    with pytest.raises(ValueError, match="args required"):
        run(src, out, None)


def test_all_non_heic_format_combinations(tmp_images, tmp_path):
    targets = ["JPEG", "PNG", "WEBP", "TIFF", "BMP", "GIF", "PNG"]
    src = tmp_images / "test.jpg"

    for t in targets:
        out = tmp_path / f"out{t.lower()}"
        assert run(src, out, _args(t)), f"Failed JPEG -> {t}"
