from recall.app.domain.question import Question
from recall.app.services.scoring import ScoringService


def test_scores_correct_and_unanswered_questions() -> None:
    questions = [
        Question(
            source_id="source",
            chunk_id="chunk-a",
            prompt="A?",
            choices=("a", "b", "c", "d"),
            correct_choice_index=1,
            explanation="Because b.",
            source_excerpt="source",
            id="q1",
        ),
        Question(
            source_id="source",
            chunk_id="chunk-b",
            prompt="B?",
            choices=("a", "b", "c", "d"),
            correct_choice_index=2,
            explanation="Because c.",
            source_excerpt="source",
            id="q2",
        ),
    ]

    score, answers = ScoringService().score(questions, {"q1": 1, "q2": None})

    assert score.correct == 1
    assert score.total == 2
    assert score.percent == 50
    assert answers[0].is_correct is True
    assert answers[1].is_correct is False
