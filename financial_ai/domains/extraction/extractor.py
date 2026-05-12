"""Event extraction interfaces and deterministic fallback extractor."""

from __future__ import annotations

import re
from typing import Protocol

from financial_ai.shared.models import EventType, ExtractedEvent, NormalizedDocument, RiskLevel, Sentiment

_COMPANY_RE = re.compile(r"\b[A-Z][A-Za-z&.]{2,}(?:\s+[A-Z][A-Za-z&.]{2,})?\b")
_NEGATIVE_TERMS = {"risk", "lawsuit", "decline", "miss", "cut", "spike", "disruption", "probe"}
_POSITIVE_TERMS = {"beat", "growth", "record", "approval", "upgrade", "profit", "demand"}
_EVENT_KEYWORDS: tuple[tuple[EventType, tuple[str, ...]], ...] = (
    (EventType.EARNINGS, ("earnings", "revenue", "guidance", "eps")),
    (EventType.MACRO, ("inflation", "fed", "rates", "jobs", "gdp")),
    (EventType.REGULATORY, ("sec", "regulator", "lawsuit", "probe")),
    (EventType.MERGER, ("acquire", "merger", "takeover")),
    (EventType.PRODUCT, ("launch", "product", "approval")),
    (EventType.SUPPLY_CHAIN, ("supply", "shipment", "supplier", "shortage")),
)


class LLMExtractor(Protocol):
    """Protocol for llama.cpp, hosted LLM, or LangGraph-backed extractors."""

    async def extract(self, document: NormalizedDocument) -> ExtractedEvent:
        """Extract a structured event from a normalized document."""


class KeywordEventExtractor:
    """Deterministic extraction fallback for tests and offline development."""

    def extract(self, document: NormalizedDocument) -> ExtractedEvent:
        text = f"{document.title} {document.content}"
        lowered = text.lower()
        event_type = next(
            (
                event_type
                for event_type, keywords in _EVENT_KEYWORDS
                if any(keyword in lowered for keyword in keywords)
            ),
            EventType.OTHER,
        )
        sentiment = self._sentiment(lowered)
        risk_level = self._risk_level(lowered, sentiment)
        entities = tuple(dict.fromkeys(_COMPANY_RE.findall(text)))[:10]
        catalysts = tuple(
            keyword
            for _, keywords in _EVENT_KEYWORDS
            for keyword in keywords
            if keyword in lowered
        )[:8]
        return ExtractedEvent(
            document_id=document.article_id,
            event_type=event_type,
            entities=entities,
            sentiment=sentiment,
            risk_level=risk_level,
            catalysts=catalysts,
            macro_impact="requires_human_review" if event_type is EventType.MACRO else None,
            confidence=0.55 if event_type is EventType.OTHER else 0.72,
        )

    def _sentiment(self, lowered_text: str) -> Sentiment:
        positive = sum(term in lowered_text for term in _POSITIVE_TERMS)
        negative = sum(term in lowered_text for term in _NEGATIVE_TERMS)
        if positive > negative:
            return Sentiment.POSITIVE
        if negative > positive:
            return Sentiment.NEGATIVE
        return Sentiment.NEUTRAL

    def _risk_level(self, lowered_text: str, sentiment: Sentiment) -> RiskLevel:
        if sentiment is Sentiment.NEGATIVE and any(term in lowered_text for term in ("lawsuit", "probe", "disruption")):
            return RiskLevel.HIGH
        if sentiment is Sentiment.NEGATIVE:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
