from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from recall.app.domain.source import utc_now_iso


@dataclass(frozen=True)
class Answer:
    question_id: str
    selected_choice_index: int | None
    is_correct: bool


@dataclass(frozen=True)
class Attempt:
    exam_id: str
    answers: tuple[Answer, ...]
    score: float
    id: str = field(default_factory=lambda: str(uuid4()))
    started_at: str = field(default_factory=utc_now_iso)
    finished_at: str = field(default_factory=utc_now_iso)
