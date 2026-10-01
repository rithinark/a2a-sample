# Orchestrator / Workers

## Problem

Decompose a task into owned, potentially independent work products.

## When to use

Subtasks have clear interfaces and measurable specialization or concurrency gains.

## When not to use

A single workflow can execute the work, or workers would share identical context/tools.

## Architecture

`coordinator -> task contracts -> workers -> artifacts -> coordinator -> verification`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Parent plan, task contracts, worker status, artifact IDs, merge/conflict state, budgets.

## Failure modes

Duplicate/conflicting work, runaway fan-out, shared-state races, shallow synthesis.

## Cost / latency considerations

Fan-out and synthesis cost grow quickly; cap concurrency and cancel obsolete tasks.

## Observability

Parent/child traces, task ownership, queue time, artifacts, merge decisions, aggregate cost.

## Testing strategy

Test partitioning, worker failure/cancellation, conflicting evidence, and single-worker baseline.

## Implementation notes

GENERAL PATTERN: use structured contracts and a deterministic merge policy where possible.

CLAUDE-SPECIFIC IMPLEMENTATION: no Claude-specific orchestration contract is required.

## Anthropic reference

[Official Anthropic source](https://platform.claude.com/cookbook/patterns-agents-multi-agent-research-system)
