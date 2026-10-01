# Failure Handling

Classify failures as invalid input, model format/choice, transient tool/network, permanent tool/policy, stale/conflicting state, timeout/budget, or unsafe request. Define deterministic handling for each: reject, repair once or bounded times, retry with backoff/idempotency key, degrade, escalate, or terminate safely.

Do not silently retry side effects. Detect no progress using state changes, not merely iteration count. Preserve a replayable sanitized trace and make recovery compensation explicit.
