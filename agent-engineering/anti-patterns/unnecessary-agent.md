# Unnecessary Agent

## Signal

A model loop is used for a stable rule, lookup, transformation, or fixed workflow.

## Why it fails

It increases cost, latency, nondeterminism, and incident surface while obscuring accountability.

## Reject or correct

Replace with deterministic code; retain a narrowly scoped model call only for genuine semantic ambiguity.

## Required guardrail

If a deterministic output changes, the result should be explainable and testable without a model.

## Review evidence

Ask for the state model, policy boundary, budget, trace, and a test that demonstrates the guardrail.
