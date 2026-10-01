# Context Compaction

## Problem

Keep long-running work within finite context while retaining decision-relevant facts.

## When to use

History/tool results grow beyond a budget and durable state can be extracted.

## When not to use

The full source is needed for an imminent high-stakes decision or no verification exists.

## Architecture

`history/artifacts -> extract canonical state -> summary + references -> continue`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Token budget, canonical facts/decisions/open tasks, provenance, stale markers, source refs.

## Failure modes

Lossy summary, stale facts, omitted constraints, compaction thrashing.

## Cost / latency considerations

Adds extraction/verification work but avoids repeated long-context cost and failure.

## Observability

Pre/post token size, extracted fields, source refs, validation, compaction trigger.

## Testing strategy

Test recall of critical facts, conflicting updates, repeated compaction, and source rehydration.

## Implementation notes

GENERAL PATTERN: persist canonical state externally and rehydrate by need.

CLAUDE-SPECIFIC IMPLEMENTATION: provider context-editing/compaction features are optional adapters.

## Anthropic reference

[Official Anthropic source](https://docs.anthropic.com/en/docs/build-with-claude/context-management)
