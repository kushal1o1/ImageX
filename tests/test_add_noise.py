from PIL import Image

from imagex.features.add_noise import run


def test_gaussian_noise_runs(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "noisy.jpg"
    assert run(src, out, {"intensity": 10, "noise_type": "gaussian"})

    result = Image.open(out)
    assert result.format == "JPEG"
    assert result.size == (50, 50)


def test_salt_pepper_noise_runs(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    out = tmp_path / "sp.jpg"
    assert run(src, out, {"intensity": 10, "noise_type": "salt_pepper"})

    result = Image.open(out)
    assert result.format == "JPEG"
    assert result.size == (50, 50)


def test_noise_changes_pixels(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    original = Image.open(src)
    orig_pixels = list(original.getdata())

    out = tmp_path / "noisy.jpg"
    run(src, out, {"intensity": 80, "noise_type": "gaussian"})

    noisy = Image.open(out)
    noisy_pixels = list(noisy.getdata())

    changed = sum(1 for a, b in zip(orig_pixels, noisy_pixels) if a != b)
    assert changed > 0


def test_noise_on_png_alpha(tmp_images, tmp_path):
    src = tmp_images / "with_alpha.png"
    out = tmp_path / "noisy.png"
    assert run(src, out, {"intensity": 5, "noise_type": "gaussian"})

    result = Image.open(out)
    assert result.format == "PNG"


def test_low_intensity_minimal_change(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    original = Image.open(src)
    orig_pixels = list(original.getdata())

    out = tmp_path / "tiny.jpg"
    run(src, out, {"intensity": 1, "noise_type": "gaussian"})

    noisy = Image.open(out)
    noisy_pixels = list(noisy.getdata())

    changed = sum(1 for a, b in zip(orig_pixels, noisy_pixels) if a != b)
    assert changed < len(orig_pixels)


def test_salt_pepper_changes_pixels(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    original = Image.open(src)
    orig_pixels = list(original.getdata())

    out = tmp_path / "sp.jpg"
    run(src, out, {"intensity": 50, "noise_type": "salt_pepper"})

    noisy = Image.open(out)
    noisy_pixels = list(noisy.getdata())

    changed = sum(1 for a, b in zip(orig_pixels, noisy_pixels) if a != b)
    assert changed > 0


def test_run_without_args_raises(tmp_images, tmp_path):
    import pytest

    src = tmp_images / "test.jpg"
    out = tmp_path / "out.jpg"
    with pytest.raises(ValueError, match="args required"):
        run(src, out, None)
