---
skill: frontend-craft
date: 2026-06-15
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/frontend-craft/SKILL.md
after_ref: skills/frontend-craft/SKILL.md
reasoning_basis: router_skill_identity
proof_artifacts:
  - skills/frontend-craft/SKILL.md
  - skills/skill-maintenance/qa_checklist.md
  - docs/skills/best-practices.md
eval_required: no
---

# Frontend Craft Router Shape Audit

## Change

- Before: `frontend-craft` worked as a useful frontend umbrella, but its first
  load read more like a reference document than an explicit callable workflow.
- After: `frontend-craft` declares itself as the general frontend entrypoint and
  router, adds a `frontend_craft(...)` signature, names state reads/writes,
  routes, failure modes, and phase boundaries, projects its executable program
  through the numbered `## Todo List`, promotes true gotchas into executable
  route/proof steps, and keeps detailed frontend doctrine in downstream skills,
  references, and `qa_checklist.md`.
- Why: the operator asked whether this should be a skill or a doc. The answer
  is that it should remain a skill only as a compact router; niche design,
  implementation, asset, and QA details should stay out of first load.
- Tradeoff accepted: the skill still carries a compact branch table and gotchas
  because routing is its job. It should not absorb the detailed rubrics owned by
  `functional-ui`, `visual-design`, `frontend-design`, `landing-page`,
  `web-design-guidelines`, `visual-qa`, or media skills.

## Structure Checklist

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names triggers, routing, proof expectations, outputs, and failure modes. |
| `reference_load_precision` | pass | Branch references are listed in the Reference Map and named from routing steps. |
| `missing_context_rate` | pass | Required routing and completion gates remain in first load. |
| `noisy_context_rate` | pass | The duplicate `Core Workflow` prose and first-load `Top Gotchas` block were removed; long QA checks remain in `qa_checklist.md`; detailed playbooks remain in references. |
| `duplicated_instruction_count` | pass | The executable workflow is represented once as `Todo List` steps, matching `docs/specs/program-notation.md`; high-risk gotchas are either step conditions or deferred reference detail. |
| `prompt_size_tokens` | pass | First-load stays under the checklist's rough 250-line warning threshold. |
| `maintenance_locality` | pass | Router identity lives in `SKILL.md`; niche checks live in owner references or downstream skills. |
| `composition_clarity` | pass | Signature names inputs, outputs, state, routes, and failure modes. |

## Proof

- Validation: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed after the structure update.
- Reviewer lane: skipped; this is an owner-local structure clarification with a
  self-check audit.
- Eval required: no; no eval behavior changed.
