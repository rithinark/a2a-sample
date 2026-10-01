# Vendor Adaptation

## General agent engineering principles

Architecture, explicit state, typed capability boundaries, bounded loops, retrieval/filtering, verification, approval, evaluation, and observability must survive a provider change. Define interfaces around model invocation, tool registry/execution, state store, retrieval, tracing, and policy.

## Anthropic-specific features

Claude tool-use formats, tool-search tools, programmatic tool calling, context-management/context-editing controls, prompt-cache semantics, Agent SDK APIs, and Cookbook recipes are implementation options. Consult the official URL in [source-index.md](source-index.md) before use; do not leak their request/response objects into domain state.

## OpenAI-specific features

Use OpenAI's current Responses/Agents capabilities, tool/function calling, tracing, and provider controls only behind the same interfaces. Verify current official OpenAI documentation before relying on any context, caching, or orchestration feature; feature names and guarantees differ.

## Framework-specific implementations

LangGraph, an Agents SDK, workflow engines, queues, and custom state machines may implement the architecture. Framework control flow must still expose state ownership, permissions, termination, budgets, retries, and traces. Do not mistake a framework abstraction for a safety property.
