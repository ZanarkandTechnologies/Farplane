---
template_id: skill-template
template_version: "0.4.1"
feature_refs:
  - FEAT-0022
  - FEAT-0054
  - FEAT-0057
  - FEAT-0062
consumer_scope: skill
applies_to:
  - skills/*/SKILL.md
surface_fields:
  eval: supported
  qa_checklist: supported
  skill_ui: supported
  workflow: optional
---

---
name: {skill_name}
description: "[TODO: Verb input/context into output/artifact when call-condition; <=220 chars.]"
tier: [TODO: 1 | 2 | 3]
source: local
template_uses:
  skill-template: "0.4.0"
  # Add only after the skill fits 10 top-level todos, 5 QA checklist items,
  # and 5 eval tasks.
  # skill-surface-budget: "0.1.0"
# Tier 3 only: back-office | sales | deals | marketing | operations |
# intelligence | customer. See rules/skill-departments.toml.
group: [TODO: canonical department required for Tier 3]
# Optional. Each method is a child contract; the parent signature owns shared
# inputs, gates, state, and evidence.
methods:
  - id: {skill_name}:{method_name}
    class: artifact # artifact | integration | internal
    output: {one-named-output}
allowed-tools: {tools}
---

# {skill_title}

## Context

[TODO: Only context needed every time this skill loads: tier/system placement,
source-of-truth docs, ownership constraints, and assumptions.]

[TODO: First-load sufficiency has priority over modular neatness. Keep required
trigger, context, gates, routing, proof, and output contracts in `SKILL.md`; move
only conditional detail to references.]

[TODO: Follow `docs/skills/composition.md`. Name the one primary output this
skill owns, its next owner, and the work it must not duplicate. A durable
planner's primary output is the canonical ticket; put its child-action graph in
the ticket's `Change Plan`, not in a parallel plan artifact.]

[TODO: Place content by access frequency and owner scope: always-needed rules in
`SKILL.md`, one-skill conditional detail in `references/*`, and cross-skill
standards in `docs/*`.]

[TODO: For long or complex skills, use
`../skill-maintenance/qa_checklist.md`: keep detail in first load only when
defer_loading_risk is greater than context_rot_risk plus
compaction_loss_risk.]

[TODO: Add `qa_checklist.md` at the skill package root only when the skill has
repeatable runtime guardrails that should be read before execution as
preflight constraints and applied again at finish. Keep it Markdown until a
runner or renderer needs stricter structure.]

[TODO: Do not add a generic `## Job`; put ordered work in `## Todo List` as
visible task labels like `- [ ] 1. ...`, and use a specific contract section
only when it adds non-duplicated durable shape.]

[TODO: For skills enrolled in `skill-surface-budget`, keep this first-load todo
list to 10 top-level items or fewer. Use `consolidate(..., structure = skill)`
through `skill-maintenance.refine_skill` before adding item 11.]

[TODO: Paths in this skill are relative to this skill package. Use
`scripts/foo.py` and `references/foo.md` for nearby files.]

## Skill Signature

[TODO: Keep this when it clarifies callable behavior, required inputs, state,
gates, routes, or failure modes. Delete it only for tiny skills where the todo
list already makes composition obvious. See
`docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md`.]

```text
{skill_function}(input_text, state?) -> primary_output + evidence?
state: reads(...); writes(...); remembers(...)
owns: one named artifact or verdict
gates: proof_condition; finish_gate; blocker_condition
routes: next-skill | next-skill:method | direct-answer
fails: known bad behavior; overbroad behavior; misplaced ownership
```

[TODO: Add a compact budget type only when effort, search breadth,
finish-gate depth, delegation, or external compute materially changes the
workflow. Delete this section for tiny or deterministic skills.]

```text
{SkillBudget} = {
  grounding?: "none" | "skim" | "targeted" | "deep",
  search?: "direct" | "limited" | "broad",
  compute?: "single-agent" | "parallel-subagents" | "council",
  finish_gate?: "self-check" | "checklist" | "validator" | "eval" | "QA" | "review" | "demo" | "human-feedback"
}
```

When a caller invokes this skill without required inputs, the agent should
resolve the missing parameters before execution:

```text
resolve_skill_params(skill_signature, user_request, state)
  -> bound_inputs | setup_workflow | blocking_question
```

Use local files, task artifacts, setup workflows, or a narrow blocking question
to bind missing inputs. Do not run the skill against guessed parameters when the
signature makes those parameters required for correctness.

## Phase Boundary

[TODO: Keep this section when the skill may call phase-like skills such as
`plan`, `review`, `eval`, or `research`. Delete it for tiny skills where the
rule is obvious.]

Tier 0 is inherited, not a leaf-skill todo. Call `plan`, `review`, `eval`, or
another workflow skill only when that phase needs its own artifact, explicit
budget, handoff, independent judgment, or proof surface.

Externalized phase calls must shrink or specialize the current scope:

```text
externalize_phase(parent_task, phase, child_scope, budget)
  -> skill_call | inline_phase
```

Do not call phase-like skills recursively at the same scope.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Route the request or return its exact blocker.
- [ ] 2. Bind required inputs and select the one applicable domain branch.
- [ ] 3. Produce this skill's named primary artifact or delivery.
- [ ] 4. Apply only this skill's domain-specific gate.
- [ ] 5. Return the artifact, evidence, and one next owner.

[TODO: Keep five top-level domain nodes by default. A sixth needs a separate
owned artifact or a real independent branch. Do not repeat Tier 0 lifecycle
steps, generic QA preflight/finish language, ticket writeback, or another
skill's implementation work here. Route conditional/provider detail through a
precise reference load condition.]
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [TODO: Inline one short positive example. For prompt-heavy or
  quality-dependent skills, use
  `docs/skills/templates/GOLDEN_EXAMPLE.md` to add one compact
  `examples/golden/<case>.md`; load it conditionally with QA and calibrate from
  invariants rather than copied facts or wording. For other reference assets,
  accepted outputs, or comparison gates, add `examples/<slug>/example.md` plus
  optional `examples/<slug>/assets/*`.
  Use `templates/*` or `prompts/*` when the reusable asset is a prompt,
  packet, or generated artifact shape.]
- [TODO: If this skill needs a focused behavioral eval, add
  `evals/evals.json` in the skill package using the Agent Skills eval object
  schema.]
- [TODO: For material creation or structure changes, add a skill-local audit
  record under `audits/YYYY-MM-DD-<short-change>.md` using
  `../skill-maintenance/templates/skill-audit.md`. Do not add numeric
  `health_score` or `last_edited` frontmatter to `SKILL.md`.]
- [TODO: For skills with a long finish checklist, put it in
  `references/*-checklist.md` and load it only at the finish gate.]

## Gotchas

- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]

## Reference Map

- [TODO: `references/name.md` - read only when ...]

## Output

- [TODO: Expected artifact, type, path, or response shape.]
