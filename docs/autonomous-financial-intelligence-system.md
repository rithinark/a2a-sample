# Autonomous Financial Intelligence System — Implementation Plan

## Vision

Build a continuously running financial research operating system that ingests market information, extracts structured knowledge, maintains multi-layer memory, reasons over time, tracks a mock portfolio, and generates autonomous insights.

The system should optimize for reliable memory, retrieval quality, event modeling, graph reasoning, and orchestration rather than relying on one large conversational agent.

## Target Architecture

```text
News / social / structured sources
        ↓
Ingestion layer
        ↓
Deduplication + parsing
        ↓
Event extraction
        ↓
Graph DB + Vector DB + Timeseries DB
        ↓
Scheduled reasoning agents
        ↓
Deterministic portfolio simulator
        ↓
Insight reports and alerts
```

## Recommended Technology Stack

| Component | Recommended technology | Purpose |
| --- | --- | --- |
| API | FastAPI | External control plane, health checks, report access, portfolio endpoints |
| Queue | Redis | Lightweight broker for ingestion and extraction jobs |
| Workers | Celery or Dramatiq | Distributed background processing |
| Relational DB | PostgreSQL | Raw archive, normalized articles, portfolio state, metrics |
| Vector DB | Qdrant | Semantic retrieval and semantic deduplication |
| Graph DB | Neo4j | Entity, event, exposure, and relationship reasoning |
| LLM runtime | llama.cpp | Local inference for extraction, summarization, and reasoning |
| Agent orchestration | LangGraph | Planner/executor/reflection workflows |
| Scheduler | APScheduler | Fast, medium, and deep reasoning loops |
| Monitoring | Prometheus + Grafana | Operational visibility and quality tracking |

## Repository Layout

The long-term codebase should be organized around runtime apps, domain modules, infrastructure adapters, and specialized agents:

```text
financial_ai/
├── apps/
│   ├── api/
│   ├── workers/
│   ├── scheduler/
│   └── dashboard/
├── domains/
│   ├── ingestion/
│   ├── extraction/
│   ├── graph/
│   ├── portfolio/
│   ├── reasoning/
│   └── memory/
├── infrastructure/
│   ├── llm/
│   ├── qdrant/
│   ├── neo4j/
│   ├── postgres/
│   └── redis/
├── agents/
│   ├── planner/
│   ├── executor/
│   ├── reflection/
│   └── reporting/
└── shared/
```

## Phase 1 — Foundation

**Goal:** establish the infrastructure baseline before adding expensive reasoning.

### Deliverables

- Docker Compose stack for PostgreSQL, Redis, Qdrant, Neo4j, Prometheus, and Grafana.
- FastAPI control plane with readiness and liveness checks.
- Worker process with a simple queue consumer.
- APScheduler process with disabled-by-default scheduled jobs.
- Shared configuration module for service URLs, model paths, queue names, and loop intervals.
- Database migrations for the first archive and portfolio tables.

### Acceptance criteria

- `docker compose up` starts all infrastructure services.
- API health endpoint verifies PostgreSQL, Redis, Qdrant, and Neo4j connectivity.
- A test job can be enqueued, consumed, and persisted.
- Metrics endpoint exposes queue depth, worker success count, worker failure count, and job latency.

## Phase 2 — News Ingestion Layer

**Goal:** continuously collect market-relevant information from financial news, social sources, and structured feeds.

### Initial sources

- Financial news: Reuters, Yahoo Finance, MarketWatch, CNBC.
- Social: Reddit finance communities and curated finance accounts on X/Twitter.
- Structured data: SEC filings, earnings calendars, and macroeconomic calendars.

### Worker flow

```text
RSS/API poller
    ↓
raw_document queue
    ↓
parser worker
    ↓
normalized_document table
```

### Raw article schema

```sql
CREATE TABLE raw_articles (
    id UUID PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT,
    content TEXT,
    url TEXT UNIQUE,
    published_at TIMESTAMP,
    checksum TEXT NOT NULL,
    ingested_at TIMESTAMP NOT NULL DEFAULT now()
);
```

