# Codexter Policy Index

Purpose: provide one convenient policy map without turning policy into another
duplicated source of truth.

This folder answers:

- where does a rule live?
- which surface owns the current behavior?
- which memory entry explains why the rule exists?
- which validator or review loop checks drift?

## Ownership Model

| Policy kind | Canonical owner | Use this index for |
| --- | --- | --- |
| Active repo routing | [`AGENTS.md`](/Users/kenjipcx/coding-harness/Codexter/AGENTS.md) | Find the current Codexter-local rule quickly |
| Installed global behavior | [`templates/global/AGENTS.md`](/Users/kenjipcx/coding-harness/Codexter/templates/global/AGENTS.md) | Check what `install.sh` ships into `~/.codex/AGENTS.md` |
| Durable invariants | [`docs/MEMORY.md`](/Users/kenjipcx/coding-harness/Codexter/docs/MEMORY.md) | Find the `MEM-####` reason behind a rule |
| Repeated misses | [`docs/TROUBLES.md`](/Users/kenjipcx/coding-harness/Codexter/docs/TROUBLES.md) | See why a rule may need promotion |
| System contracts | [`docs/specs/`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/README.md) | Read the detailed model or contract |
| Skill workflows | [`docs/skills/README.md`](/Users/kenjipcx/coding-harness/Codexter/docs/skills/README.md) and [`skills/*/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills) | Locate executable workflow policy |
| Feature provenance | [`docs/features/registry.jsonl`](/Users/kenjipcx/coding-harness/Codexter/docs/features/registry.jsonl) | Dedupe new harness ideas against existing features |
| Source provenance | [`docs/sources/registry.jsonl`](/Users/kenjipcx/coding-harness/Codexter/docs/sources/registry.jsonl) | Dedupe outside sources before adopting ideas |
| Ticket execution policy | [`tickets/README.md`](/Users/kenjipcx/coding-harness/Codexter/tickets/README.md) and [`tickets/templates/ticket.md`](/Users/kenjipcx/coding-harness/Codexter/tickets/templates/ticket.md) | Check task state, proof, and lifecycle rules |

## Current Policy Clusters

### Documentation Ownership

- Governance: [`docs/specs/doc-governance.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/doc-governance.md)
- Duplicate audit: [`docs/policies/duplication-audit.md`](/Users/kenjipcx/coding-harness/Codexter/docs/policies/duplication-audit.md)
- Canonical spec index: [`docs/specs/README.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/README.md)
- Durable rules: `MEM-0013`, `MEM-0071`, `MEM-0108`
- Drift check: prefer canonical-owner docs plus compatibility pointers over
  parallel copies of the same doctrine.

### Harness Placement

- Canonical doctrine: [`docs/specs/harness-engineering-doctrine.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/harness-engineering-doctrine.md)
- Advisor workflow: [`skills/harness-advisor/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/harness-advisor/SKILL.md)
- Durable rule: `MEM-0106`
- Drift check: use `harness-advisor` before expanding root policy, global
  templates, skills, subagents, hooks, validators, registries, or ticket
  contracts.

### First-Principles Planning

- Canonical contract: [`docs/specs/first-principles-planning.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/first-principles-planning.md)
- Consuming workflows: [`skills/prd/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/prd/SKILL.md), [`skills/spec-to-ticket/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/spec-to-ticket/SKILL.md), [`skills/impl-plan/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/impl-plan/SKILL.md)
- Drift check: PRDs, tickets, and implementation plans should preserve
  objective, need, assumptions, root cause, constraints, first viable slice,
  proof, tradeoffs, and non-goals before execution.
- Advisory use: [`skills/advise/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/advise/SKILL.md)
  uses the same basis before comparing options and recommending a path.

### Skill System

