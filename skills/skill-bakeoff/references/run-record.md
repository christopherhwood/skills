# Run record

Keep a compact record in the evaluation workspace. Plain text or JSON is sufficient; no harness is required. Reuse existing tools when they meet the experiment's needs. Add a helper only for an observed repeated or fragile operation, and evaluate its benefit independently.

Record before execution:

- Decision, candidate labels, exact file snapshots/hashes, intended treatment, and baseline.
- Creation task (if applicable), ordered downstream prompts, raw input provenance/completeness, and source-time skill inventory.
- Model/settings, tools, permissions, budgets, isolation method, repetitions, and known uncontrolled variables.
- Case-specific success criteria from user goals and corrections; record the agreed transfer/regression scope. Keep evaluator-only criteria and baseline answers outside worker inputs.

Keep per-arm artifacts:

- Generated skills, responses by turn, rendered outputs, and checks actually performed.
- Tool errors, missing inputs, deviations, skipped follow-ups, and observed cost/time.
- Helper checks and their inputs/results, separately from task-quality judgments.

Review after execution:

| Case | Anonymous arm | Evidence/artifact | Improvement or failure | Severity/uncertainty |
| --- | --- | --- | --- | --- |

Retain the blind review and reveal the mapping only after judgment. Summarize the candidate differences, structural results, downstream observations, helper reliability, transfer/regression outcomes, and selection rationale. State which checks were not run and what the sample cannot establish. Keep private transcripts and run outputs out of distributable skills.

For example, comparing long, short, and short-plus-helper creators requires three creation arms followed by matched tasks using each generated skill set. A manual-skill arm or no-skill arm is a separate baseline only if it serves the stated decision; do not substitute an older unmatched run.

## Review boundaries

For two-stage creator trials, keep the objects being judged separate:

| Review | Supply | Withhold |
| --- | --- | --- |
| Downstream behavior | Task, criteria, anonymous answers and their actual artifacts | Generated skills/resources, creator instructions, candidate mapping, prior verdicts |
| Created skills | Creation request, raw source, source-time inventory, anonymous generated skill files/resources | Creator instructions and candidate mapping |

Freeze the downstream review before releasing the creation packet. Prefer a separate creation reviewer when useful; if reusing one, disclose carryover and preserve the earlier judgment. Keep treatment-revealing paths and notes out of packets. A result artifact is not automatically safe for every review: a generated skill is an artifact in stage one but generating instructions in stage two.
