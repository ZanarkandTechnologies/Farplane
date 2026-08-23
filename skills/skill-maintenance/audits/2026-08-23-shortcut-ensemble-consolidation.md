---
skill: skill-maintenance
date: 2026-08-23
change_type: consolidation
owner: skill-maintenance
status: pass
review_route: reviewer
reasoning_basis: local_contracts
proof_artifacts:
  - tickets/TASK-9028/ticket.md
eval_required: no
---

# Shortcut And Ensemble Consolidation

## Decision

Retire the unused Deep Interview and Skill Registry UI shortcuts. Replace
Reshape Feasible with the strategic `feasible-roadmap` shortcut; replace
Commit Message with staged-only `commit`. Retire the generic budget router and
Deliberative Advice wrapper in favor of owner-local `ensemble.yaml` files.

## Contract

```text
skill(input, context?, ensemble?: auto | max) -> normal_output + dissent?

omitted -> direct path
auto    -> exactly 3 relevant, diverse local personas
max     -> every local persona
```

The shared typed parser validates all five ensemble packages. Child calls do
not inherit ensemble mode. `lean-check` is a shortcut, but its non-projected
classification does not weaken the system policy that requires it before code
changes.

## Preservation

- Retired budget and deliberative audits live under `audits/retired/`.
- Historical ledgers remain untouched.
- Commit does not stage or push; its temporary-repository tests prove no staged
  change is a no-op and unstaged work survives a staged commit.

## Proof

- `python3 bin/validators/check_skill_ensembles.py`
- `python3 skills/commit/scripts/test_commit_staged.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `python3 skills/skill-maintenance/scripts/sync_skill_plugins.py --check`
- focused frontmatter, gate, registry, runtime, and commit tests
- active-source stale-reference scan with historical and generated exclusions

## Review Receipt

2026-08-23 reviewer re-review: **TAS-A / pass** across `skill-contract`,
`integration-readiness`, `evidence-quality`, and `code-quality`. It confirmed
the broader underscore/hyphen retired-name scan is clean, generated discovery
omits retired packages, historic audits are preserved, and the only failing
aggregate frontmatter check is unrelated stale `TASK-0441` source references
in `FEAT-0075` and `FEAT-0079`.
