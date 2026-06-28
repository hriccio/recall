from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class Question:
    source_id: str
    chunk_id: str
    prompt: str
    choices: tuple[str, str, str, str]
    correct_choice_index: int
    explanation: str
    source_excerpt: str
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if len(self.choices) != 4:
            raise ValueError("Multiple-choice questions must have exactly four choices.")
        if not 0 <= self.correct_choice_index < 4:
            raise ValueError("Correct choice index must be between 0 and 3.")
        if not self.prompt.strip():
            raise ValueError("Question prompt cannot be empty.")
