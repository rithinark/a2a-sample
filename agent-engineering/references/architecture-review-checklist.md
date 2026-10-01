# Architecture Review Checklist

- **Architecture:** Is an agent necessary and as simple as possible?
- **State:** Are inputs, artifacts, ownership, persistence, and terminal/error states explicit?
- **Tools:** Are they minimal, typed, validated, permission-scoped, timeout-bounded, and side-effect controlled?
- **Loop:** Are stopping conditions, maximum iterations, retries, deadlines, and no-progress behavior explicit?
- **Context:** Is growth forecast, are results filtered, and are stale/large data compacted or externalized?
- **Verification:** Which schema, deterministic, tool, evaluator, and human checks verify outputs and actions?
- **Reliability/security:** Are tool/model failures, untrusted input, idempotency, rollback, secrets, and tenancy handled?
- **Cost/latency:** Is model selection justified and are budgets, fan-out, cache, and critical path measured?
- **Observability:** Can an engineer reconstruct transitions, calls, errors, retries, costs, and outcomes safely?
- **Testing:** Do normal, failure, edge, adversarial, and regression cases exercise the above?
