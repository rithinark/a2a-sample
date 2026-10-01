# Over-Engineered Routing

## Signal

A classifier/router is added where explicit rules or a single handler suffice.

## Why it fails

It increases cost, latency, nondeterminism, and incident surface while obscuring accountability.

## Reject or correct

Use deterministic capability/policy filtering first; add semantic routing only for measured ambiguity.

## Required guardrail

Evaluate routing accuracy and fallback behavior before launch.

## Review evidence

Ask for the state model, policy boundary, budget, trace, and a test that demonstrates the guardrail.
