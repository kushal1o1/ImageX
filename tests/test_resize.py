from PIL import Image

from imagex.features.resize import _fit_within, run


class TestFitWithin:
    def test_no_upscale(self):
        assert _fit_within(100, 100, 200, 200) == (100, 100)

    def test_fit_width(self):
        w, h = _fit_within(200, 100, 100, 100)
        assert w == 100 and h == 50

    def test_fit_height(self):
        w, h = _fit_within(100, 200, 100, 100)
        assert w == 50 and h == 100

    def test_same_ratio(self):
        w, h = _fit_within(200, 100, 100, 50)
        assert w == 100 and h == 50

    def test_minimum_one(self):
        w, h = _fit_within(1, 1, 1, 1)
        assert w >= 1 and h >= 1


class TestResizeRun:
    def test_percentage_halves_size(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        img = Image.open(src)
        out = tmp_path / "half.png"
        assert run(src, out, {"method": "percentage", "value": 50})

        resized = Image.open(out)
        assert resized.width == img.width // 2
        assert resized.height == img.height // 2

    def test_exact_dimensions(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "exact.png"
        assert run(src, out, {"method": "exact", "width": 25, "height": 30})

        resized = Image.open(out)
        assert resized.width == 25
        assert resized.height == 30

    def test_fit_within_maintains_ratio(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"

        out = tmp_path / "fit.png"
        assert run(src, out, {"method": "fit", "max_width": 25, "max_height": 25})

        resized = Image.open(out)
        assert resized.width <= 25
        assert resized.height <= 25
        # aspect ratio should match (50x50 -> 25x25 since it's square)
        assert resized.width == resized.height

    def test_fit_no_upscale(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"

        out = tmp_path / "noscale.png"
        assert run(src, out, {"method": "fit", "max_width": 9999, "max_height": 9999})

        resized = Image.open(out)
        img = Image.open(src)
        assert resized.width == img.width
        assert resized.height == img.height

    def test_percentage_100_is_same(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        img = Image.open(src)

        out = tmp_path / "same.png"
        assert run(src, out, {"method": "percentage", "value": 100})

        resized = Image.open(out)
        assert resized.width == img.width
        assert resized.height == img.height

    def test_run_without_args_raises(self, tmp_images, tmp_path):
        src = tmp_images / "test.jpg"
        out = tmp_path / "out.jpg"
        try:
            run(src, out, None)
            assert False, "should have raised"
        except ValueError as e:
            assert "args required" in str(e).lower()