### Normalized article schema

```sql
CREATE TABLE normalized_articles (
    id UUID PRIMARY KEY,
    raw_article_id UUID NOT NULL REFERENCES raw_articles(id),
    canonical_title TEXT,
    canonical_content TEXT NOT NULL,
    language TEXT,
    tickers TEXT[],
    source_reliability NUMERIC,
    normalized_at TIMESTAMP NOT NULL DEFAULT now()
);
```

## Phase 3 — Deduplication and Cleaning

**Goal:** prevent token explosion, repetitive reasoning, and low-quality memory.

### Deduplication strategy

1. Compute `sha256(content)` for exact duplicate detection.
2. Generate embeddings for normalized content.
3. Query Qdrant for nearest neighbors.
4. Mark documents as duplicates when cosine similarity exceeds `0.95`.
5. Preserve duplicate references for auditability, but only reason over the canonical article.

### Cleaning requirements

- Remove boilerplate, navigation text, cookie banners, and repeated disclaimers.
- Normalize timestamps to UTC.
- Preserve source attribution and URL lineage.
- Store parsing confidence and extraction warnings.

## Phase 4 — Event Extraction

**Goal:** convert unstructured articles into structured market events.

### Extraction fields

The extraction layer should identify:

- companies
- tickers
- sectors
- event type
- sentiment
- risk level
- catalysts
- affected entities
- macroeconomic impact
- confidence
- source evidence spans

### JSON output contract

```json
{
  "entities": [],
  "events": [],
  "sentiment": {},
  "relationships": [],
  "confidence": 0.0,
  "evidence": []
}
```

### Model strategy

- Primary extraction and summarization model: local Gemma-class small model quantized for available hardware.
- Optional code/schema specialist: Qwen2.5 Coder-class model for prompt and schema development.
- Embeddings: small local embedding model with stable vector dimensions.

Extraction should be schema-validated. Invalid outputs must be stored with error metadata and sent to a repair queue rather than silently discarded.

## Phase 5 — Knowledge Graph

**Goal:** make the graph the primary intelligence layer.

### Node types

- `Company`
- `Sector`
- `Commodity`
- `Country`
- `Person`
- `Event`
- `Theme`
- `PortfolioPosition`

### Relationship types

- `AFFECTS`
- `SUPPLIES`
- `COMPETES_WITH`
- `OWNS`
- `MENTIONS`
- `CORRELATED_WITH`
- `EXPOSED_TO`
- `BENEFITS_FROM`
- `HURT_BY`
- `DEPENDS_ON`

### Example relationship pattern

```text
NVIDIA
  ├─ BENEFITS_FROM → AI Demand
  ├─ DEPENDS_ON → TSMC
  ├─ CORRELATED_WITH → Semiconductor ETF
  └─ COMPETES_WITH → AMD
```

### Graph principles

- Every relationship must include source article IDs and confidence.
- Events should be temporal nodes, not static properties.
- Derived edges should reference the reasoning job that created them.
- Low-confidence edges should expire or require reinforcement.

## Phase 6 — Memory System

**Goal:** support auditability, semantic retrieval, graph reasoning, and compressed long-term recall.

### Layer 1 — Raw archive

Store every raw source document for replay, audit, and future retraining.

### Layer 2 — Vector memory

Use Qdrant for semantic lookup, examples such as “recent semiconductor supply chain disruptions”.

### Layer 3 — Graph memory

Use Neo4j for relationship reasoning, examples such as “which companies are indirectly exposed to oil price spikes?”

### Layer 4 — Episodic memory

Generate daily and weekly compressed summaries such as “AI infrastructure spending accelerated across hyperscalers this week.”

## Phase 7 — Reasoning Agents

**Goal:** use scheduled reasoning loops instead of continuous chat.

### Fast loop — every 5 minutes

- classify incoming news
- detect urgency
- update graph with direct facts
- enqueue alerts for high-risk events

### Medium loop — hourly

- correlate related events
- detect sector movement
- identify sentiment shifts
- summarize emerging themes

