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
