from pathlib import Path

from recall.app.adapters.ai.fake import FakeQuestionGenerator
from recall.app.domain.source import Source
from recall.app.services.source_chunker import SourceChunker


def test_generates_deterministic_multiple_choice_questions() -> None:
    source = Source(
        title="notes",
        file_path=Path("notes.md"),
        content_hash="hash",
        raw_text=(
            "# Memory\n\nActive recall improves retention by forcing retrieval from memory.\n\n"
            "# Sleep\n\nSleep supports consolidation and helps stabilize newly learned material."
        ),
    )
    chunks = SourceChunker().chunk(source)

    questions = FakeQuestionGenerator().generate_questions(chunks, 2)

    assert len(questions) == 2
    assert all(len(question.choices) == 4 for question in questions)
    assert questions[0].correct_choice_index == 0
    assert questions[1].correct_choice_index == 1
    assert "Active recall" in questions[0].source_excerpt
