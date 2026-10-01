---
name: agent-engineering
description: Design, implement, refactor, review, or debug bounded, observable agentic systems, including tool-using LLM workflows, RAG agents, model routers, multi-agent systems, and long-running autonomous workflows. Use when an implementation must choose an agent architecture, control tool use/context/state, or verify model-driven outcomes; do not use for ordinary deterministic application code with no agentic decision loop.
---

# Agent Engineering

Treat these as engineering constraints:

1. Determine whether an agent is necessary; prefer deterministic code for deterministic work.
2. State the objective, state ownership, side-effect boundary, and success measure explicitly.
3. Define termination, iteration, timeout, retry, and recovery before implementing any loop.
4. Expose narrow typed tools; validate inputs, scope authorization, and do not give direct access unless required.
5. Keep large/repeated/intermediate data outside model context; retrieve or summarize only decision-relevant facts.
6. Verify consequential outputs independently. Model generation is never verification.
7. Add observable state transitions, model calls, tool calls, retries, errors, costs, latency, and outcomes.
8. Use multi-agent designs only when independent work, specialization, or parallelism has a measured benefit.
9. Isolate provider mechanisms behind adapters; preserve vendor-neutral state and policy.
10. Prefer the simplest architecture that meets the requirement.

## Required reasoning before significant agent work

For a medium or large change, state briefly in the implementation plan:

1. **Classify:** deterministic workflow, LLM-assisted workflow, single agent, planner/executor, orchestrator/workers, evaluator/optimizer, router, multi-agent, retrieval/RAG, long-running, human-in-the-loop, and/or operational agent.
2. **Justify necessity:** decide whether autonomy, tools, iterative reasoning, or dynamic decomposition is actually required. Use a simpler workflow if not.
3. **Model state:** inputs, working/persistent state, tool results, artifacts, decisions, termination, errors, and retry state; name each owner.
4. **Model tools:** purpose, schema, outputs, side effects, idempotency, timeout, authorization, and failure behavior; decide if direct model access is necessary.
5. **Model the loop:** initial state, actions, observation/update, explicit stopping conditions, maximum iterations, deadline, and recovery. Reject unbounded loops.
6. **Model verification:** select schema, deterministic, tool-based, evaluator, and/or human checks proportionate to impact.
7. **Model context:** forecast growth; filter tool results; decide compaction, summaries, external persistence, retrieval, and staleness rules.
8. **Model operations:** budget model calls/tokens/tool work/latency and define trace fields and alerts.

For a small change, apply applicable constraints silently and record only decisions that affect behavior or risk.

## Selective reading

- Start with [architecture](references/architecture.md) and the [architecture review checklist](references/architecture-review-checklist.md).
- Load [agent loops](references/agent-loops.md), [tool design](references/tool-design.md), [context engineering](references/context-engineering.md), and [verification](references/verification.md) whenever their component exists.
- Load pattern files only after the architecture decision; load matching anti-patterns to challenge it.
- Load [vendor adaptation](references/vendor-adaptation.md) for platform/API choices and [source index](references/source-index.md) for official provenance.
- Use [tests/scenarios.md](tests/scenarios.md) to forward-test architecture behavior before approving major systems.
