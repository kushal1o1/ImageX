from pathlib import Path

import pytest

from imagex.config import BACKUP_DIR_NAME, is_image
from imagex.utils.file_ops import backup_file, find_images, get_output_path


def test_is_image():
    assert is_image(Path("photo.jpg"))
    assert is_image(Path("photo.jpeg"))
    assert is_image(Path("photo.png"))
    assert is_image(Path("photo.webp"))
    assert is_image(Path("photo.tiff"))
    assert is_image(Path("photo.tif"))
    assert is_image(Path("photo.bmp"))
    assert is_image(Path("photo.gif"))
    assert is_image(Path("photo.ico"))
    assert is_image(Path("photo.JPG"))
    assert not is_image(Path("photo.txt"))
    assert not is_image(Path("photo.pdf"))
    assert not is_image(Path("archive.zip"))


def test_find_images_finds_only_images(tmp_images: Path, non_image: Path):
    files = find_images(tmp_images)
    names = {f.name for f in files}

    assert "test.jpg" in names
    assert "with_alpha.png" in names
    assert "image.webp" in names
    assert "small.bmp" in names
    assert non_image.name not in names


def test_find_images_empty_dir(tmp_path: Path):
    assert find_images(tmp_path) == []


def test_find_images_no_images(tmp_path: Path):
    (tmp_path / "readme.md").write_text("# hello")
    assert find_images(tmp_path) == []


def test_get_output_path_overwrite(tmp_images: Path):
    f = tmp_images / "test.jpg"
    assert get_output_path(f, "overwrite") == f


def test_get_output_path_output(tmp_images: Path):
    f = tmp_images / "test.jpg"
    result = get_output_path(f, "output")
    assert result.parent.name == "output"
    assert result.name == "test.jpg"


def test_get_output_path_custom(tmp_images: Path):
    f = tmp_images / "test.jpg"
    custom = Path("/tmp/imagex-test-output")
    result = get_output_path(f, "custom", custom)
    assert result == custom / "test.jpg"


def test_get_output_path_custom_requires_dir(tmp_images: Path):
    f = tmp_images / "test.jpg"
    with pytest.raises(ValueError, match="output_dir required"):
        get_output_path(f, "custom")


def test_get_output_path_invalid_mode(tmp_images: Path):
    f = tmp_images / "test.jpg"
    with pytest.raises(ValueError, match="Unknown output mode"):
        get_output_path(f, "unknown")


def test_backup_file_creates_backup(tmp_images: Path, tmp_path: Path):
    src = tmp_images / "test.jpg"
    backup = backup_file(src)

    assert backup.exists()
    assert backup.name == "test.jpg"
    assert BACKUP_DIR_NAME in str(backup.parent)


def test_backup_file_is_copy(tmp_images: Path, tmp_path: Path):
    src = tmp_images / "test.jpg"
    original_bytes = src.read_bytes()
    backup = backup_file(src)

    assert backup.read_bytes() == original_bytes
