# Planner / Executor

## Problem

Handle a goal whose valid steps depend on discovered information.

## When to use

Planning materially reduces errors and the plan can be bounded and validated before effects.

## When not to use

Known fixed workflows or when a vague plan would become hidden state.

## Architecture

`goal -> planner -> validated bounded plan -> executor -> observations -> replan/terminal`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Goal, plan version, step preconditions, completed steps, observations, replan count.

## Failure modes

Invalid plans, stale preconditions, unsafe execution, replan loops.

## Cost / latency considerations

Planning adds calls and latency; execute deterministic steps directly when possible.

## Observability

Plan, validation results, step transitions, precondition failures, replan reason.

## Testing strategy

Test bad/stale plans, failed step, forbidden operation, max replan, successful fixed workflow.

## Implementation notes

GENERAL PATTERN: store plans as data and validate each effect at execution time.

CLAUDE-SPECIFIC IMPLEMENTATION: keep planner message/tool formats out of domain state.

## Anthropic reference

[Official Anthropic source](https://www.anthropic.com/engineering/building-effective-agents)
