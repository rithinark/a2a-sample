# Autonomous Financial Intelligence System

This package implements the first runnable foundation for a continuously running financial research operating system. It is intentionally split into domain modules so production adapters can be added without changing the core contracts.

## Implemented foundation

- **Ingestion**: source adapter protocol, static replay source, and document normalization.
- **Deduplication**: exact SHA-256 checksum detection and optional semantic vector detection with cosine similarity.
- **Extraction**: deterministic baseline extractor that emits the same structured event contract expected from a future llama.cpp-backed extraction model.
- **Graph memory**: in-memory graph store mirroring the Neo4j relationship model.
- **Memory**: raw archive, vector lookup, graph memory, and episodic summaries.
- **Reasoning loops**: fast, medium, and deep loop boundaries for scheduled orchestration.
- **Portfolio simulator**: deterministic position and portfolio analytics engine.
- **Reporting**: report builder for hourly/daily autonomous insight summaries.
- **Scheduler metadata**: default job cadences for ingestion and reasoning loops.

## Next production steps

1. Replace `StaticNewsSource` with RSS/API/SEC/social source adapters.
2. Persist the shared models into PostgreSQL, Qdrant, and Neo4j repositories.
3. Swap the deterministic `EventExtractor` for a local llama.cpp extraction runtime that returns the same `ExtractedEvent` schema.
4. Wire `DEFAULT_JOBS` into APScheduler and expose operational controls through FastAPI.
5. Add Prometheus counters for ingestion rate, duplicate rate, extraction confidence, graph growth, and reasoning latency.
