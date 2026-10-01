# Tool Design

A tool is a capability boundary, not a prompt convenience. Give every tool a narrow name, typed input/output schema, examples of valid/invalid inputs, error taxonomy, timeout, authorization policy, idempotency semantics, and audit fields.

Validate model-supplied arguments before execution. Separate read from write tools; make dangerous writes previewable and approval-gated. Return compact, decision-relevant result summaries plus stable artifact references rather than raw dumps. Put deterministic computation, parsing, filtering, and policy enforcement in code.

**Selection rules:** Few known tools → explicitly scope them. Large changing catalog → evaluate search/discovery plus allowlists. Many independent calls or huge results → batch/external processing or programmatic execution, while retaining sandboxing, quotas, and result validation.
