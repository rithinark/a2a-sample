#!/usr/bin/env python3
"""Offline structural checks for the Agent Engineering skill."""
from __future__ import annotations
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1])
errors: list[str] = []
skill = root / "SKILL.md"
if not skill.is_file(): errors.append("missing SKILL.md")
else:
    text = skill.read_text()
    if not re.match(r"^---\nname: agent-engineering\ndescription: .+\n---\n", text): errors.append("invalid SKILL.md front matter")
required = ["references/source-index.md", "references/architecture-review-checklist.md", "references/vendor-adaptation.md", "references/maintenance.md", "tests/scenarios.md"]
patterns = ["router", "orchestrator-workers", "evaluator-optimizer", "parallel-workers", "planner-executor", "tool-search", "programmatic-tool-calling", "context-compaction", "specialist-agents", "human-approval"]
anti = ["unnecessary-agent", "unbounded-loop", "giant-context", "excessive-tools", "blind-tool-calls", "multi-agent-by-default", "llm-for-deterministic-work", "missing-verification", "hidden-state"]
for relative in required + [f"patterns/{x}.md" for x in patterns] + [f"anti-patterns/{x}.md" for x in anti]:
    if not (root / relative).is_file(): errors.append(f"missing {relative}")
for filename in patterns:
    content = (root / "patterns" / f"{filename}.md").read_text() if (root / "patterns" / f"{filename}.md").is_file() else ""
    for heading in ["Problem", "When to use", "When not to use", "Architecture", "Control flow", "State requirements", "Failure modes", "Cost / latency considerations", "Observability", "Testing strategy", "Implementation notes", "Anthropic reference"]:
        if f"## {heading}" not in content: errors.append(f"patterns/{filename}.md missing {heading}")
if errors:
    print("INVALID\n" + "\n".join(f"- {error}" for error in errors)); sys.exit(1)
print("VALID: agent-engineering skill structure and required pattern sections")
