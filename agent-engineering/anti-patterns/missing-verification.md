# Missing Verification

## Signal

Generated output is treated as correct because a model produced it.

## Why it fails

It increases cost, latency, nondeterminism, and incident surface while obscuring accountability.

## Reject or correct

Add schemas, deterministic/tool checks, evaluator rubric, and/or approval based on impact.

## Required guardrail

Generator and verifier should not share unexamined assumptions.

## Review evidence

Ask for the state model, policy boundary, budget, trace, and a test that demonstrates the guardrail.
