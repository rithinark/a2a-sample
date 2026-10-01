# LLM-Only Orchestration

## Signal

A model controls retries, queues, policies, budgets, and side effects that require deterministic guarantees.

## Why it fails

It increases cost, latency, nondeterminism, and incident surface while obscuring accountability.

## Reject or correct

Put scheduling, permissions, idempotency, budget enforcement, and transitions in code; model only chooses within policy.

## Required guardrail

An LLM may propose, but code must enforce.

## Review evidence

Ask for the state model, policy boundary, budget, trace, and a test that demonstrates the guardrail.
