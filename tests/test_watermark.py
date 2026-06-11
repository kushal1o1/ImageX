import pytest
from PIL import Image

from imagex.features.watermark import run


@pytest.fixture
def logo_img(tmp_path):
    path = tmp_path / "logo.png"
    img = Image.new("RGBA", (20, 20), (255, 0, 0, 255))
    img.save(str(path))
    return path


class TestAddText:
    def test_text_watermark_renders(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "wm.png"
        args = {
            "action": "add",
            "type": "text",
            "text": "TEST",
            "font_size": 20,
            "color": "white",
            "position": "Top-Left",
            "opacity": 128,
        }
        assert run(src, out, args)

        result = Image.open(out)
        assert result.size == (50, 50)

    def test_text_watermark_all_positions(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        for pos in ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center"]:
            out = tmp_path / f"wm_{pos}.png"
            args = {
                "action": "add",
                "type": "text",
                "text": "X",
                "font_size": 16,
                "color": "white",
                "position": pos,
                "opacity": 255,
            }
            assert run(src, out, args)
            assert Image.open(out).size == (50, 50)

    def test_text_watermark_opacity_affects_output(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"

        out_low = tmp_path / "low.png"
        run(src, out_low, {
            "action": "add", "type": "text", "text": "W",
            "font_size": 16, "color": "white",
            "position": "Top-Left", "opacity": 10,
        })

        out_high = tmp_path / "high.png"
        run(src, out_high, {
            "action": "add", "type": "text", "text": "W",
            "font_size": 16, "color": "white",
            "position": "Top-Left", "opacity": 255,
        })

        px_low = list(Image.open(out_low).getdata())
        px_high = list(Image.open(out_high).getdata())
        assert px_low != px_high

    def test_text_watermark_preserves_size(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "wm.png"
        args = {
            "action": "add", "type": "text", "text": "Hello",
            "font_size": 20, "color": "red",
            "position": "Bottom-Right", "opacity": 200,
        }
        run(src, out, args)
        orig = Image.open(src)
        result = Image.open(out)
        assert result.size == orig.size

    def test_text_color(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "red.png"
        args = {
            "action": "add", "type": "text", "text": "W",
            "font_size": 16, "color": "red",
            "position": "Top-Left", "opacity": 255,
        }
        assert run(src, out, args)


class TestAddImage:
    def test_image_watermark_renders(self, tmp_images, tmp_path, logo_img):
        src = tmp_images / "test.jpg"
        out = tmp_path / "wm.png"
        args = {
            "action": "add",
            "type": "image",
            "logo_path": str(logo_img),
            "scale": 20,
            "position": "Bottom-Right",
            "opacity": 200,
        }
        assert run(src, out, args)
        assert Image.open(out).size == (50, 50)

    def test_image_watermark_preserves_size(self, tmp_images, tmp_path, logo_img):
        src = tmp_images / "test.jpg"
        out = tmp_path / "wm.png"
        args = {
            "action": "add", "type": "image",
            "logo_path": str(logo_img), "scale": 50,
            "position": "Center", "opacity": 255,
        }
        run(src, out, args)
        assert Image.open(out).size == (50, 50)

    def test_missing_logo_raises(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "wm.png"
        args = {
            "action": "add", "type": "image",
            "logo_path": "/nonexistent.png", "scale": 10,
            "position": "Top-Left", "opacity": 255,
        }
        with pytest.raises(FileNotFoundError):
            run(src, out, args)


class TestRemove:
    def test_remove_region_changes_pixels(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        original = Image.open(src)
        orig_pixels = list(original.getdata())

        out = tmp_path / "removed.png"
        args = {
            "action": "remove",
            "position": "Top-Right",
            "size_ratio": 0.2,
        }
        assert run(src, out, args)

        result = Image.open(out)
        assert result.size == (50, 50)

        result_pixels = list(result.getdata())
        changed = sum(1 for a, b in zip(orig_pixels, result_pixels) if a != b)
        assert changed > 0

    def test_remove_all_positions(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        for pos in ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center"]:
            out = tmp_path / f"rm_{pos}.png"
            args = {
                "action": "remove", "position": pos, "size_ratio": 0.15,
            }
            assert run(src, out, args)

    def test_remove_preserves_size(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "rm.png"
        run(src, out, {"action": "remove", "position": "Center", "size_ratio": 0.2})
        assert Image.open(out).size == (50, 50)

    def test_remove_different_sizes(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        for ratio in [0.1, 0.2, 0.3]:
            out = tmp_path / f"rm_{ratio}.png"
            assert run(src, out, {
                "action": "remove", "position": "Bottom-Left", "size_ratio": ratio,
            })


class TestErrors:
    def test_run_without_args_raises(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "out.png"
        with pytest.raises(ValueError, match="args required"):
            run(src, out, None)
