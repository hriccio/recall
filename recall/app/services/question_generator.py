from __future__ import annotations

from abc import ABC, abstractmethod

from recall.app.domain.question import Question
from recall.app.domain.source import SourceChunk


class QuestionGenerator(ABC):
    @abstractmethod
    def generate_questions(self, chunks: list[SourceChunk], count: int) -> list[Question]:
        raise NotImplementedError
