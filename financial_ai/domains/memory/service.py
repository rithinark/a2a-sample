"""Multi-layer memory primitives for financial intelligence."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from financial_ai.shared.models import ExtractedEvent, NormalizedDocument


@dataclass
class EpisodicMemory:
    """Stores compressed daily and weekly summaries."""

    summaries: dict[date, list[str]] = field(default_factory=dict)

    def append_daily(self, day: date, summary: str) -> None:
        self.summaries.setdefault(day, []).append(summary)

    def latest(self, limit: int = 5) -> list[str]:
        items: list[str] = []
        for day in sorted(self.summaries, reverse=True):
            items.extend(self.summaries[day])
            if len(items) >= limit:
                return items[:limit]
        return items


@dataclass
class MemoryUpdate:
    """Bundle of data persisted after each reasoning loop."""

    document: NormalizedDocument
    event: ExtractedEvent
    summary: str
