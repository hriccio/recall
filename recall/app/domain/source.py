from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Source:
    title: str
    file_path: Path
    content_hash: str
    raw_text: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class SourceChunk:
    source_id: str
    index: int
    text: str
    heading: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
