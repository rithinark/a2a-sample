"""Insight report generation helpers."""

from __future__ import annotations

from financial_ai.shared.models import ExtractedEvent, InsightReport, LoopCadence, PortfolioSnapshot, RiskLevel, Sentiment


class InsightReporter:
    """Generate hourly and daily reports from structured state."""

    def hourly(self, events: list[ExtractedEvent]) -> InsightReport:
        highlights = tuple(self._event_highlight(event) for event in events[:10])
        risks = tuple(self._event_highlight(event) for event in events if event.risk_level is RiskLevel.HIGH)
        return InsightReport(
            cadence=LoopCadence.MEDIUM,
            title="Hourly Market Intelligence Brief",
            highlights=highlights,
            risks=risks,
        )

    def daily(self, events: list[ExtractedEvent], snapshot: PortfolioSnapshot) -> InsightReport:
        positive_count = sum(event.sentiment is Sentiment.POSITIVE for event in events)
        negative_count = sum(event.sentiment is Sentiment.NEGATIVE for event in events)
        highlights = (
            f"Processed {len(events)} extracted events.",
            f"Sentiment balance: {positive_count} positive / {negative_count} negative.",
            f"Portfolio unrealized P/L: {snapshot.unrealized_pl:.2f}.",
        )
        risks = tuple(self._event_highlight(event) for event in events if event.risk_level is not RiskLevel.LOW)
        return InsightReport(
            cadence=LoopCadence.DEEP,
            title="Daily Portfolio and Macro Review",
            highlights=highlights,
            risks=risks,
            portfolio_snapshot=snapshot,
        )

    def _event_highlight(self, event: ExtractedEvent) -> str:
        entities = ", ".join(event.entities) if event.entities else "Unknown entities"
        return f"{event.event_type.value}: {entities} ({event.sentiment.value}, risk={event.risk_level.value})"
