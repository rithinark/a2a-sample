"""Structured event extraction layer.

The production implementation can replace this deterministic extractor with a
llama.cpp-backed model while preserving the same output contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from financial_ai.domains.models import EventType, ExtractedEvent, NormalizedDocument, Relationship, Sentiment


POSITIVE_TERMS = {"beats", "growth", "surge", "record", "upgrade", "benefits", "accelerated"}
NEGATIVE_TERMS = {"miss", "risk", "falls", "lawsuit", "downgrade", "shortage", "spike", "disruption"}
EVENT_KEYWORDS = {
    EventType.EARNINGS: {"earnings", "revenue", "eps", "guidance"},
    EventType.MACRO: {"inflation", "fed", "rates", "jobs", "gdp", "oil"},
    EventType.REGULATORY: {"sec", "regulator", "lawsuit", "probe", "antitrust"},
    EventType.M_AND_A: {"acquire", "merger", "takeover", "deal"},
    EventType.PRODUCT: {"launch", "product", "chip", "model"},
    EventType.SUPPLY_CHAIN: {"supply", "supplier", "shortage", "tsmc", "shipping"},
}


@dataclass
class EventExtractor:
    """Deterministic baseline extractor for entities, events, and relationships."""

    watchlist: tuple[str, ...] = ("NVDA", "AMD", "AAPL", "MSFT", "TSLA", "TSMC", "XOM", "DAL", "UAL")

    def extract(self, document: NormalizedDocument) -> ExtractedEvent:
        text = f"{document.title} {document.content}"
        lowered = text.casefold()
        entities = tuple(symbol for symbol in self.watchlist if symbol.casefold() in lowered)
        event_type = self._event_type(lowered)
        sentiment = self._sentiment(lowered)
        relationships = tuple(
            Relationship(
                subject=entity,
                predicate="MENTIONS",
                object=document.title,
                confidence=0.7,
                source_document_id=document.raw_article_id,
            )
            for entity in entities
        )
        risk_level = min(1.0, sum(1 for term in NEGATIVE_TERMS if term in lowered) / 3)
        confidence = 0.45 + (0.2 if entities else 0.0) + (0.2 if event_type is not EventType.UNKNOWN else 0.0)
        return ExtractedEvent(
            document_id=document.raw_article_id,
            event_type=event_type,
            entities=entities,
            sentiment=sentiment,
            risk_level=risk_level,
            catalysts=tuple(term for term in EVENT_KEYWORDS.get(event_type, set()) if term in lowered),
            relationships=relationships,
            confidence=min(confidence, 0.95),
            occurred_at=document.published_at,
        )

    def _event_type(self, lowered_text: str) -> EventType:
        for event_type, keywords in EVENT_KEYWORDS.items():
            if any(keyword in lowered_text for keyword in keywords):
                return event_type
        return EventType.UNKNOWN

    def _sentiment(self, lowered_text: str) -> Sentiment:
        positive = sum(term in lowered_text for term in POSITIVE_TERMS)
        negative = sum(term in lowered_text for term in NEGATIVE_TERMS)
        if positive > negative:
            return Sentiment.POSITIVE
        if negative > positive:
            return Sentiment.NEGATIVE
        return Sentiment.NEUTRAL
