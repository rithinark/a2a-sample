# Observability

Emit structured events for run start/end, state transition, model request/response metadata, tool request/result, retry, policy/approval decision, validation outcome, compaction, and error. Link events with run, parent, task, tenant, artifact, tool, model, prompt/version, and idempotency identifiers; redact secrets and sensitive payloads.

Capture token/cost estimates and latency per stage. Alert on error rate, invalid actions, no-progress loops, budget exhaustion, tool denial, retrieval emptiness, and quality regression. An engineer should be able to reconstruct a run without exposing chain-of-thought or secret tool results.
