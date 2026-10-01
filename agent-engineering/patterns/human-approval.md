# Human Approval

## Problem

Control consequential actions when automation cannot safely decide alone.

## When to use

An action is irreversible, privileged, high impact, or materially uncertain.

## When not to use

A low-risk reversible action is fully covered by deterministic policy.

## Architecture

`proposal -> validation -> action preview -> authorized approval -> exact execution -> audit`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Action hash, preview, evidence, risk, approver, scope, expiry, decision, execution result.

## Failure modes

Approval fatigue, stale approval, ambiguous preview, bypass, unlogged execution.

## Cost / latency considerations

Adds human latency; reserve it for risk and make queues/expiry visible.

## Observability

Preview, action hash, approver, authorization, expiry, decision, executed action, rollback.

## Testing strategy

Test rejection, expiry, modification-after-approval, unauthorized approver, and audit completeness.

## Implementation notes

GENERAL PATTERN: bind approval to exact validated intent and preserve rollback/audit.

CLAUDE-SPECIFIC IMPLEMENTATION: approval is application policy, not a model feature.

## Anthropic reference

[Official Anthropic source](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)
