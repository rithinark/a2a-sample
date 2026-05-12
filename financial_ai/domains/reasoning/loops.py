"""Scheduled reasoning loops for autonomous financial research."""

from __future__ import annotations

from datetime import datetime, timezone

from financial_ai.domains.extraction.service import EventExtractionService
from financial_ai.domains.graph.service import KnowledgeGraph
from financial_ai.domains.ingestion.service import IngestionService
from financial_ai.domains.memory.service import EpisodicMemory, MemoryUpdate
from financial_ai.shared.models import InsightReport, RawArticle


class ReasoningLoopRunner:
    """Coordinates fast, medium, and deep loops over incremental data."""

    def __init__(
        self,
        ingestion: IngestionService | None = None,
        extractor: EventExtractionService | None = None,
        graph: KnowledgeGraph | None = None,
        memory: EpisodicMemory | None = None,
    ):
        self.ingestion = ingestion or IngestionService()
        self.extractor = extractor or EventExtractionService()
        self.graph = graph or KnowledgeGraph()
        self.memory = memory or EpisodicMemory()

    def fast_loop(self, articles: list[RawArticle]) -> list[MemoryUpdate]:
        updates: list[MemoryUpdate] = []
        for article in articles:
            document = self.ingestion.normalize(article)
            event = self.extractor.extract(document)
            self.graph.apply_event(event)
            summary = f"{event.event_type.value}: {document.title}"
            self.memory.append_daily(datetime.now(timezone.utc).date(), summary)
            updates.append(
                MemoryUpdate(document=document, event=event, summary=summary)
            )
        return updates

    def medium_loop(self) -> InsightReport:
        bullets = tuple(self.memory.latest(limit=10)) or (
            "No new financial events detected.",
        )
        return InsightReport(
            cadence="hourly",
            title="Hourly Market Intelligence",
            bullets=bullets,
        )

    def deep_loop(self) -> InsightReport:
        bullets = tuple(self.memory.latest(limit=20)) or (
            "No thesis updates available.",
        )
        return InsightReport(
            cadence="daily",
            title="Daily Portfolio and Macro Review",
            bullets=bullets,
        )
"""Scheduled reasoning loops for autonomous financial intelligence."""

from __future__ import annotations

from dataclasses import dataclass

from financial_ai.domains.extraction.extractor import EventExtractor
from financial_ai.domains.graph.store import KnowledgeGraph
from financial_ai.domains.models import ExtractedEvent, NormalizedDocument, PortfolioSnapshot
from financial_ai.domains.portfolio.engine import PortfolioEngine


@dataclass
class ReasoningLoops:
    """Fast, medium, and deep loop orchestration boundaries."""

    extractor: EventExtractor
    graph: KnowledgeGraph
    portfolio: PortfolioEngine

    def fast_loop(self, documents: list[NormalizedDocument]) -> list[ExtractedEvent]:
        events = [self.extractor.extract(document) for document in documents if document.duplicate_of is None]
        for event in events:
            self.graph.apply_event(event)
        return events

    def medium_loop(self, events: list[ExtractedEvent]) -> dict[str, int]:
        sector_or_entity_counts: dict[str, int] = {}
        for event in events:
            for entity in event.entities:
                sector_or_entity_counts[entity] = sector_or_entity_counts.get(entity, 0) + 1
        return sector_or_entity_counts

    def deep_loop(self, prices: dict[str, float]) -> PortfolioSnapshot:
        return self.portfolio.snapshot(prices)
