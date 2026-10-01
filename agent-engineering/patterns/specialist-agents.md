# Specialist Agents

## Problem

Apply distinct expertise, tool permissions, or evaluation criteria to separate subproblems.

## When to use

Specialization is real, interfaces are crisp, and a baseline shows benefit.

## When not to use

Roles differ only in persona text or coordination cost exceeds the gain.

## Architecture

`coordinator -> specialist contract -> evidence artifact -> integration/verification`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Specialty contract, permitted tools/data, task, artifacts, confidence, handoff criteria.

## Failure modes

Siloed partial answers, contradictory advice, privilege expansion, coordination overhead.

## Cost / latency considerations

Extra prompts/calls and integration add latency; limit specialists to proven domains.

## Observability

Specialist version, permissions, task, evidence, conflicts, integration decision.

## Testing strategy

Compare one-agent baseline; test boundary cases, conflicts, unauthorized requests, and handoffs.

## Implementation notes

GENERAL PATTERN: specialize capabilities and rubrics, not just personalities.

CLAUDE-SPECIFIC IMPLEMENTATION: use provider-specific agents only through common contracts.

## Anthropic reference

[Official Anthropic source](https://platform.claude.com/cookbook/patterns-agents-multi-agent-research-system)
