"""FastAPI surface for the autonomous financial intelligence system."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from financial_ai.domains.portfolio.engine import PortfolioEngine
from financial_ai.domains.reasoning.loops import ReasoningLoopRunner
from financial_ai.shared.models import PortfolioPosition, RawArticle

app = FastAPI(title="Autonomous Financial Intelligence API", version="0.1.0")
runner = ReasoningLoopRunner()
portfolio_engine = PortfolioEngine()


class ArticleIn(BaseModel):
    source: str
    title: str
    content: str
    url: str


class PositionIn(BaseModel):
    ticker: str
    entry_price: Decimal = Field(gt=0)
    quantity: Decimal
    thesis: str
    confidence: Decimal = Field(ge=0, le=1)
    sector: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(article: ArticleIn) -> dict[str, object]:
    updates = runner.fast_loop([RawArticle(**article.model_dump())])
    event = updates[0].event
    return {
        "document_id": str(event.document_id),
        "event_type": event.event_type.value,
        "sentiment": event.sentiment.value,
        "risk_level": event.risk_level,
        "entities": [entity.name for entity in event.entities],
    }


@app.get("/reports/hourly")
def hourly_report() -> dict[str, object]:
    report = runner.medium_loop()
    return {
        "title": report.title,
        "cadence": report.cadence,
        "bullets": list(report.bullets),
    }


@app.post("/portfolio/snapshot")
def portfolio_snapshot(
    position: PositionIn, current_price: Decimal
) -> dict[str, object]:
    portfolio_position = PortfolioPosition(
        **position.model_dump(),
        opened_at=datetime.now(timezone.utc),
    )
    snapshot = portfolio_engine.snapshot(
        [portfolio_position],
        {position.ticker: current_price},
    )
    return {
        "market_value": str(snapshot.market_value),
        "cost_basis": str(snapshot.cost_basis),
        "unrealized_pl": str(snapshot.unrealized_pl),
        "unrealized_pl_pct": str(snapshot.unrealized_pl_pct),
        "sector_exposure": {
            key: str(value) for key, value in snapshot.sector_exposure.items()
        },
        "position_count": snapshot.position_count,
    }
