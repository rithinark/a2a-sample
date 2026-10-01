# Agent Engineering Skill

A vendor-neutral Codex skill for designing, implementing, reviewing, and debugging production-oriented agentic systems. It converts official Anthropic Cookbook and documentation patterns into decision rules rather than copying recipes.

## Install and use

Copy `agent-engineering/` into a Codex skills directory (for example, `$CODEX_HOME/skills/agent-engineering`). Codex activates it for requests about agentic systems, tool-using LLM workflows, multi-agent systems, RAG, routers, and long-running autonomous workflows. The body of `SKILL.md` is intentionally concise; load only the related reference or pattern file as needed.

## Layout

- `SKILL.md` — operational engineering contract.
- `references/` — architecture rules, provider adaptation, source provenance, checklists, and domain guidance.
- `patterns/` — selectable architectures with constraints and tests.
- `anti-patterns/` — designs to reject or correct.
- `tests/` — scenario prompts and expected architecture behaviors.
- `scripts/` — offline validation and optional source-link maintenance.

## Provenance and updates

`references/source-index.md` records authoritative official URLs and its retrieval date. The skill works offline after installation; live access is optional. When sources change, update the index, refresh only affected summaries, mark deprecated guidance, and run the validators. Add a pattern only after documenting its problem, contraindications, state, failure modes, economics, observability, testing, and vendor boundary.

## Tests

Run `python scripts/validate_skill.py .` from this directory. Review `tests/scenarios.md` against a Codex run: each scenario has behavior-based acceptance criteria, not a prescribed implementation.
