"""Scheduler job definitions and default cadences."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class ScheduledJob:
    """Declarative APScheduler-compatible job metadata."""

    name: str
    interval: timedelta
    description: str


DEFAULT_JOBS = (
    ScheduledJob("ingest_news", timedelta(minutes=1), "Poll RSS/API/SEC/social sources into the raw document queue."),
    ScheduledJob("fast_reasoning", timedelta(minutes=5), "Classify new documents, detect urgency, and update graph memory."),
    ScheduledJob("medium_reasoning", timedelta(hours=1), "Correlate events, detect trends, and update sector/entity shifts."),
    ScheduledJob("deep_reasoning", timedelta(days=1), "Review portfolio, macro context, theses, and reflection summaries."),
)
