# Blind Tool Calls

## Signal

Model-generated arguments execute without schema, policy, or permission checks.

## Why it fails

It increases cost, latency, nondeterminism, and incident surface while obscuring accountability.

## Reject or correct

Validate arguments; separate reads/writes; enforce authorization, idempotency, timeout, preview, and audit.

## Required guardrail

Reject direct execution of high-impact actions.

## Review evidence

Ask for the state model, policy boundary, budget, trace, and a test that demonstrates the guardrail.
