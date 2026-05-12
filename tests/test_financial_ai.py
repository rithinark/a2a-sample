from datetime import datetime, timezone
import unittest

from financial_ai.domains.dedup.service import DeduplicationService
from financial_ai.domains.extraction.extractor import EventExtractor
from financial_ai.domains.ingestion.pipeline import IngestionPipeline, StaticNewsSource
from financial_ai.domains.models import EventType, Position, RawArticle, Sentiment
from financial_ai.domains.portfolio.engine import PortfolioEngine
from financial_ai.domains.reasoning.loops import ReasoningLoops
from financial_ai.domains.graph.store import KnowledgeGraph


class FinancialAITest(unittest.TestCase):
    def test_ingestion_dedup_extraction_and_graph_loop(self):
        article = RawArticle(
            source="demo",
            title="NVDA earnings beats as AI demand accelerated",
            content="NVDA reported earnings growth and benefits from AI infrastructure spending.",
            url="https://example.com/nvda",
            published_at=datetime(2026, 5, 12, tzinfo=timezone.utc),
        )
        pipeline = IngestionPipeline([StaticNewsSource(name="demo", articles=[article])])
        documents = pipeline.collect()

        dedup = DeduplicationService()
        unique = dedup.classify(documents[0], [1.0, 0.0, 0.0])
        duplicate = dedup.classify(documents[0], [1.0, 0.0, 0.0])

        self.assertIsNone(unique.duplicate_of)
        self.assertEqual(duplicate.duplicate_of, article.id)

        graph = KnowledgeGraph()
        loops = ReasoningLoops(EventExtractor(), graph, PortfolioEngine())
        events = loops.fast_loop([unique])

        self.assertEqual(events[0].event_type, EventType.EARNINGS)
        self.assertEqual(events[0].sentiment, Sentiment.POSITIVE)
        self.assertIn("NVDA", graph.adjacency)

    def test_portfolio_snapshot_is_deterministic(self):
        engine = PortfolioEngine()
        engine.open_position(
            Position(
                ticker="NVDA",
                entry_price=100.0,
                quantity=2,
                thesis="AI infrastructure demand",
                confidence=0.8,
                sector="technology",
            )
        )

        snapshot = engine.snapshot({"NVDA": 125.0})

        self.assertEqual(snapshot.market_value, 250.0)
        self.assertEqual(snapshot.cost_basis, 200.0)
        self.assertEqual(snapshot.unrealized_pl, 50.0)
        self.assertAlmostEqual(snapshot.unrealized_pl_pct, 0.25)
        self.assertEqual(snapshot.sector_exposure["technology"], 1.0)


if __name__ == "__main__":
    unittest.main()
