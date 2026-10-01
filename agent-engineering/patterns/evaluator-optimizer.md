# Evaluator / Optimizer

## Problem

Improve a candidate against a defined quality rubric.

## When to use

A rubric exists, deterministic checks are insufficient, and bounded revisions improve outcomes.

## When not to use

There is no measurable rubric or a deterministic validator can decide correctness.

## Architecture

`generator -> validators/evaluator -> bounded repair -> terminal accept/escalate`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Candidate versions, rubric, evidence, scores, revision count, acceptance reason.

## Failure modes

Self-confirmation bias, rubric gaming, endless rewrites, evaluator disagreement.

## Cost / latency considerations

Adds at least one evaluation call per iteration; cap revisions and preserve best candidate.

## Observability

Version, evaluator inputs/result, failing criterion, revision, final reason.

## Testing strategy

Use gold cases, evaluator-human agreement, adversarial rubric gaming, max-revision cases.

## Implementation notes

GENERAL PATTERN: make acceptance criteria explicit and prefer independent checks.

CLAUDE-SPECIFIC IMPLEMENTATION: evaluator calls are ordinary provider calls behind an interface.

## Anthropic reference

[Official Anthropic source](https://www.anthropic.com/engineering/building-effective-agents)
