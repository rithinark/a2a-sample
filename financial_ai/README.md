# Autonomous Financial Intelligence System

This package is a first implementation scaffold for a continuously running financial research operating system. It turns the implementation plan into concrete, testable Python modules while leaving infrastructure adapters (FastAPI, Redis, PostgreSQL, Qdrant, Neo4j, and schedulers) pluggable.

## Architecture

```text
News sources -> ingestion -> deduplication -> extraction
                                      |             |
                                      v             v
                              raw archive      graph/vector/time memory
                                      \             /
                                       reasoning loops
                                             |
                                      portfolio simulator
                                             |
                                      insight reports
```

## Implemented building blocks

- **Shared contracts** define normalized documents, extracted events, graph edges, portfolio positions, reports, and loop cadence values.
- **Ingestion pipeline** normalizes source payloads and assigns stable checksums for exact deduplication.
- **Deduplication service** combines exact checksum matching with optional semantic fingerprints.
- **Extraction interface** provides deterministic keyword extraction now and an `LLMExtractor` protocol for llama.cpp or hosted models later.
- **Graph memory** keeps an in-memory relationship graph that mirrors the future Neo4j model.
- **Portfolio engine** calculates deterministic unrealized P/L, exposure, sector concentration, and win-rate metrics.
- **Reasoning loops** model the fast, medium, and deep scheduled passes without a single giant ReAct loop.
- **Reporter** produces hourly and daily insight report objects from events, graph state, and portfolio metrics.

## Next adapters to add

1. FastAPI routes in `apps/api` for reports, health, portfolio state, and ingestion submission.
2. Redis/Celery or Dramatiq worker entrypoints in `apps/workers`.
3. PostgreSQL repositories in `infrastructure/postgres` for raw articles, positions, and reports.
4. Qdrant vector-memory implementation in `infrastructure/qdrant`.
5. Neo4j graph persistence in `infrastructure/neo4j`.
6. APScheduler jobs in `apps/scheduler` to invoke the loop cadence defined in `domains/reasoning/loops.py`.
