"""Structured financial event extraction."""

from __future__ import annotations

import re

from financial_ai.shared.models import (
    Entity,
    EventType,
    ExtractedEvent,
    NormalizedDocument,
    Relationship,
    Sentiment,
)

EXTRACTION_PROMPT = """
Extract companies, sectors, event type, sentiment, risk level, catalysts,
affected entities, macroeconomic impact, relationships, and confidence.
Return JSON with entities, events, sentiment, relationships, and confidence.
""".strip()

_TICKER_PATTERN = re.compile(r"\b[A-Z]{1,5}\b")
_NEGATIVE_TERMS = {
    "miss",
    "falls",
    "lawsuit",
    "probe",
    "cut",
    "risk",
    "decline",
    "warning",
}
_POSITIVE_TERMS = {
    "beats",
    "surges",
    "raises",
    "growth",
    "approval",
    "record",
    "profit",
}


class EventExtractionService:
    """LLM-ready extraction service with a deterministic fallback classifier."""

    def extract(self, document: NormalizedDocument) -> ExtractedEvent:
        text = f"{document.title} {document.content}"
        lowered = text.lower()
        tickers = sorted(set(_TICKER_PATTERN.findall(text)))[:12]
        entities = tuple(
            Entity(name=ticker, kind="company", ticker=ticker) for ticker in tickers
        )
        sentiment = self._sentiment(lowered)
        event_type = self._event_type(lowered)
        risk_level = self._risk_level(sentiment, lowered)
        catalysts = tuple(
            term
            for term in sorted(_POSITIVE_TERMS | _NEGATIVE_TERMS)
            if term in lowered
        )
        relationships = tuple(
            Relationship(
                source=entity.name,
                relation="MENTIONS",
                target=str(document.raw_article_id),
                confidence=0.7,
            )
            for entity in entities
        )
        return ExtractedEvent(
            document_id=document.raw_article_id,
            event_type=event_type,
            entities=entities,
            sentiment=sentiment,
            risk_level=risk_level,
            catalysts=catalysts,
            relationships=relationships,
            confidence=0.65 if entities else 0.45,
        )

    @staticmethod
    def _sentiment(text: str) -> Sentiment:
        positive = sum(term in text for term in _POSITIVE_TERMS)
        negative = sum(term in text for term in _NEGATIVE_TERMS)
        if positive > negative:
            return Sentiment.POSITIVE
        if negative > positive:
            return Sentiment.NEGATIVE
        return Sentiment.NEUTRAL

    @staticmethod
    def _event_type(text: str) -> EventType:
        if "earnings" in text or "revenue" in text:
            return EventType.EARNINGS
        if "fed" in text or "inflation" in text or "jobs" in text:
            return EventType.MACRO
        if "merger" in text or "acquisition" in text:
            return EventType.M_AND_A
        if "supply" in text or "shipment" in text:
            return EventType.SUPPLY_CHAIN
        if "regulator" in text or "sec" in text:
            return EventType.REGULATORY
        return EventType.UNKNOWN

    @staticmethod
    def _risk_level(sentiment: Sentiment, text: str) -> int:
        base = 3 if sentiment == Sentiment.NEGATIVE else 2
        if "bankruptcy" in text or "investigation" in text or "crash" in text:
            return 5
        return base
