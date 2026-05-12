"""Scheduled reasoning loop definitions for autonomous operation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from financial_ai.shared.models import LoopCadence


@dataclass(frozen=True)
class ReasoningTask:
    """A scheduled unit of work for planner/executor workers."""

    name: str
    cadence: LoopCadence
    description: str


FAST_LOOP_TASKS = (
    ReasoningTask("classify_incoming_news", LoopCadence.FAST, "Classify fresh documents and detect urgency."),
    ReasoningTask("update_graph", LoopCadence.FAST, "Apply new extracted events to graph memory."),
)
MEDIUM_LOOP_TASKS = (
    ReasoningTask("correlate_events", LoopCadence.MEDIUM, "Detect event clusters, trends, and sector sentiment shifts."),
    ReasoningTask("refresh_memory_summaries", LoopCadence.MEDIUM, "Compress recent evidence into episodic memory."),
)
DEEP_LOOP_TASKS = (
    ReasoningTask("portfolio_review", LoopCadence.DEEP, "Review portfolio exposure, thesis drift, and macro risks."),
    ReasoningTask("reflection", LoopCadence.DEEP, "Reflect on extraction quality and reasoning misses."),
)


class ReasoningLoopRegistry:
    """Register specialized workers by cadence instead of running one giant agent loop."""

    def __init__(self):
        self._handlers: dict[str, Callable[[], object]] = {}

    def register(self, task_name: str, handler: Callable[[], object]) -> None:
        self._handlers[task_name] = handler

    def tasks_for(self, cadence: LoopCadence) -> tuple[ReasoningTask, ...]:
        tasks = FAST_LOOP_TASKS + MEDIUM_LOOP_TASKS + DEEP_LOOP_TASKS
        return tuple(task for task in tasks if task.cadence is cadence)

    def run(self, cadence: LoopCadence) -> dict[str, object]:
        results: dict[str, object] = {}
        for task in self.tasks_for(cadence):
            handler = self._handlers.get(task.name)
            if handler is not None:
                results[task.name] = handler()
        return results
