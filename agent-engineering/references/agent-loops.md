# Bounded Agent Loops

Use an agent loop only when the next action depends on observations that cannot be encoded as a fixed workflow. Represent it as a state machine, not an implicit chat transcript.

**Required guards:** `max_iterations`, wall-clock deadline, token/cost budget, allowed actions by state, idempotency keys for effects, retry classification, and terminal reason. A tool failure, malformed model action, duplicate effect, approval denial, budget exhaustion, and no-progress iteration must have defined transitions.

**Decision rules:** If a loop has no explicit terminal state, reject it. If repeated critique/rewrite follows a rubric, consider evaluator/optimizer. If a plan is stable, execute it deterministically. Record `run_id`, state transition, action, observation summary, guard values, and terminal reason.