- Skill registry contract: [`docs/skills/README.md`](/Users/kenjipcx/coding-harness/Codexter/docs/skills/README.md)
- Maintenance workflow: [`skills/skill-maintenance/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/skill-maintenance/SKILL.md)
- Generated registry: [`docs/skills/registry.jsonl`](/Users/kenjipcx/coding-harness/Codexter/docs/skills/registry.jsonl)
- Durable rules: `MEM-0098`, `MEM-0099`, `MEM-0100`, `MEM-0103`, `MEM-0104`
- Drift check: `python3 skills/skill-maintenance/scripts/check_skills.py --write`

Why `skill-maintenance` is a skill: it is an executable upkeep workflow with
ordered reads, edits, registry regeneration, and validation. A skill is the
right shape because agents must do the same maintenance sequence repeatedly.
The policies inside it are skill-system policies, not the whole harness policy
library.

### External Skill Boundaries

- Policy surfaces: [`AGENTS.md`](/Users/kenjipcx/coding-harness/Codexter/AGENTS.md), [`templates/global/AGENTS.md`](/Users/kenjipcx/coding-harness/Codexter/templates/global/AGENTS.md), [`docs/skills/README.md`](/Users/kenjipcx/coding-harness/Codexter/docs/skills/README.md)
- Self-healing contract: [`docs/specs/skill-self-healing.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/skill-self-healing.md)
- Durable rules: `MEM-0073`, `MEM-0103`, `MEM-0107`
- Drift check: self-healing may mirror external skills and create repair
  tickets, but must not directly edit installed or external skill bodies unless
  the operator explicitly requests that specific edit.

### Tickets, Proof, And Review

- Ticket contract: [`tickets/README.md`](/Users/kenjipcx/coding-harness/Codexter/tickets/README.md)
- Review gates: [`docs/specs/review-gates.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/review-gates.md)
- Review workflow: [`skills/review/SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/SKILL.md)
- Durable rules: `MEM-0006`, `MEM-0007`, `MEM-0045`, `MEM-0048`, `MEM-0064`
- Drift checks:
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `python3 bin/check_harness_invariants.py`

### Runtime And Hooks

- Runtime spec: [`docs/specs/runtime-surface.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/runtime-surface.md)
- Stop-hook review gates: [`docs/specs/review-gates.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/review-gates.md)
- Hook code: [`bin/stop_hook.py`](/Users/kenjipcx/coding-harness/Codexter/bin/stop_hook.py)
- Durable rules: `MEM-0008`, `MEM-0010`, `MEM-0023`, `MEM-0034`, `MEM-0035`
- Drift checks:
  - `python3 bin/test_stop_hook.py`
  - `python3 bin/test_runtime_state.py`

### Context Graph And Case Memory

- Seed spec: [`docs/specs/case-based-memory-context-graph.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/case-based-memory-context-graph.md)
- Existing ledgers: [`docs/MEMORY.md`](/Users/kenjipcx/coding-harness/Codexter/docs/MEMORY.md), [`docs/HISTORY.md`](/Users/kenjipcx/coding-harness/Codexter/docs/HISTORY.md), [`docs/TROUBLES.md`](/Users/kenjipcx/coding-harness/Codexter/docs/TROUBLES.md), [`docs/features/registry.jsonl`](/Users/kenjipcx/coding-harness/Codexter/docs/features/registry.jsonl)
- Feature row: `FEAT-0026`
- First target: connect decisions, features, tickets, sources, memories, and
  troubles without replacing the existing ledgers.

## Minimal Example

When adding a new harness rule:

1. Decide the owner with [`harness-advisor`](/Users/kenjipcx/coding-harness/Codexter/skills/harness-advisor/SKILL.md).
2. Put the operational rule in the owning surface.
3. Add a durable `MEM-####` only if the rule is reusable.
4. Add or update a `FEAT-####` row only if the rule changes a harness feature.
5. Update this index only when the new rule creates a new cluster or changes
   where agents should look.

## How To Test

Run the relevant checks for the surfaces changed:

```bash
python3 docs/features/validate_features.py
python3 tickets/scripts/check_ticket_metadata.py
python3 bin/check_harness_invariants.py
python3 bin/check_doc_parity.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

Use only the checks that match the changed surface. For example, a policy index
wording change does not need skill registry regeneration unless skill metadata,
skill links, or direct checklists changed.
