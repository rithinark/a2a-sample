"""Insight report generation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from financial_ai.domains.models import ExtractedEvent, InsightReport, PortfolioSnapshot, Sentiment


@dataclass
class ReportGenerator:
    """Builds concise hourly and daily reports from events and portfolio state."""

    def build(self, cadence: str, events: list[ExtractedEvent], snapshot: PortfolioSnapshot | None = None) -> InsightReport:
        top_events = tuple(sorted(events, key=lambda event: (event.risk_level, event.confidence), reverse=True)[:5])
        emerging_risks = tuple(
            f"{','.join(event.entities) or 'Market'}: {event.event_type.value} risk {event.risk_level:.0%}"
            for event in top_events
            if event.risk_level >= 0.5 or event.sentiment is Sentiment.NEGATIVE
        )
        narrative = self._narrative(cadence, top_events, snapshot)
        return InsightReport(
            cadence=cadence,
            generated_at=datetime.now(timezone.utc),
            top_events=top_events,
            emerging_risks=emerging_risks,
            portfolio_snapshot=snapshot,
            narrative=narrative,
        )

    def _narrative(self, cadence: str, events: tuple[ExtractedEvent, ...], snapshot: PortfolioSnapshot | None) -> str:
        event_count = len(events)
        portfolio_text = ""
        if snapshot is not None:
            portfolio_text = f" Portfolio P/L is {snapshot.unrealized_pl_pct:.2%} with {snapshot.concentration:.2%} max position concentration."
        return f"{cadence.title()} report: {event_count} priority events identified.{portfolio_text}"
