from __future__ import annotations

import hashlib
from pathlib import Path

from recall.app.domain.source import Source


class TextLoader:
    SUPPORTED_SUFFIXES = {".txt", ".md"}

    def __init__(self, max_bytes: int = 5_000_000) -> None:
        self.max_bytes = max_bytes

    def load(self, file_path: str | Path) -> Source:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")
        if path.suffix.lower() not in self.SUPPORTED_SUFFIXES:
            raise ValueError("Recall currently supports only .txt and .md files.")
        if path.stat().st_size > self.max_bytes:
            raise ValueError("File is too large for this first version of Recall.")

        raw_text = path.read_text(encoding="utf-8").strip()
        if not raw_text:
            raise ValueError("The selected file is empty.")

        content_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        return Source(
            title=path.stem,
            file_path=path,
            content_hash=content_hash,
            raw_text=raw_text,
        )
