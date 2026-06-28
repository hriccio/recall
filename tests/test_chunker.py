from pathlib import Path

from recall.app.domain.source import Source
from recall.app.services.source_chunker import SourceChunker


def make_source(text: str) -> Source:
    return Source(title="notes", file_path=Path("notes.md"), content_hash="hash", raw_text=text)


def test_chunks_markdown_by_heading() -> None:
    source = make_source("# Photosynthesis\n\nPlants convert light.\n\n## Respiration\n\nCells release energy.")

    chunks = SourceChunker().chunk(source)

    assert [chunk.heading for chunk in chunks] == ["Photosynthesis", "Respiration"]
    assert chunks[0].text == "Plants convert light."
    assert chunks[1].text == "Cells release energy."


def test_falls_back_to_paragraph_chunks() -> None:
    source = make_source("Alpha is a topic.\n\nBeta is another topic.\n\nGamma continues the notes.")

    chunks = SourceChunker(target_chars=30).chunk(source)

    assert len(chunks) == 3
    assert chunks[0].heading is None
