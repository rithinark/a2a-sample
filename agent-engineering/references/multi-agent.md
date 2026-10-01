# Multi-Agent Architecture

Choose coordinator/workers only when work can be partitioned with clear ownership, bounded interfaces, and an expected quality, latency, or throughput benefit. A coordinator assigns tasks and integration criteria; workers return structured artifacts, evidence, confidence, and terminal status. The coordinator—not a shared prompt—owns final assembly and cancellation.

Use parallel workers for independent tasks; specialist agents for materially different prompts/tools/evaluators. Do not add agents merely to imitate a team, split a tiny task, or compensate for vague state. Budget fan-out, prevent recursive delegation, cap workers, and define conflict resolution. Trace parent/child runs, task contracts, artifact IDs, duplication, and aggregate cost.
