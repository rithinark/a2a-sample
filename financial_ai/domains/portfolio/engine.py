"""Deterministic mock portfolio simulator."""

from __future__ import annotations

from decimal import Decimal

from financial_ai.shared.models import PortfolioPosition, PortfolioSnapshot


class PortfolioEngine:
    """Computes portfolio metrics without using LLM judgement."""

    def snapshot(
        self, positions: list[PortfolioPosition], prices: dict[str, Decimal]
    ) -> PortfolioSnapshot:
        cost_basis = Decimal("0")
        market_value = Decimal("0")
        sector_exposure: dict[str, Decimal] = {}

        for position in positions:
            cost = position.entry_price * position.quantity
            current_price = prices.get(position.ticker, position.entry_price)
            value = current_price * position.quantity
            sector = position.sector or "unknown"
            cost_basis += cost
            market_value += value
            sector_exposure[sector] = sector_exposure.get(sector, Decimal("0")) + value

        unrealized = market_value - cost_basis
        pct = Decimal("0") if cost_basis == 0 else unrealized / cost_basis
        return PortfolioSnapshot(
            market_value=market_value,
            cost_basis=cost_basis,
            unrealized_pl=unrealized,
            unrealized_pl_pct=pct,
            sector_exposure=sector_exposure,
            position_count=len(positions),
        )
