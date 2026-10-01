# Tool Search

## Problem

Select relevant tools from a large, changing catalog without exposing all definitions.

## When to use

The catalog is large enough to hurt context/cost and metadata can support reliable discovery.

## When not to use

A small stable set is known for the task or search recall cannot be evaluated.

## Architecture

`request -> policy allowlist -> tool search -> scoped tools -> call -> validation`

## Control flow

Execute each arrow as a bounded transition; validate before crossing any side-effect boundary and end with a declared terminal state.

## State requirements

Tool metadata/index, permissions, search query/results, selected tool set, expiry.

## Failure modes

Missed tool, irrelevant/unsafe tool exposure, stale metadata, permission bypass.

## Cost / latency considerations

Search adds a stage but can reduce tool-schema tokens and wrong-tool calls.

## Observability

Search query/results, permissions filtered, selected tools, call success, recall failures.

## Testing strategy

Measure allowed-tool recall, unsafe exposure, ambiguous queries, stale catalog, baseline cost.

## Implementation notes

GENERAL PATTERN: search only allowlisted metadata and validate selection/execution.

CLAUDE-SPECIFIC IMPLEMENTATION: native tool search is an optional provider optimization.

## Anthropic reference

[Official Anthropic source](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/tool-search-tool)
