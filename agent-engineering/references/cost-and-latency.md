# Cost and Latency

Estimate the critical path and fan-out: model calls × input/output tokens, retrieval, tool latency, verifier calls, retries, and coordination. Set per-run and per-tenant budgets with graceful terminal states. Use deterministic routing/capability filters before model routing, smaller models only after quality evaluation, parallelism only for independent work, caching only for stable/reusable data, and batching where it preserves control.

Optimize after measurement. A cheap architecture that needs repeated repair can cost more and be slower than one correct bounded call.
