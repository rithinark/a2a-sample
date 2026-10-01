# Programmatic Tool Calling

## Problem

Batch data-heavy tool work and keep intermediate results out of model context.

## When to use

Many calls are composable, results are large, and safe sandboxed code can do deterministic filtering.

## When not to use

Effects are high-risk, work is not composable, or code execution cannot be sandboxed/audited.

## Architecture

`model intent -> constrained program/batch -> sandboxed tools -> filtered artifact -> model decision`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Program spec, inputs, allowlisted tools, sandbox limits, artifacts, logs, result summary.

## Failure modes

Code injection, hidden side effects, runaway resources, opaque failures, stale artifacts.

## Cost / latency considerations

Can cut round trips/context but adds sandbox, execution, and observability overhead.

## Observability

Program hash, tool calls, resource use, artifacts, policy denials, compact result.

## Testing strategy

Test sandbox escape attempts, resource limits, failed calls, large output, equivalence to sequential baseline.

## Implementation notes

GENERAL PATTERN: delegate only constrained deterministic data work to a sandbox.

CLAUDE-SPECIFIC IMPLEMENTATION: native programmatic tool calling semantics are provider-specific.

## Anthropic reference

[Official Anthropic source](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/programmatic-tool-calling)
