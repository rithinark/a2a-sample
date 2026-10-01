# Evaluation

Define success before optimization: task outcome, safety, correctness, grounding, latency, cost, and human burden. Build scenario sets for normal, edge, tool-failure, malformed-output, adversarial-input, budget-limit, and regression cases. Grade deterministic properties deterministically; use calibrated model graders only for subjective criteria and spot-check them with humans.

Report pass rate by slice, confidence intervals where meaningful, cost/latency distributions, and failure taxonomy. Freeze representative traces as regression fixtures; do not judge only polished demos.
