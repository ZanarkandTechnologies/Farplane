---
skill: skill-maintenance
date: 2026-08-23
change_type: maintenance
owner: skill-maintenance
status: draft
review_route: reviewer
before_ref: separate frontmatter and ensemble validator commands
after_ref: one package lint with optional progressive ensemble sidecars
reasoning_basis: first_principles
proof_artifacts:
  - python3 bin/farplane.py lint all --json
  - python3 skills/skill-maintenance/scripts/sync_skill_plugins.py --check
  - focused unittest contract and projection suite
eval_required: no
---

# Unified Skill Contract Lint

## Change

- Before: skill metadata and optional persona files had separate validator
  commands. Some renderers parsed skill frontmatter independently.
- After: `farplane lint skills` validates each `SKILL.md` plus any optional
  `ensemble.yaml` through one package lint, writes the registry, and regenerates
  skill and harness graph outputs.
- Why: one package lint should not require every skill invocation to load a
  persona council; nested persona names must never leak into skill discovery or
  plugin names.
- Tradeoff accepted: package metadata remains physically split, but the
  ensemble file is opened only for `ensemble=auto|max` or validation.

## Contract

```text
SKILL.md frontmatter + ensemble.yaml?
  -> typed skill identity + capability? + optional personas
  -> skill contract lint
  -> registry write -> skill graph -> harness graph
```

The direct path remains the default. `ensemble=auto` opens the optional sidecar
and selects three relevant personas; `ensemble=max` uses all declared personas.

## Proof Required

| Check | Verdict | Evidence |
| --- | --- | --- |
| One parser for skill metadata | pass | `skill_contract.py`, registry, graph-doc, and plugin discovery use the shared parser. |
| Complete persona validation | pass | 5 optional sidecars / 23 personas from `check_skill_frontmatter.py`. |
| Progressive persona loading | pass | `SKILL.md` remains minimal; persona prompts stay in sidecars. |
| Lint refresh order | pass | `farplane lint all --json` reports contract, registry, skill graph, then harness graph. |
| Plugin discovery remains correct | pass | nested-persona regression test and `sync_skill_plugins.py --check`. |
| Independent review | pending | The earlier TAS-A reviewed the superseded eager-frontmatter version; rerun is required for the progressive-sidecar correction. |

## Scope

- `bin/core/skill_contract.py`
- `bin/core/farplane_lint.py`
- `bin/validators/check_skill_frontmatter.py`
- the five ensemble-owning packages
- skill registry/graph/plugin parser and focused tests

## Non-Goals

- No generic persona router, budget type, or graph persona nodes.
- No change to the concurrently renamed `deep-system-design` package.

## Review Receipt

The 2026-08-23 TAS-A receipt applies only to the superseded eager-frontmatter
implementation. Re-run independent review against this progressive-sidecar
layout before marking the audit passed.
