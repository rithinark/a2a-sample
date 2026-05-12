"""Deterministic mock portfolio simulator and analytics engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from financial_ai.domains.models import PortfolioSnapshot, Position


@dataclass
class PortfolioEngine:
    """Tracks positions and computes risk/performance without LLM logic."""

    positions: dict[str, Position] = field(default_factory=dict)

    def open_position(self, position: Position) -> None:
        self.positions[position.ticker] = position

    def close_position(self, ticker: str) -> Position:
        return self.positions.pop(ticker)

    def snapshot(self, prices: dict[str, float], as_of: datetime | None = None) -> PortfolioSnapshot:
        as_of = as_of or datetime.now(timezone.utc)
        position_values = {
            ticker: prices.get(ticker, position.entry_price) * position.quantity
            for ticker, position in self.positions.items()
        }
        market_value = sum(position_values.values())
        cost_basis = sum(position.cost_basis for position in self.positions.values())
        unrealized_pl = market_value - cost_basis
        unrealized_pl_pct = unrealized_pl / cost_basis if cost_basis else 0.0
        sector_exposure: dict[str, float] = {}
        for ticker, value in position_values.items():
            sector = self.positions[ticker].sector
            sector_exposure[sector] = sector_exposure.get(sector, 0.0) + value
        if market_value:
            sector_exposure = {sector: value / market_value for sector, value in sector_exposure.items()}
        concentration = max((value / market_value for value in position_values.values()), default=0.0) if market_value else 0.0
        return PortfolioSnapshot(
            as_of=as_of,
            market_value=market_value,
            cost_basis=cost_basis,
            unrealized_pl=unrealized_pl,
            unrealized_pl_pct=unrealized_pl_pct,
            sector_exposure=sector_exposure,
            position_values=position_values,
            concentration=concentration,
        )
