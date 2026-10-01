# Parallel Workers

## Problem

Reduce critical-path time for independent bounded tasks.

## When to use

Tasks have no ordering/data dependency and results can be merged deterministically.

## When not to use

Tasks share mutable state, have rate limits, or coordination dominates.

## Architecture

`input -> independent workers (bounded fan-out) -> join -> validation`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Task list, worker status, deadlines, cancellation, result artifacts, join policy.

## Failure modes

Rate-limit bursts, partial failure, nondeterministic merge, duplicated effects.

## Cost / latency considerations

Can reduce latency but increases total calls; set concurrency and per-worker budgets.

## Observability

Fan-out count, queue/execute time, cancellation, partial results, join outcome.

## Testing strategy

Test one/many/zero tasks, slow worker, partial failure, duplicate and ordering cases.

## Implementation notes

GENERAL PATTERN: parallelize only pure or idempotent work and join by a declared policy.

CLAUDE-SPECIFIC IMPLEMENTATION: provider concurrency limits belong in the adapter.

## Anthropic reference

[Official Anthropic source](https://www.anthropic.com/engineering/building-effective-agents)
