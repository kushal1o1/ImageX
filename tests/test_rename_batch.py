
import pytest

from imagex.features.rename_batch import run


def test_rename_single_file(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    dst = tmp_path / "renamed.jpg"
    src_renamed = tmp_path / "renamed.jpg"

    args = {"rename_map": {str(src): "renamed.jpg"}, "sorted_files": [str(src)]}
    result = run(src, dst, args)

    assert result
    assert src_renamed.exists()


def test_rename_multiple_files(tmp_images, tmp_path):
    files = sorted(tmp_images.iterdir())
    rename_map = {}
    for i, f in enumerate(files):
        new_name = f"photo_{i:03d}{f.suffix}"
        rename_map[str(f)] = new_name

    args = {"rename_map": rename_map, "sorted_files": [str(f) for f in files]}
    for f in files:
        dst = f  # doesn't matter for rename
        assert run(f, dst, args)

    for i, f in enumerate(files):
        assert not f.exists()
        assert (f.parent / f"photo_{i:03d}{f.suffix}").exists()


def test_rename_preserves_extension(tmp_images, tmp_path):
    src = tmp_images / "image.webp"
    dst = tmp_path / "out"
    args = {"rename_map": {str(src): "vacation.webp"}, "sorted_files": [str(src)]}
    run(src, dst, args)

    renamed = src.parent / "vacation.webp"
    assert renamed.exists()
    assert renamed.suffix == ".webp"


def test_rename_noop_same_name(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    dst = tmp_path / "out"
    args = {"rename_map": {str(src): "test.jpg"}, "sorted_files": [str(src)]}
    assert run(src, dst, args)
    assert src.exists()


def test_rename_without_args_raises(tmp_images, tmp_path):
    src = tmp_images / "test.jpg"
    dst = tmp_path / "out"
    with pytest.raises(ValueError, match="args required"):
        run(src, dst, None)
