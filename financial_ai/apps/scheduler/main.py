"""Scheduler entrypoint documenting autonomous loop cadence."""

from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from financial_ai.domains.reasoning.loops import ReasoningLoopRunner


def build_scheduler(runner: ReasoningLoopRunner | None = None) -> BackgroundScheduler:
    runner = runner or ReasoningLoopRunner()
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        lambda: runner.medium_loop(), "interval", hours=1, id="medium_reasoning_loop"
    )
    scheduler.add_job(
        lambda: runner.deep_loop(), "cron", hour=22, minute=0, id="deep_reasoning_loop"
    )
    return scheduler
