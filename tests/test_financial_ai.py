from datetime import datetime, timezone
from decimal import Decimal

from financial_ai.domains.dedup.service import DeduplicationService
from financial_ai.domains.ingestion.service import IngestionService
from financial_ai.domains.portfolio.engine import PortfolioEngine
from financial_ai.domains.reasoning.loops import ReasoningLoopRunner
from financial_ai.shared.models import PortfolioPosition, RawArticle, Sentiment


def test_ingestion_normalizes_and_checksums_content():
    article = RawArticle(
        source=" CNBC ",
        title="  NVDA   beats ",
        content="Record   revenue",
        url=" https://example.com/a ",
    )
    document = IngestionService().normalize(article)

    assert document.source == "cnbc"
    assert document.title == "NVDA beats"
    assert len(document.checksum) == 64


def test_dedup_detects_exact_checksum_after_remembering():
    service = IngestionService()
    document = service.normalize(
        RawArticle(source="x", title="A", content="Same", url="u")
    )
    dedup = DeduplicationService()

    assert not dedup.check(document).is_duplicate
    dedup.remember(document)
    assert dedup.check(document).reason == "exact_checksum"


def test_fast_loop_extracts_event_and_updates_memory():
    runner = ReasoningLoopRunner()
    article = RawArticle(
        source="reuters",
        title="NVDA beats earnings",
        content="NVDA reports record revenue growth",
        url="https://example.com/nvda",
    )

    updates = runner.fast_loop([article])

    assert updates[0].event.sentiment == Sentiment.POSITIVE
    assert updates[0].event.entities[0].ticker == "NVDA"
    assert runner.medium_loop().bullets


def test_portfolio_snapshot_is_deterministic():
    position = PortfolioPosition(
        ticker="NVDA",
        entry_price=Decimal("100"),
        quantity=Decimal("2"),
        thesis="AI demand",
        confidence=Decimal("0.8"),
        opened_at=datetime.now(timezone.utc),
        sector="semiconductors",
    )

    snapshot = PortfolioEngine().snapshot([position], {"NVDA": Decimal("125")})

    assert snapshot.cost_basis == Decimal("200")
    assert snapshot.market_value == Decimal("250")
    assert snapshot.unrealized_pl == Decimal("50")
    assert snapshot.sector_exposure["semiconductors"] == Decimal("250")
