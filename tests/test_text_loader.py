from pathlib import Path

import pytest

from recall.app.adapters.files.text_loader import TextLoader


def test_loads_markdown_source(tmp_path: Path) -> None:
    file_path = tmp_path / "biology.md"
    file_path.write_text("# Cells\n\nCells contain organelles.", encoding="utf-8")

    source = TextLoader().load(file_path)

    assert source.title == "biology"
    assert source.file_path == file_path
    assert source.content_hash
    assert "organelles" in source.raw_text


def test_rejects_unsupported_file(tmp_path: Path) -> None:
    file_path = tmp_path / "notes.pdf"
    file_path.write_text("not really a pdf", encoding="utf-8")

    with pytest.raises(ValueError, match=".txt and .md"):
        TextLoader().load(file_path)


def test_rejects_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "empty.txt"
    file_path.write_text("   ", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        TextLoader().load(file_path)
