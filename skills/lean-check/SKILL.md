---
name: lean-check
description: "Turn a suspected overbuilt change or plan into a first-sufficient-rung verdict, evidence, and smallest safe next action."
tier: 2
source: local
template_uses:
  skill-template: "0.4.0"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.1"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep
---

# Lean Check

## Context

`lean-check` is the reusable first-sufficient-rung judgment for a proposed
implementation or plan. Use it before adding code when the request may be
speculative, duplicate local behavior, or introduce an unnecessary library or
surface. It owns the leanness decision and receipt; it does not implement the
change or replace correctness, safety, accessibility, or proof requirements.

`impl-plan` calls this skill after repository inspection and context resolution.
Direct coding work may call it without a ticket. Use `review` only when the
result needs a TAS verdict; use `desloppify` only when an accepted cleanup must
be executed through its CLI loop.

## Skill Signature

```text
lean_check(target, local_evidence?, proposed_change?) -> lean_receipt
state: reads(current need, local code/tests/docs, standard or platform options,
  installed dependencies); writes(no files by default)
owns: first-sufficient-rung verdict and smallest safe next action
gates: current_need_named; first_sufficient_rung_named; evidence_named;
  proof_preserved
routes: impl-plan | review | desloppify | direct implementation
fails: speculative build; duplicate owner; new dependency before reuse;
  line-count optimization that removes required proof or safety
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read [qa_checklist.md](qa_checklist.md), then name the target, current
  need, and proposed new surface.
- [ ] 2. Inspect only enough local evidence to test the ladder: nearby
  implementation, tests, docs, platform, and installed dependencies.
- [ ] 3. Stop at the first sufficient rung.
  - [ ] `skip`: no current need; defer speculative work.
  - [ ] `reuse_local`: an existing helper, utility, component, or pattern fits.
  - [ ] `standard_library`: the language/runtime already provides it.
  - [ ] `native_platform`: a browser, OS, or platform primitive covers it.
  - [ ] `installed_dependency`: an already-present dependency covers it.
  - [ ] `inline`: one local expression is clearer than a new abstraction.
  - [ ] `minimum_new_code`: only no earlier rung is sufficient.
- [ ] 4. State the smallest safe next action and what evidence would overturn it.
- [ ] 5. Apply [qa_checklist.md](qa_checklist.md) to the receipt, then return
  it; route a material plan to `impl-plan` and a judgment-heavy acceptance
  question to `review` with `debloatability` or `code-quality` as applicable.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Receipt shape:

```yaml
target:
current_need:
rung: skip | reuse_local | standard_library | native_platform | installed_dependency | inline | minimum_new_code
evidence: []
smallest_next_action:
proof_preserved:
review_route: none | review:<rubric-family>
```

Example: a request for a date-picker library selects `native_platform` when
the required behavior fits `<input type="date">`; the next action is to use the
native control and keep the existing form validation proof.

## Gotchas

- Do not continue down the ladder after finding a sufficient rung.
- Do not call a smaller diff lean when it removes a necessary test, safety
  check, accessibility behavior, migration, or proof artifact.
- Do not invent a numeric leanness score; return the specific rung and evidence.

## Reference Map

- [Impl Plan](../impl-plan/SKILL.md) - use when the receipt changes a material
  ticket's implementation boundary.
- [Review](../review/SKILL.md) - use only when a TAS judgment is required.
- [Desloppify](../desloppify/SKILL.md) - use only for an accepted cleanup CLI
  execution loop.

## Output

- One `lean_receipt` with the first sufficient rung, local evidence, smallest
  next action, proof-preservation statement, and optional review route.
