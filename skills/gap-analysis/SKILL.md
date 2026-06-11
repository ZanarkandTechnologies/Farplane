---
name: gap-analysis
description: "Turn current-vs-expected behavior evidence into a grounded GapReport with missing pieces, owner surface, and proof path."
tier: 2
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0053
methods:
  - gap-analysis:skill
  - gap-analysis:harness
  - gap-analysis:ui
  - gap-analysis:feature
allowed-tools: Read, Glob, Grep, Bash
---

# Gap Analysis

## Context

Use this skill when the operator wants to compare any existing Farplane surface
with an intended behavior, diagnose why it does not yet produce that behavior,
or stop rewriting the same "what is missing here?" prompt by hand.

This skill is a diagnostic interface, not the improvement loop itself:

```text
gap_analysis(target, expected_behavior?, evidence?) -> GapReport + next_owner
```

The output should make the target easier to improve by naming the current
contract, desired behavior, missing inputs and outputs, missing proof or evals,
and smallest next owner for remediation.

## Skill Signature

```text
gap_analysis(target, expected_behavior?, evidence?) -> gap_report + next_owner
state: reads(target_artifact, relevant_context, supplied_evidence); writes(gap_report?)
gates: current_state:grounded; expected_behavior:explicit_or_marked_unknown; owner_surface:named
routes: harness-advisor | eval | self-improve | skill-maintenance | impl-plan | functional-ui | research:gap | direct-fix
fails: jumps to a fix before naming the gap; confuses symptom with owner; invents expected behavior; creates duplicate skills
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the target surface, intended behavior, method address when
  useful, and expected signature before inspecting files.
- [ ] 2. Ground the current contract with [reference-grounding](../reference-grounding/SKILL.md):
  read the target file or package, nearby docs, direct todo list when present,
  relevant references, scripts, templates, examples, existing evals, and any
  local improvement memory.
- [ ] 3. Compare current versus intended behavior across the gap matrix:
  trigger, inputs, state/files read, outputs, artifacts written, proof/evals,
  composition points, failure modes, and owner boundaries.
- [ ] 4. Classify each gap as `missing`, `weak`, `ambiguous`, `overbroad`,
  `misplaced`, or `covered`; mark severity as `blocker`, `important`, or
  `nice-to-have`.
- [ ] 5. Choose the next owner.
  - [ ] 1. Target surface edit.
  - [ ] 2. Eval task, hardcase metadata, or fixture.
  - [ ] 3. Skill-local self-improvement memory.
  - [ ] 4. Skill-maintenance pass.
  - [ ] 5. Harness placement decision.
  - [ ] 6. Deliberative advice only when remediation is high-stakes,
    expensive, or materially branching.
- [ ] 6. Review the gap report before returning it: every recommendation should
  point to local evidence, an owning surface, and a verification path.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Return or write a compact GapReport:

```markdown
## Gap Report

Target:
Intended behavior: ...
Signature:
`surface_action(inputs, state?) -> outputs + artifacts + evidence`

### Current Contract
- Trigger:
- Inputs:
- Outputs:
- Proof:

### Gaps
| Area | Status | Severity | Evidence | Fix owner |
| --- | --- | --- | --- | --- |

### Recommendation
Recommended next owner: ...
Why this owner: ...
Verification: ...
```

## Gotchas

- Use this skill before editing when the target behavior is fuzzy.
- Use the target surface directly when the user already named the exact edit and
  no gap diagnosis is needed.
- Use `self-improve` after this report only when the next step is a measured
  improvement loop with a metric, baseline, candidates, and result memory.
- Use `harness-advisor` after this report when the fix may belong outside the
  target surface.
- Use `deliberative-advice` only when the remediation choice itself needs
  independent perspectives and visible dissent.
- Do not mark `expected_behavior` as known when the operator only supplied an
  observation. Preserve the uncertainty and route to product or research
  grounding when needed.

## Reference Map

- [docs/skills/system.md](../../docs/skills/system.md) - tier model, todo-link
  rules, source ownership, and feature tracking.
- [docs/skills/best-practices.md](../../docs/skills/best-practices.md) -
  first-load contract quality, skill signatures, and reference placement.
- [docs/specs/self-improvement-contracts.md](../../docs/specs/self-improvement-contracts.md) -
  compact signature grammar and self-improvement workflow contracts.
- [reference-grounding](../reference-grounding/SKILL.md) - required evidence
  primitive for local files.
- [advise](../advise/SKILL.md) - use only when the gap report exposes real
  remediation options and a recommendation is needed.
- [harness-advisor](../harness-advisor/SKILL.md) - use when the fix may belong
  outside the inspected target surface.
- [eval](../eval/SKILL.md) - use when the gap should become a repeatable proof
  case or hardcase-marked eval.

## Output

Prefer writing the report to the active ticket or a relevant experiment/spec
when it will be reused. A concise chat report is fine when the operator only
needs a quick diagnostic answer.

Return:

- `Target`
- `Intended behavior`
- `Signature`
- `Current Contract`
- `Gaps`
- `Recommendation`
- `Verification`

Gap matrix dimensions:

Check these dimensions every time:

```text
current_contract(skill) -> triggers + todo_path + inputs + outputs + proof
intended_contract(behavior) -> required_signature + expected_artifacts + reward
gap(current, intended) -> missing/weak/ambiguous/overbroad/misplaced/covered
remediate(gap) -> owner_surface + verification
```

Common skill gaps:

- Trigger gap: description does not fire for the user wording.
- Input gap: the skill does not ask for or infer the variables it needs.
- Output gap: the skill returns prose when a durable artifact or structured
  report is needed.
- Proof gap: no eval, fixture, command, or review path proves the behavior.
- Composition gap: the skill should call a lower-level primitive or hand off to
  a higher-level workflow but does not say when.
- Placement gap: the requested rule belongs in a template, doc, validator,
  ticket contract, or agent prompt instead of the skill.
