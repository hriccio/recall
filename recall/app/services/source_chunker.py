from __future__ import annotations

import re

from recall.app.domain.source import Source, SourceChunk


class SourceChunker:
    def __init__(self, target_chars: int = 1_200) -> None:
        self.target_chars = target_chars

    def chunk(self, source: Source) -> list[SourceChunk]:
        text = source.raw_text.strip()
        if not text:
            return []

        heading_chunks = self._chunk_markdown_headings(source)
        if heading_chunks:
            return heading_chunks

        return self._chunk_paragraphs(source)

    def _chunk_markdown_headings(self, source: Source) -> list[SourceChunk]:
        sections: list[tuple[str, list[str]]] = []
        current_heading: str | None = None
        current_lines: list[str] = []

        for line in source.raw_text.splitlines():
            match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if match:
                if current_heading and "\n".join(current_lines).strip():
                    sections.append((current_heading, current_lines))
                current_heading = match.group(2).strip()
                current_lines = []
                continue
            if current_heading:
                current_lines.append(line)

        if current_heading and "\n".join(current_lines).strip():
            sections.append((current_heading, current_lines))

        chunks: list[SourceChunk] = []
        for heading, lines in sections:
            body = "\n".join(lines).strip()
            for part in self._split_text(body):
                chunks.append(
                    SourceChunk(
                        source_id=source.id,
                        index=len(chunks),
                        heading=heading,
                        text=part,
                    )
                )
        return chunks

    def _chunk_paragraphs(self, source: Source) -> list[SourceChunk]:
        chunks = [
            SourceChunk(source_id=source.id, index=index, text=part)
            for index, part in enumerate(self._split_text(source.raw_text))
        ]
        return chunks

    def _split_text(self, text: str) -> list[str]:
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
        if not paragraphs:
            return []

        chunks: list[str] = []
        current: list[str] = []
        current_len = 0

        for paragraph in paragraphs:
            if current and current_len + len(paragraph) + 2 > self.target_chars:
                chunks.append("\n\n".join(current))
                current = []
                current_len = 0
            if len(paragraph) > self.target_chars:
                if current:
                    chunks.append("\n\n".join(current))
                    current = []
                    current_len = 0
                chunks.extend(self._split_long_paragraph(paragraph))
                continue
            current.append(paragraph)
            current_len += len(paragraph) + 2

        if current:
            chunks.append("\n\n".join(current))
        return chunks

    def _split_long_paragraph(self, paragraph: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        chunks: list[str] = []
        current: list[str] = []
        current_len = 0

        for sentence in sentences:
            if current and current_len + len(sentence) + 1 > self.target_chars:
                chunks.append(" ".join(current))
                current = []
                current_len = 0
            current.append(sentence)
            current_len += len(sentence) + 1

        if current:
            chunks.append(" ".join(current))
        return chunks
