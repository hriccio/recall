from __future__ import annotations

from recall.app.domain.attempt import Answer
from recall.app.domain.question import Question
from recall.app.domain.score import Score


class ScoringService:
    def score(self, questions: list[Question], selections: dict[str, int | None]) -> tuple[Score, tuple[Answer, ...]]:
        answers: list[Answer] = []
        correct = 0

        for question in questions:
            selected = selections.get(question.id)
            is_correct = selected == question.correct_choice_index
            if is_correct:
                correct += 1
            answers.append(
                Answer(
                    question_id=question.id,
                    selected_choice_index=selected,
                    is_correct=is_correct,
                )
            )

        return Score(correct=correct, total=len(questions)), tuple(answers)
