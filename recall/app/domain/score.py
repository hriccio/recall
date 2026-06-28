from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    correct: int
    total: int

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0.0
        return self.correct / self.total * 100
