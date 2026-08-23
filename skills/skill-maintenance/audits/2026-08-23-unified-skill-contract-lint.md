---
skill: skill-maintenance
date: 2026-08-23
change_type: maintenance
owner: skill-maintenance
status: pass
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
  `ensemble.yaml` through one package lint. `farplane validate skills` runs
  that lint first, then writes the registry and regenerates skill and harness
  graph outputs.
- Why: one package lint should not require every skill invocation to load a
  persona council; nested persona names must never leak into skill discovery or
  plugin names.
- Tradeoff accepted: package metadata remains physically split, but the
  ensemble file is opened only for `ensemble=auto|max` or validation.

## Contract

```text
SKILL.md frontmatter + ensemble.yaml?
  -> typed skill identity + capability? + optional personas
  -> farplane lint skills (read-only)
  -> farplane validate skills: registry write -> skill graph -> harness graph
```

The direct path remains the default. `ensemble=auto` opens the optional sidecar
and selects three relevant personas; `ensemble=max` uses all declared personas.

## Proof Required

| Check | Verdict | Evidence |
| --- | --- | --- |
| One parser for skill metadata | pass | `skill_contract.py`, registry, graph-doc, and plugin discovery use the shared parser. |
| Complete persona validation | pass | 5 optional sidecars / 23 personas from `check_skill_frontmatter.py`. |
| Progressive persona loading | pass | `SKILL.md` remains minimal; persona prompts stay in sidecars. |
| Validation refresh order | pass | `farplane validate skills` passed in order: lint, registry write, skill graph, harness graph; `--check` then confirmed freshness without writes. |
| Plugin discovery remains correct | pass | nested-persona regression test and `sync_skill_plugins.py --check`. |
| Independent review | pass | Rerun TAS-A reviewed the progressive-sidecar implementation, CLI boundary, generated outputs, and focused proof. |

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

The earlier eager-frontmatter receipt is superseded. A 2026-08-23 rerun issued
**TAS-A / pass** for the progressive-sidecar layout: pure `farplane lint
skills`, ordered `farplane validate skills` refresh, a passing `--check` run,
and no persona IDs or prompts in generated skill docs, graphs, registry, or
plugin outputs.
