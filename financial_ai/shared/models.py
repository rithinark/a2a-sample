"""Core domain models for the financial intelligence system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class EventType(str, Enum):
    """Financial event categories tracked by the system."""

    EARNINGS = "earnings"
    MACRO = "macro"
    M_AND_A = "m_and_a"
    PRODUCT = "product"
    REGULATORY = "regulatory"
    SUPPLY_CHAIN = "supply_chain"
    MARKET_MOVE = "market_move"
    MANAGEMENT = "management"
    UNKNOWN = "unknown"


class Sentiment(str, Enum):
    """Coarse event sentiment for deterministic downstream logic."""

    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass(frozen=True)
class RawArticle:
    """Immutable raw article record captured before enrichment."""

    source: str
    title: str
    content: str
    url: str
    published_at: datetime | None = None
    id: UUID = field(default_factory=uuid4)
    checksum: str | None = None
    ingested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class NormalizedDocument:
    """Article after cleaning, canonicalization, and exact checksum generation."""

    raw_article_id: UUID
    source: str
    title: str
    content: str
    url: str
    checksum: str
    published_at: datetime | None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Entity:
    """Entity mentioned in extracted financial knowledge."""

    name: str
    kind: str
    ticker: str | None = None


@dataclass(frozen=True)
class Relationship:
    """Directed relationship between two entities or events."""

    source: str
    relation: str
    target: str
    confidence: float = 0.0


@dataclass(frozen=True)
class ExtractedEvent:
    """Structured event extracted from a normalized financial document."""

    document_id: UUID
    event_type: EventType
    entities: tuple[Entity, ...]
    sentiment: Sentiment
    risk_level: int
    catalysts: tuple[str, ...] = ()
    relationships: tuple[Relationship, ...] = ()
    confidence: float = 0.0
    extracted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class PortfolioPosition:
    """Deterministic portfolio position used by the simulator."""

    ticker: str
    entry_price: Decimal
    quantity: Decimal
    thesis: str
    confidence: Decimal
    opened_at: datetime
    sector: str | None = None
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class PortfolioSnapshot:
    """Point-in-time portfolio analytics output."""

    market_value: Decimal
    cost_basis: Decimal
    unrealized_pl: Decimal
    unrealized_pl_pct: Decimal
    sector_exposure: dict[str, Decimal]
    position_count: int


@dataclass(frozen=True)
class InsightReport:
    """Generated report from a scheduled reasoning loop."""

    cadence: str
    title: str
    bullets: tuple[str, ...]
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
