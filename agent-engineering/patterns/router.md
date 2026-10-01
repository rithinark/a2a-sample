# Router

## Problem

Select one bounded workflow or model capability from a request.

## When to use

A rule/capability filter cannot reliably classify semantic intent.

## When not to use

A fixed rule, allowlist, or deterministic capability check decides it.

## Architecture

`request -> policy/filter -> router -> selected handler -> validator`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Routing policy, candidate set, decision/confidence, reason, fallback.

## Failure modes

Ambiguous or malicious inputs, wrong route, route drift, fallback loops.

## Cost / latency considerations

One classification call; constrain candidates and cache only safe stable decisions.

## Observability

Route candidates, decision, confidence, policy exclusions, fallback, outcome.

## Testing strategy

Use labeled routing sets, ambiguous cases, denied routes, and cost/latency slices.

## Implementation notes

GENERAL PATTERN: apply deterministic filters first; return structured routing decisions.

CLAUDE-SPECIFIC IMPLEMENTATION: use current Claude tool/message APIs only behind a router interface.

## Anthropic reference

[Official Anthropic source](https://www.anthropic.com/engineering/building-effective-agents)
