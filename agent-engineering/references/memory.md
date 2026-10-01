# Memory

Separate request state, session memory, durable domain data, and episodic traces. Persist facts only with provenance, scope, expiry/staleness policy, ownership, and a correction path. Retrieval should filter by tenant, permissions, relevance, and recency.

Do not use hidden prompt history as the system of record. Do not persist private reasoning as user memory. Evaluate memory with insertion, retrieval, conflict, expiry, deletion, and cross-tenant isolation cases.
