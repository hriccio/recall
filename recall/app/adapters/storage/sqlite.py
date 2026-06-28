from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from recall.app.domain.attempt import Answer, Attempt
from recall.app.domain.exam import Exam
from recall.app.domain.question import Question
from recall.app.domain.source import Source, SourceChunk


class SQLiteStore:
    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is None:
            db_path = Path.home() / ".local" / "share" / "recall" / "recall.sqlite3"
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_schema(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS sources (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    raw_text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    heading TEXT,
                    text TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES sources(id)
                );

                CREATE TABLE IF NOT EXISTS questions (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    chunk_id TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    choices_json TEXT NOT NULL,
                    correct_choice_index INTEGER NOT NULL,
                    explanation TEXT NOT NULL,
                    source_excerpt TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS exams (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    question_ids_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS attempts (
                    id TEXT PRIMARY KEY,
                    exam_id TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT NOT NULL,
                    score REAL NOT NULL,
                    answers_json TEXT NOT NULL
                );
                """
            )

    def save_source(self, source: Source, chunks: list[SourceChunk]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO sources
                (id, title, file_path, content_hash, raw_text, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (source.id, source.title, str(source.file_path), source.content_hash, source.raw_text, source.created_at),
            )
            connection.executemany(
                """
                INSERT OR REPLACE INTO chunks
                (id, source_id, chunk_index, heading, text)
                VALUES (?, ?, ?, ?, ?)
                """,
                [(chunk.id, chunk.source_id, chunk.index, chunk.heading, chunk.text) for chunk in chunks],
            )

    def save_questions(self, questions: list[Question]) -> None:
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT OR REPLACE INTO questions
                (id, source_id, chunk_id, prompt, choices_json, correct_choice_index, explanation, source_excerpt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        question.id,
                        question.source_id,
                        question.chunk_id,
                        question.prompt,
                        json.dumps(question.choices),
                        question.correct_choice_index,
                        question.explanation,
                        question.source_excerpt,
                    )
                    for question in questions
                ],
            )

    def save_exam(self, exam: Exam) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO exams
                (id, source_id, title, question_ids_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (exam.id, exam.source_id, exam.title, json.dumps(exam.question_ids), exam.created_at),
            )

    def save_attempt(self, attempt: Attempt) -> None:
        answers = [
            {
                "question_id": answer.question_id,
                "selected_choice_index": answer.selected_choice_index,
                "is_correct": answer.is_correct,
            }
            for answer in attempt.answers
        ]
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO attempts
                (id, exam_id, started_at, finished_at, score, answers_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (attempt.id, attempt.exam_id, attempt.started_at, attempt.finished_at, attempt.score, json.dumps(answers)),
            )

    def attempts_for_source(self, source_id: str) -> list[Attempt]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT attempts.*
                FROM attempts
                JOIN exams ON exams.id = attempts.exam_id
                WHERE exams.source_id = ?
                ORDER BY attempts.finished_at DESC
                """,
                (source_id,),
            ).fetchall()

        attempts: list[Attempt] = []
        for row in rows:
            answers = tuple(
                Answer(
                    question_id=item["question_id"],
                    selected_choice_index=item["selected_choice_index"],
                    is_correct=item["is_correct"],
                )
                for item in json.loads(row["answers_json"])
            )
            attempts.append(
                Attempt(
                    id=row["id"],
                    exam_id=row["exam_id"],
                    started_at=row["started_at"],
                    finished_at=row["finished_at"],
                    score=row["score"],
                    answers=answers,
                )
            )
        return attempts
