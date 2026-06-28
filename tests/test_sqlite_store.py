from pathlib import Path

from recall.app.adapters.storage.sqlite import SQLiteStore
from recall.app.domain.attempt import Answer, Attempt
from recall.app.domain.exam import Exam
from recall.app.domain.question import Question
from recall.app.domain.source import Source, SourceChunk


def test_saves_attempts_for_source(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "recall.sqlite3")
    source = Source(title="notes", file_path=tmp_path / "notes.md", content_hash="hash", raw_text="Study text.")
    chunk = SourceChunk(source_id=source.id, index=0, text="Study text.")
    question = Question(
        source_id=source.id,
        chunk_id=chunk.id,
        prompt="Prompt?",
        choices=("one", "two", "three", "four"),
        correct_choice_index=0,
        explanation="Explanation.",
        source_excerpt="Study text.",
    )
    exam = Exam(source_id=source.id, title="Exam", question_ids=(question.id,))
    attempt = Attempt(exam_id=exam.id, answers=(Answer(question.id, 0, True),), score=100.0)

    store.save_source(source, [chunk])
    store.save_questions([question])
    store.save_exam(exam)
    store.save_attempt(attempt)

    attempts = store.attempts_for_source(source.id)

    assert len(attempts) == 1
    assert attempts[0].score == 100.0
    assert attempts[0].answers[0].is_correct is True
