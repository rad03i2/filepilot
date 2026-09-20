from pathlib import Path

import pytest

from filepilot.core import apply_plan, build_plan, category_for, file_sha256, undo


def test_categories_are_case_insensitive():
    assert category_for(Path("photo.JPG")) == "Images"
    assert category_for(Path("report.PDF")) == "Documents"
    assert category_for(Path("unknown.xyz")) == "Other"


def test_plan_avoids_name_collisions(tmp_path):
    source = tmp_path / "in"
    destination = tmp_path / "out"
    source.mkdir()
    (source / "a.txt").write_text("new", encoding="utf-8")
    (destination / "Documents").mkdir(parents=True)
    (destination / "Documents" / "a.txt").write_text("old", encoding="utf-8")
    moves = build_plan(source, destination)
    assert len(moves) == 1
    assert Path(moves[0].destination).name == "a (1).txt"


def test_apply_and_undo_round_trip(tmp_path):
    source = tmp_path / "in"
    destination = tmp_path / "out"
    source.mkdir()
    original = source / "notes.txt"
    original.write_text("hello", encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    moves = build_plan(source, destination)
    apply_plan(moves, manifest)
    moved = destination / "Documents" / "notes.txt"
    assert moved.read_text(encoding="utf-8") == "hello"
    assert not original.exists()
    assert undo(manifest) == 1
    assert original.read_text(encoding="utf-8") == "hello"


def test_recursive_same_destination_is_rejected(tmp_path):
    with pytest.raises(ValueError):
        build_plan(tmp_path, recursive=True)


def test_hidden_files_are_ignored_by_default(tmp_path):
    (tmp_path / ".secret.txt").write_text("secret", encoding="utf-8")
    assert build_plan(tmp_path) == []
    assert len(build_plan(tmp_path, include_hidden=True)) == 1


def test_sha256(tmp_path):
    path = tmp_path / "hello.txt"
    path.write_bytes(b"hello")
    assert file_sha256(path) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
