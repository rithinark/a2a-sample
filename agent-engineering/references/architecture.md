# Architecture Selection

Choose the smallest architecture that satisfies the uncertainty and side-effect profile.

| Workload | Default | Escalate only when | Avoid when |
|---|---|---|---|
| Deterministic transformation | Code/workflow | Inputs need semantic interpretation | Rules or parsers can decide |
| LLM-assisted workflow | One model call plus validation | A bounded tool/reason loop is necessary | Output is fully deterministic |
| Router | Rules/capability filter | Semantic ambiguity warrants a classifier | A static rule answers it |
| Planner/executor | Planner produces a bounded plan; executor validates steps | Steps depend on discovered facts | Direct workflow is known |
| Orchestrator/workers | Coordinator delegates independent, owned subproblems | Parallelism/specialization reduces time or errors | Workers share the same context/toolset |
| Evaluator/optimizer | Generator plus independent checks | Revision is needed and a rubric exists | A deterministic validator suffices |
| Retrieval/RAG | Retrieve, filter, cite, then answer | Corpus is too large or changes | Facts are already in structured storage |
| Long-running agent | Persisted state machine | Work exceeds a request/session boundary | A synchronous job suffices |

Architectural assumptions: model outputs are fallible; tools and networks fail; context is finite; side effects require a policy boundary. Explicitly record which assumption is being made and test its failure.
