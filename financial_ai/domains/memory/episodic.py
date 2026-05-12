"""Summarized episodic memory for daily and weekly compression."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class EpisodicSummary:
    """Compressed memory entry produced by medium/deep reasoning loops."""

    period_start: date
    period_end: date
    summary: str
    themes: tuple[str, ...] = ()
    evidence_count: int = 0


@dataclass
class EpisodicMemoryStore:
    """In-memory summary store that can be replaced with Postgres later."""

    summaries: list[EpisodicSummary] = field(default_factory=list)

    def add(self, summary: EpisodicSummary) -> None:
        self.summaries.append(summary)

    def recent(self, limit: int = 7) -> tuple[EpisodicSummary, ...]:
        return tuple(self.summaries[-limit:])
