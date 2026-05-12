from financial_ai.agents.reporting.reporter import InsightReporter
from financial_ai.domains.dedup.service import DeduplicationService
from financial_ai.domains.extraction.extractor import KeywordEventExtractor
from financial_ai.domains.graph.memory import RelationshipGraph
from financial_ai.domains.ingestion.pipeline import NewsIngestionPipeline
from financial_ai.domains.portfolio.engine import PortfolioEngine
from financial_ai.shared.models import Position, RelationshipType, Sentiment


def _sample_document():
    pipeline = NewsIngestionPipeline()
    return pipeline.ingest_batch(
        [
            {
                "source": "demo",
                "title": "NVIDIA reports record AI demand",
                "content": "NVIDIA revenue beat expectations as AI infrastructure demand grows.",
                "url": "https://example.test/nvidia-ai-demand",
            }
        ]
    )[0]


def test_ingestion_and_deduplication_detect_exact_duplicates():
    document = _sample_document()
    dedup = DeduplicationService()

    first_decision = dedup.evaluate(document)
    second_decision = dedup.evaluate(document)

    assert first_decision.is_duplicate is False
    assert first_decision.reason == "new_document"
    assert second_decision.is_duplicate is True
    assert second_decision.reason == "exact_checksum"


def test_extraction_updates_graph_relationships():
    document = _sample_document()
    event = KeywordEventExtractor().extract(document)
    graph = RelationshipGraph()

    relationships = graph.apply_event(event)

    assert event.sentiment is Sentiment.POSITIVE
    assert relationships
    assert any(edge.relationship is RelationshipType.BENEFITS_FROM for edge in relationships)
    assert graph.evidence_for_document(document.article_id)


def test_portfolio_snapshot_and_daily_report_are_deterministic():
    engine = PortfolioEngine()
    engine.open_position(
        Position(
            ticker="NVDA",
            entry_price=100.0,
            quantity=2.0,
            thesis="AI infrastructure demand remains durable.",
            confidence=0.7,
            sector="semiconductors",
        )
    )
    snapshot = engine.snapshot({"NVDA": 125.0})
    event = KeywordEventExtractor().extract(_sample_document())

    report = InsightReporter().daily([event], snapshot)

    assert snapshot.market_value == 250.0
    assert snapshot.unrealized_pl == 50.0
    assert snapshot.exposure_by_sector == {"semiconductors": 250.0}
    assert report.portfolio_snapshot == snapshot
    assert "Portfolio unrealized P/L: 50.00." in report.highlights
