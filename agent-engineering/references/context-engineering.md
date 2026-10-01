# Context Engineering

Budget context like memory. Track static instructions, history, tool definitions, retrieved passages, and tool results separately. Keep canonical state and artifacts externally; inject only the current decision slice.

Use retrieval for a large corpus, filtering before insertion, and references instead of raw payloads. Compact only after extracting durable facts, decisions, open tasks, constraints, provenance, and stale-data markers. Test that compaction preserves required information. Cache stable prefixes only when provider semantics and privacy policy permit it.

Trigger compaction or state extraction by forecasted token budget, not only model failure. Never treat a summary as authoritative if the source artifact is available and material to a side effect.
