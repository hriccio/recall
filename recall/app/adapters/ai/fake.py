from __future__ import annotations

import re

from recall.app.domain.question import Question
from recall.app.domain.source import SourceChunk
from recall.app.services.question_generator import QuestionGenerator


class FakeQuestionGenerator(QuestionGenerator):
    """Deterministic offline generator for development and tests."""

    def generate_questions(self, chunks: list[SourceChunk], count: int) -> list[Question]:
        usable_chunks = [chunk for chunk in chunks if len(chunk.text.split()) >= 8]
        if not usable_chunks or count <= 0:
            return []

        questions: list[Question] = []
        for index in range(count):
            chunk = usable_chunks[index % len(usable_chunks)]
            excerpt = self._excerpt(chunk.text)
            correct = self._answer_statement(excerpt)
            choices = self._choices(correct, usable_chunks, index)
            correct_index = index % 4
            ordered = list(choices)
            ordered[correct_index], ordered[0] = ordered[0], ordered[correct_index]

            heading = chunk.heading or f"section {chunk.index + 1}"
            questions.append(
                Question(
                    source_id=chunk.source_id,
                    chunk_id=chunk.id,
                    prompt=f"According to {heading}, which statement is best supported by the source?",
                    choices=(ordered[0], ordered[1], ordered[2], ordered[3]),
                    correct_choice_index=correct_index,
                    explanation="The correct answer restates information found in the source excerpt.",
                    source_excerpt=excerpt,
                )
            )
        return questions

    def _excerpt(self, text: str) -> str:
        compact = re.sub(r"\s+", " ", text).strip()
        sentences = re.split(r"(?<=[.!?])\s+", compact)
        for sentence in sentences:
            if 40 <= len(sentence) <= 220:
                return sentence
        return compact[:220].rstrip()

    def _answer_statement(self, excerpt: str) -> str:
        return excerpt.rstrip(".") + "."

    def _choices(self, correct: str, chunks: list[SourceChunk], index: int) -> tuple[str, str, str, str]:
        distractors: list[str] = []
        for offset in range(1, len(chunks) + 1):
            other = chunks[(index + offset) % len(chunks)]
            candidate = self._answer_statement(self._excerpt(other.text))
            if candidate != correct and candidate not in distractors:
                distractors.append(candidate)
            if len(distractors) == 3:
                break

        generic = [
            "The source says this topic requires a remote service account.",
            "The source says the main goal is public sharing and collaboration.",
            "The source says this material should be ignored during review.",
        ]
        for candidate in generic:
            if len(distractors) == 3:
                break
            if candidate != correct and candidate not in distractors:
                distractors.append(candidate)

        return (correct, distractors[0], distractors[1], distractors[2])
