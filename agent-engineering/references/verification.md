# Verification

Classify output risk before choosing checks. Prefer schemas and deterministic validators for syntax, policy, calculations, and invariants; use tool-based verification for external facts/actions; use an evaluator model only for judgment that cannot be coded; require human approval for irreversible, high-impact, privileged, or ambiguous effects.

Keep generator and verifier inputs/criteria independent where feasible. A verifier must be able to reject, explain, and route failure into a bounded repair path. Record evidence, validator version, result, and approval identity.
