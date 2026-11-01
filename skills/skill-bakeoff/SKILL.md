---
name: skill-bakeoff
description: Run matched behavioral evaluations of skill versions, creator workflows, or optional helpers to choose what to keep. Companion to skill-creator for substantive skill comparisons; not routine structural validation or general model benchmarking.
---

# Skill bakeoff

Use skill-creator for authoring and structural validation; use this skill for evidence about behavior. When creating from chats, pair it with skills-from-chats. Keep evaluation artifacts in the task workspace, outside installed skills. Do not install a winner merely because it wins a trial.

## Define the decision

State what the user is choosing and name the exact candidates before running anything. Distinguish **a skill versus no skill**, **manual versus generated skills**, and **alternative creator instructions**. These answer different questions. Resolve consequential ambiguity rather than substituting an easier comparison. When replaying an existing bakeoff, preserve its decision, candidates, and task set; use its evidence as the baseline, not its winner as the expected answer.

Freeze candidate files, raw inputs, tool availability, and success criteria. Record versions or hashes and the model/settings actually available. Use the same tasks, source-time skill inventory, permissions, tools, and budgets across arms except the intended treatment. For a helper arm, change only helper availability and necessary usage instructions; allow other arms ordinary tools unless explicitly testing a narrower constraint.

Use [the run record](references/run-record.md) to preserve enough evidence to reproduce the comparison. Scale the number of cases and repetitions to the decision; a small exploratory bakeoff need not become a benchmark project.

## Run the right experiment

Use fresh independent subagents for matched arms when available and authorized, with only their candidate, task, and necessary raw inputs. Keep their work in separate directories. Do not give them prior answers, other candidates, expected winners, or this conversation's conclusions. Keep model/settings matched; disclose inherited context or uncontrolled differences. Do not spawn nested evaluators: the coordinator owns all trial and review agents.

For creator comparisons, test two stages:

1. Each creator receives the same creation request, raw source material, and existing-skill inventory; it produces actual skill files and requested artifacts. Check retained behaviors, update-versus-create choices, overfitting, and useful tooling decisions.
2. Fresh agents apply each generated skill set to the same downstream tasks. Deliver multi-turn prompts sequentially, preserving each arm's own answers. Keep original assistant answers separate for later baseline comparison. Report when historical follow-ups no longer fit; do not invent user reactions.

A creator's output length or structural validity does not establish downstream usefulness. Likewise, a helper's robust file handling does not establish better reasoning. Test helpers separately on concrete failure cases such as truncated input and overwrite protection when those are relevant to their purpose.

Use bounded transfer and regression checks where they help the decision; do not automatically expand an agreed replay into a new benchmark. Label conceptual checks, simulations, and executed tasks distinctly. If execution is unavailable, report unrun cases rather than presenting proposed results as observations.

## Judge and decide

When independent review is available and authorized, supply anonymized artifacts, the task, and outcome-based criteria. Build separate review packets for downstream answers and generated skills using [the review boundaries](references/run-record.md). Freeze downstream judgments before exposing generating skill files; retain the candidate mapping with the coordinator. Otherwise label self-review and disclose the missing independent check.

Inspect visuals at their intended size and verify consequential factual differences against evidence. Record what was actually inspected. Blind labels reduce bias but do not guarantee anonymity.

Compare correctness, retained requirements, practical usability, omissions, and failures before brevity. Measure instruction length separately from output length; define exclusions. Record cost/time only when observed. Keep hard failures visible rather than burying them in an average score.

Report concrete differences, artifact links, limitations, and a verdict: better, mixed, unchanged, or inconclusive. Single-run preferences are observations, not causal proof or statistical significance. Repeat close or noisy cases when the decision warrants it. If revising a candidate, freeze a new version and rerun affected comparisons; do not mix results across versions.

Recommend the smallest version justified by the evidence. Preserve the user's choice about helpers and deployment. Selection, installation, committing, and publication remain separate actions governed by the current request.
