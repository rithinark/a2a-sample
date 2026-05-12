"""Deterministic mock portfolio simulator."""

from __future__ import annotations

from financial_ai.shared.models import PortfolioSnapshot, Position


class PortfolioEngine:
    """Maintain positions and calculate portfolio metrics without LLM logic."""

    def __init__(self):
        self._positions: dict[str, Position] = {}
        self._closed_results: list[float] = []

    def open_position(self, position: Position) -> None:
        self._positions[position.ticker.upper()] = position

    def close_position(self, ticker: str, exit_price: float) -> float:
        position = self._positions.pop(ticker.upper())
        result = (exit_price - position.entry_price) * position.quantity
        self._closed_results.append(result)
        return result

    def positions(self) -> tuple[Position, ...]:
        return tuple(self._positions.values())

    def snapshot(self, market_prices: dict[str, float]) -> PortfolioSnapshot:
        market_value = 0.0
        unrealized_pl = 0.0
        exposure_by_sector: dict[str, float] = {}

        for ticker, position in self._positions.items():
            current_price = market_prices.get(ticker, position.entry_price)
            value = current_price * position.quantity
            market_value += value
            unrealized_pl += (current_price - position.entry_price) * position.quantity
            exposure_by_sector[position.sector] = exposure_by_sector.get(position.sector, 0.0) + value

        wins = sum(result > 0 for result in self._closed_results)
        win_rate = wins / len(self._closed_results) if self._closed_results else 0.0
        return PortfolioSnapshot(
            market_value=market_value,
            unrealized_pl=unrealized_pl,
            exposure_by_sector=exposure_by_sector,
            win_rate=win_rate,
            position_count=len(self._positions),
        )
