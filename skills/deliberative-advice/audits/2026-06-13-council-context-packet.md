---
skill: deliberative-advice
date: 2026-06-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/deliberative-advice/SKILL.md
after_ref: skills/deliberative-advice/SKILL.md
reasoning_basis: harness-advisor
proof_artifacts:
  - skills/deliberative-advice/SKILL.md
  - skills/deliberative-advice/references/llm-council-model.md
  - skills/deliberative-advice/eval_task.json
  - docs/specs/context-and-handoff-policy.md
eval_required: yes
---

# Council Context Packet Audit

## Change

- Before: council mode asked lanes to share the same decision, criteria,
  evidence packet, and output shape, but did not require the evidence packet to
  exist as a durable artifact before subagents were spawned.
- After: `advise:council` requires a Council Context Packet when prior
  discussion, options, evidence, or constraints matter, and every lane receives
  the packet path plus its lane-specific brief.
- Why: independent lanes lose value when their prompt is a thin summary of a
  long discussion.
- Tradeoff accepted: council mode pays one artifact-writing step before
  spawning lanes.

## First-Principles Reasoning

- Objective: preserve rich decision context across isolated subagent lanes.
- Placement logic: `deliberative-advice` owns council procedure; global and
  agent prompts own generic subagent handoff expectations.
- Expected behavior delta: material council calls produce or reuse a
  `context_ref` before first-pass recommendations.
- Proof needed: skill validation, JSON eval validity, and structure self-check.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` now requires the packet before spawning lanes. |
| `reference_load_precision` | pass | Detailed packet mechanics live in `references/llm-council-model.md`. |
| `missing_context_rate` | pass | Required packet fields are listed in first load. |
| `noisy_context_rate` | pass | Long template detail stays in the reference. |
| `duplicated_instruction_count` | pass | Global rule covers all subagents; this skill covers council-specific behavior. |
| `prompt_size_tokens` | pass | First load adds the gate without copying a full example transcript. |
| `task_success_rate` | unknown | A live eval run was not performed in this pass. |
| `review_tas_rate` | unknown | No reviewer lane was used for this narrow self-check. |
| `maintenance_locality` | pass | Council behavior remains in the `deliberative-advice` package. |
| `composition_clarity` | pass | The context packet path is the shared input to all lanes. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/deliberative-advice/eval_task.json`.
- Structure evals, when needed: not run.
- Reviewer receipt: not required for this narrow self-check.
- Validator: pending command result in final work summary.
- Eval required: yes, as a regression task.
- Evidence gaps: no live council run proved the new behavior yet.

## Before Behavior

- Agents could spawn council lanes from thin prompts after a long discussion.

## After Behavior

- Council mode must package the decision frame into a durable context packet or
  identify an existing one before subagent fanout.

## Followups

- Run a real council-mode behavior test after the next substantial council
  decision to confirm lane prompts use the packet path.
