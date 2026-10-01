# Official Source Index

**Source retrieval date:** 2026-10-01. **Authority:** official Anthropic pages below. Live retrieval was attempted while preparing this skill; the environment's web gateway returned HTTP 401 and direct access was blocked with HTTP 403. Treat the URLs as the canonical update targets and re-verify feature/API details before provider-specific implementation. The guidance in this skill deliberately retains only vendor-neutral architectural conclusions, not copied recipe code.

| Topic | Official source | Pattern / capability | Problem solved | Applicability |
|---|---|---|---|---|
| Cookbook index | [Claude Cookbook](https://platform.claude.com/cookbook/) | Curated implementation recipes | Discover current recipes and assumptions | Source index; recipes are not defaults |
| Agent skills | [Agent Skills overview](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) | Progressive, task-specific instructions and resources | Reusable agent capabilities without bloated prompts | General concept; packaging is provider-specific |
| Tool use | [Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) | Typed tool contracts and tool-result loop | Let a model request bounded external actions | General |
| Tool search | [Tool search tool](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/tool-search-tool) | Dynamic tool discovery | Large tool catalogs and prompt/tool-definition cost | General concept; native mechanism is provider-specific |
| Programmatic tool calling | [Programmatic tool calling](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/programmatic-tool-calling) | Model-directed code batches tool work | Reduce round trips and retain only useful results | Partially vendor-specific |
| Context management | [Context management](https://docs.anthropic.com/en/docs/build-with-claude/context-management) | Compaction, clearing, summaries | Long-running context growth | General concept; controls vary by provider |
| Prompt caching | [Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) | Reuse stable prompt prefixes | Repeated-input cost and latency | Provider-specific feature; general cache design |
| Agent SDK | [Agent SDK overview](https://docs.anthropic.com/en/docs/agent-sdk/overview) | Agent runtime patterns | SDK-managed tools, sessions, and execution | Patterns general; APIs vendor-specific |
| Multi-agent | [Multi-agent research system](https://platform.claude.com/cookbook/patterns-agents-multi-agent-research-system) | Coordinator and specialists | Parallel/deep task decomposition | General, only with measurable decomposition benefit |
| Agent patterns | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflows vs. agents; simple composition | Select the least-complex reliable architecture | General |
| Evaluation | [Define success criteria](https://docs.anthropic.com/en/docs/test-and-evaluate/define-success) | Task-specific success measures | Make quality testable | General |
| Evaluation | [Develop tests](https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests) | Test cases and graders | Detect regressions and unsafe behavior | General |
| Observability | [Evaluation tool](https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool) | Traceable evaluation runs | Diagnose quality/cost changes | General concept |
| Retrieval | [Embeddings overview](https://docs.anthropic.com/en/docs/build-with-claude/embeddings) | External retrieval | Ground answers in relevant corpus slices | General |
| Safety / approvals | [Tool use implementation](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use) | Validation and execution boundary | Control side effects and tool errors | General |

## How to use this inventory

For each pattern, read the linked official source when online, then capture the problem, contraindications, assumptions, failure modes, and vendor boundary in the corresponding local reference. Do not elevate an example recipe into a universal requirement. Update this table and its retrieval date when sources move or change.