### Deep loop — daily

- review mock portfolio
- update investment theses
- analyze macro regime changes
- produce reflection notes and quality metrics

### LangGraph design

```text
Planner
  ↓
Task queue
  ↓
Specialized workers
  ↓
Memory update
  ↓
Reflection
```

Use separate planner, executor, reflection, memory, and reporting agents. Avoid a single large ReAct loop because it is difficult to scale, observe, and debug.

## Phase 8 — Portfolio Simulator

**Goal:** keep portfolio accounting deterministic and separate from LLM reasoning.

### Position schema

```sql
CREATE TABLE positions (
    id UUID PRIMARY KEY,
    ticker TEXT NOT NULL,
    entry_price NUMERIC NOT NULL,
    quantity NUMERIC NOT NULL,
    thesis TEXT,
    confidence NUMERIC,
    opened_at TIMESTAMP NOT NULL DEFAULT now(),
    closed_at TIMESTAMP
);
```

### Engine responsibilities

- unrealized profit and loss
- realized profit and loss
- volatility
- exposure by ticker, sector, theme, and country
- sector concentration
- win rate
- Sharpe-like metrics
- alert generation for thesis violations

LLMs may propose trades or risk alerts, but deterministic portfolio code must calculate accounting and risk metrics.

## Phase 9 — Autonomous Strategy Layer

**Goal:** evolve from reporting to proposal generation while preserving auditability.

Example workflow:

```text
Oil price spike
    ↓
Detect airline margin exposure
    ↓
Find negatively correlated airline stocks
    ↓
Check existing portfolio exposure
    ↓
Generate risk alert
```

Trade proposals should include source evidence, graph path explanations, confidence, risk scenario, invalidation criteria, and historical performance of similar proposals.

## Phase 10 — Insight Generation

### Hourly report

- top events
- sector shifts
- emerging risks
- notable correlations
- high-confidence graph updates

### Daily report

- portfolio performance
- thesis validation
- major macro events
- reflection
- extraction quality statistics
- reasoning latency and cost summary

## Phase 11 — Observability

Track both system health and intelligence quality:

- extraction accuracy
- extraction repair rate
- hallucination or unsupported-claim rate
- token usage
- local inference latency
- queue lag
- graph growth
- duplicate rate
- portfolio metric accuracy
- alert precision and follow-through

## Phase 12 — Cost and Latency Optimization

The core rule is to avoid repeatedly re-reasoning over old data.

Use:

- incremental graph updates
- compressed episodic memory
- retrieval-first reasoning
- semantic deduplication
- low-cost fast loop models
- expensive daily reflection only when enough new evidence exists

## Implementation Milestones

| Milestone | Scope | Exit criteria |
| --- | --- | --- |
| M1 | Infrastructure | Compose stack, health checks, queue smoke test |
| M2 | Ingestion | One RSS source ingested and normalized end-to-end |
| M3 | Dedup | Exact and semantic dedup with canonical article selection |
| M4 | Extraction | Schema-valid event extraction stored with confidence and evidence |
| M5 | Memory | Article embeddings in Qdrant and event/entity relationships in Neo4j |
| M6 | Reasoning | Fast, medium, and daily loops producing persisted run records |
| M7 | Portfolio | Deterministic mock portfolio accounting and exposure reporting |
| M8 | Reports | Hourly and daily generated reports exposed through API |
| M9 | Observability | Grafana dashboard for health, latency, quality, and cost metrics |

## Non-Goals for the Initial Release

- Real-money trading or broker execution.
- Fully autonomous trade execution.
- Unverified social-media-only signals driving portfolio decisions.
- Reasoning over articles without source attribution.
- A single giant conversational loop as the central architecture.

## Risk Controls

- Require source evidence for every extracted claim.
- Keep raw documents immutable for replay.
- Track confidence and provenance on every graph edge.
- Separate LLM proposals from deterministic portfolio state changes.
- Add review gates before any future real trading integration.
- Maintain model/version metadata on every reasoning output.
