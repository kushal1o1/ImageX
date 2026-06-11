from PIL import Image

from imagex.features.compress import _fmt_size, run


def test_compress_jpeg_reduces_size(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "compressed.jpg"
    assert run(src, out, {"quality": 20})
    assert out.stat().st_size < src.stat().st_size


def test_compress_png(tmp_images, tmp_path):
    src = tmp_images / "with_alpha.png"
    out = tmp_path / "compressed.png"
    assert run(src, out, {"quality": 80})
    assert out.exists()
    reopened = Image.open(out)
    assert reopened.format == "PNG"


def test_compress_webp(tmp_images, tmp_path):
    src = tmp_images / "image.webp"
    out = tmp_path / "compressed.webp"
    assert run(src, out, {"quality": 50})
    assert out.exists()
    reopened = Image.open(out)
    assert reopened.format == "WEBP"


def test_higher_quality_produces_larger_file(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"

    out_low = tmp_path / "low.jpg"
    run(src, out_low, {"quality": 10})

    out_high = tmp_path / "high.jpg"
    run(src, out_high, {"quality": 95})

    assert out_low.stat().st_size < out_high.stat().st_size


def test_png_low_quality_quantizes(tmp_images, tmp_path):
    from PIL import Image

    src = tmp_path / "rgb.png"
    Image.new("RGB", (50, 50), color="red").save(str(src))

    out = tmp_path / "quantized.png"
    assert run(src, out, {"quality": 10})

    reopened = Image.open(out)
    assert reopened.mode == "P"


def test_compress_bmp_works(tmp_images, tmp_path):
    src = tmp_images / "small.bmp"
    out = tmp_path / "compressed.bmp"
    assert run(src, out, {"quality": 50})
    reopened = Image.open(out)
    assert reopened.format == "BMP"


def test_run_without_args_raises(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "out.jpg"
    try:
        run(src, out, None)
        assert False, "should have raised"
    except ValueError as e:
        assert "quality" in str(e).lower()


def test_fmt_size():
    assert _fmt_size(500) == "500 B"
    assert _fmt_size(2048) == "2 KB"
    assert _fmt_size(2_500_000) == "2 MB"
    assert _fmt_size(2_500_000_000) == "2.3 GB"
