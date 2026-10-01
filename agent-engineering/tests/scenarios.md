# Skill Scenario Tests

Use these prompts in fresh Codex runs with this skill available. Review the proposed architecture before accepting code. A passing response need not use the same implementation, but must meet the acceptance criteria.

| Scenario prompt | Expected behavior / acceptance criteria |
|---|---|
| “Build a simple FAQ bot for 20 fixed answers.” | Reject unnecessary agent/multi-agent design; prefer deterministic lookup or one bounded response; identify a fallback and basic observability. |
| “Build a 30-tool enterprise support agent that can change subscriptions.” | Scope tools or evaluate permission-filtered tool search; define schemas, authorization, side-effect approval, termination, and traces. |
| “Create a multi-agent research system.” | Require task decomposition benefit and worker contracts; bound fan-out; retain a single-agent baseline and evidence-based synthesis. |
| “Create an autonomous remediation agent for production incidents.” | Define state machine, policy gates, idempotency, time/budget limits, verification, approval for dangerous changes, rollback, and audit. |
| “Refactor this agent so it is reliable.” | Request/derive explicit state, tool contracts, terminal states, retries, failure taxonomy, evaluation fixtures, and observability. |
| “This workflow keeps running forever.” | Diagnose missing termination/no-progress guards; add max iterations, deadline/budget, terminal reasons, and bounded recovery. |
| “The context reaches 100k tokens after several tool calls.” | Separate artifacts from prompt, filter/retrieve, define compaction/external state and tests preserving critical facts. |
| “The model keeps choosing the wrong tool.” | Narrow/scoped tools, improve metadata/schema/examples, measure selection; consider discovery only if catalog size justifies it. |
| “Extract ETL lineage from SQL and docs.” | Choose parser-first deterministic extraction; use LLM only for ambiguity; maintain structured provenance and verification. |
| “Build a model routing gateway.” | Apply deterministic capability/policy filters before semantic classifier; isolate policy, account for cost/latency, trace routes/fallbacks. |

## Evaluation rubric

Score each response for: agent necessity, explicit state, bounded loop, minimal tools and validation, context plan, verification, deterministic-vs-model split, justified multi-agent use, cost/latency, and reconstructible observability. Any missing terminal condition for a loop or unguarded consequential tool action is a failure.
