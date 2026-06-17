from PIL import Image

from imagex.features.flip import run


def _marked_image(path, size=(4, 4)):
    """An all-black image with a single white pixel in the top-left corner."""
    img = Image.new("RGB", size, color="black")
    img.putpixel((0, 0), (255, 255, 255))
    img.save(str(path))
    return img


class TestFlipRun:
    def test_flip_horizontal_moves_pixel_left_to_right(self, tmp_path):
        src = tmp_path / "marked.png"
        _marked_image(src)
        out = tmp_path / "h.png"
        assert run(src, out, {"method": Image.FLIP_LEFT_RIGHT})

        flipped = Image.open(out)
        # top-left white pixel mirrors to the top-right
        assert flipped.getpixel((3, 0)) == (255, 255, 255)
        assert flipped.getpixel((0, 0)) == (0, 0, 0)

    def test_flip_vertical_moves_pixel_top_to_bottom(self, tmp_path):
        src = tmp_path / "marked.png"
        _marked_image(src)
        out = tmp_path / "v.png"
        assert run(src, out, {"method": Image.FLIP_TOP_BOTTOM})

        flipped = Image.open(out)
        # top-left white pixel mirrors to the bottom-left
        assert flipped.getpixel((0, 3)) == (255, 255, 255)
        assert flipped.getpixel((0, 0)) == (0, 0, 0)

    def test_preserves_dimensions(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        original = Image.open(src)
        out = tmp_path / "out.jpg"
        assert run(src, out, {"method": Image.FLIP_LEFT_RIGHT})

        flipped = Image.open(out)
        assert flipped.width == original.width
        assert flipped.height == original.height

    def test_double_flip_restores_original(self, tmp_path):
        src = tmp_path / "marked.png"
        _marked_image(src)
        once = tmp_path / "once.png"
        twice = tmp_path / "twice.png"
        run(src, once, {"method": Image.FLIP_LEFT_RIGHT})
        run(once, twice, {"method": Image.FLIP_LEFT_RIGHT})

        assert Image.open(twice).getpixel((0, 0)) == (255, 255, 255)

    def test_preserves_format(self, tmp_images, tmp_path):
        src = tmp_images / "image.webp"
        out = tmp_path / "out.webp"
        assert run(src, out, {"method": Image.FLIP_TOP_BOTTOM})

        flipped = Image.open(out)
        assert flipped.format == "WEBP"

    def test_run_without_args_raises(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "out.jpg"
        try:
            run(src, out, None)
            assert False, "should have raised"
        except ValueError as e:
            assert "args required" in str(e).lower()
