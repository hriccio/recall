from __future__ import annotations

from recall.app.domain.question import Question
from recall.app.domain.source import SourceChunk
from recall.app.services.question_generator import QuestionGenerator


class OpenAIQuestionGenerator(QuestionGenerator):
    def generate_questions(self, chunks: list[SourceChunk], count: int) -> list[Question]:
        raise NotImplementedError("OpenAI integration is planned after the fake provider flow is stable.")
