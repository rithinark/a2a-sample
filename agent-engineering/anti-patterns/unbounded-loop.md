# Unbounded Loop

## Signal

The agent can continue calling itself or tools without explicit terminal conditions.

## Why it fails

It increases cost, latency, nondeterminism, and incident surface while obscuring accountability.

## Reject or correct

Define terminal states, maximum iterations, deadline, budgets, no-progress detection, and bounded recovery.

## Required guardrail

Reject before implementation; tool retries must not be implicit.

## Review evidence

Ask for the state model, policy boundary, budget, trace, and a test that demonstrates the guardrail.
