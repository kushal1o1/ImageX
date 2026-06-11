from pathlib import Path

from imagex.cli import fmt_size, select_files


class TestFmtSize:
    def test_bytes(self):
        assert fmt_size(500) == "500 B"

    def test_kilobytes(self):
        assert fmt_size(1500) == "1 KB"

    def test_megabytes(self):
        assert fmt_size(2_500_000) == "2 MB"

    def test_gigabytes(self):
        assert fmt_size(2_500_000_000) == "2.3 GB"

    def test_zero(self):
        assert fmt_size(0) == "0 B"


class TestSelectFiles:
    def test_none_when_no_files(self):
        assert select_files([]) is None

    def test_auto_select_single(self, single_jpg: Path):
        result = select_files([single_jpg])
        assert result == [single_jpg]

    def test_multiple_returns_none_when_cancelled(self, tmp_images: Path, monkeypatch):
        files = sorted(tmp_images.iterdir())

        class FakeCheckbox:
            def ask(self):
                return None

        monkeypatch.setattr("questionary.checkbox", lambda *a, **kw: FakeCheckbox())
        result = select_files(files)
        assert result is None


def test_features_registered():
    from imagex.features import get_features

    features = get_features()
    names = [v["name"] for v in features.values()]

    assert "Remove Metadata" in names
    assert "Convert Format" in names
    assert len(features) >= 2


def test_feature_registry_structure():
    from imagex.features import get_features

    for name, info in get_features().items():
        assert "name" in info
        assert "description" in info
        assert "run" in info
        assert callable(info["run"])
