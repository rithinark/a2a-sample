# Autonomous Financial Intelligence System

This package is the implementation scaffold for a continuously running financial research operating system. It separates ingestion, deduplication, extraction, graph memory, episodic memory, deterministic portfolio simulation, and scheduled reasoning loops.

## Runtime layers

- **Fast loop:** normalize incoming articles, extract structured events, update graph and episodic memory.
- **Medium loop:** produce hourly market intelligence from incremental memory.
- **Deep loop:** produce daily portfolio and macro review summaries.

## Persistence targets

- PostgreSQL stores raw archive and portfolio tables.
- Qdrant is reserved for semantic duplicate detection and vector retrieval.
- Neo4j is represented by the graph facade and can be backed by a driver later.
- Redis/Celery or Dramatiq can feed `ReasoningLoopRunner.fast_loop` with raw article batches.
