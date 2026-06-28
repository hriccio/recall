from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from recall.app.domain.source import utc_now_iso


@dataclass(frozen=True)
class Exam:
    source_id: str
    title: str
    question_ids: tuple[str, ...]
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
