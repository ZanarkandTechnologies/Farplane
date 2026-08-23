---
skill: product-backbrief
date: 2026-08-23
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/product-backbrief/SKILL.md
after_ref: skills/product-backbrief/SKILL.md
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# Shortcut Capability Classification

## Change

- Before: `product-backbrief` had no static capability classification.
- After: it declares `capability.kind: shortcut`.
- Why: it is an explicit, read-only operator alignment command that produces no
  capability-map artifact or system-boundary contract.
- Tradeoff accepted: the package remains excluded from automatic composition
  and the Capability Map; its explicit invocation remains discoverable through
  its skill package, registry, and `farplane-shortcuts` plugin projection.

## Classification Basis

`shortcut` means an explicit-only operator command with no Capability Map
projection. It is not a generic label for every skill a person can invoke.

| Candidate | Verdict | Evidence |
| --- | --- | --- |
| `product-backbrief` | tag shortcut | Read-only alignment workflow; writes none; routes only after human correction. |
| `advise`, `brainstorm`, `diagramming`, `task-recap` | already tagged | Current frontmatter declares `capability.kind: shortcut`. |
| `commit-message`, `deep-interview`, `deliberative-advice`, `problem-framing`, `reshape-feasible`, `skill-registry-ui`, `unslop` | already tagged | Current frontmatter declares `capability.kind: shortcut`. |
| `intelligest` | keep core | Explicit phrasing alone is insufficient; it owns a durable intelligence dossier workflow. |
| `phone-chaser` | keep integration | It performs an external system-boundary action. |

## Proof Artifacts

- Validator: `python3 bin/farplane.py validate frontmatter skills` passed with
  `shortcut=12`.
- Registry/plugin projection: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  and `python3 skills/skill-maintenance/scripts/sync_skill_plugins.py --check`
  passed.
- Focused tests: 34 tests passed across skill-frontmatter, registry, and plugin
  projection suites.
- Reviewer receipt: pending.

## Reviewer Receipt — 2026-08-23 Product Backbrief Shortcut Classification

TAS-A / pass. `product-backbrief` is correctly classified as
`capability.kind: shortcut`: it is read-only, writes no artifact, has no
system-boundary integration contract, and documents downstream requirements or
implementation-planning handoff as operator-confirmed rather than automatic
composition. Its generated registry projection has no `skill_links`,
`todo_skill_refs`, or `common_chains`. Narrow validators and focused tests
passed.

## Followups

- None. Future classifications use the same explicit-only, no-projection rule.
