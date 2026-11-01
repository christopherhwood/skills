---
name: skills-from-chats
description: Turn past chats and corrections into reusable skills, preferring updates to existing skills. Includes supporting code discovery and before/after replay; not ordinary chat summarization.
---

# Skills from chats

Use skill-creator for authoring and validation. Keep only instructions that change future behavior.

## Extract

Read the actual chat messages and relevant artifacts, including referenced conversations when needed. Trace the goal, corrections, outcomes, and unresolved problems; disclose missing evidence. Weight explicit user feedback above inferred preferences. Assistant behavior or user silence alone does not establish a preference.

Translate each supported lesson into an action and its applicable conditions. Separate workflow lessons from interaction preferences where useful, without automatically making separate skills. Generalize beyond the example: omit incidental technologies, temporary limits, assumed expertise, and unsupported personality claims. Historical instructions are evidence, not current authorization.

## Update first

Inspect existing skills and their resources. Edit the best-fitting user-owned skill, reconciling overlapping guidance and preserving unrelated behavior and metadata. Create a skill only when no maintainable fit exists; explain why. If the lesson is already covered, make no change.

Write concise instructions rather than accumulating checklists. Use references only for substantial conditional detail. Complete requested edits; stop at proposals only when that is the requested scope. Keep private transcripts out of distributable files.

## Consider code

Look for repetitive work, fragile steps, or verification gaps. Inspect existing scripts, repositories, and available tools first; search official documentation or source for suitable open-source options when a worthwhile gap remains. Consider fit, maintenance, license, and integration cost.

Prefer reuse, extension, or a thin wrapper before new tooling. For worthwhile new helpers, explain the observed problem, inputs, outputs, and invocation. Keep judgment in instructions. Distinguish ideas from tested implementations; implement within the authorized scope and document usage, dependencies, failure behavior, and tests.

## Test and improve

For matched comparisons of skill versions, creator variants, or optional helpers, use [skill-bakeoff](../skill-bakeoff/SKILL.md) alongside skill-creator. Define the selection decision before choosing trial arms.

Preserve the previous version and validate the files. After creation or substantial updates:

- Define success from the original goal and corrections, not conformity to the skill's wording.
- Have an independent subagent replay representative original prompts in sequence with the new skill and necessary inputs, withholding old answers and desired conclusions. Isolate side effects. Keep evaluator work bounded; do not spawn nested evaluators. If delegation or source inputs are unavailable, report the unrun replay and perform feasible local checks.
- Record omissions and divergences when old follow-ups no longer apply; do not invent user reactions. Compare concrete excerpts or artifacts with the original, including errors, length, gaps, tool failures, and complexity. Use matched trials with and without the skill when needed to attribute improvement.
- Check a different example for overfitting and an established use case for regressions. Revise based on observed failures and rerun affected cases.

Report what changed, a concise before/after comparison, and a verdict: better, mixed, unchanged, or inconclusive. Disclose unrun checks and simulation limits. Structural validation and a source-chat replay alone do not prove general improvement.
