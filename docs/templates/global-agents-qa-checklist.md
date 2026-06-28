---
title: Global AGENTS Template QA Checklist
status: active
owner: templates
created_at: 2026-06-28
updated_at: 2026-06-28
refs:
  - templates/global/AGENTS.md
  - docs/features/FEAT-0042-lean-global-agent-operating-kernel.md
  - docs/features/FEAT-0043-project-level-system-prompt-eval-suite.md
  - docs/fundamentals/prompt-engineering.md
---

# Global AGENTS Template QA Checklist

Use this checklist before changing `templates/global/AGENTS.md`. The global
template is first-load context: keep rules there only when agents need them
before project files, tickets, or skills can reliably take over.

```text
agents_template_check(rule, evidence?)
  -> keep_global | summarize_global | move_to_project |
     move_to_skill_or_checklist | move_to_validator_or_eval |
     delete | needs_evidence
```

## Review Card

For each material rule or section, record:

- `rule_ref:` file and line or section.
- `current_job:` what behavior the rule causes.
- `frequency:` most chats, common material chats, rare specialist chats, or
  unknown.
- `omission_cost:` what fails if the rule is not first-loaded.
- `owner_surface:` global template, project `AGENTS.md`, skill, checklist,
  ticket, docs, validator, eval, hook, or subagent prompt.
- `availability:` whether the owner surface is loaded or discoverable before
  the rule matters.
- `duplication:` whether the same rule already exists in an owner surface.
- `specificity:` cross-project default or Farplane/project/operator-specific.
- `prompt_tax:` invariant, procedure, example, inventory, or doctrine.
- `proof:` diff, validator, review, eval, transcript replay, or representative
  behavior check.
- `decision:` one disposition from the signature above.

Default to `needs_evidence` when frequency, omission cost, or owner availability
is asserted without examples.

## Disposition Rules

- `keep_global`: use for short rules needed before any skill or project context
  can reliably be selected. Examples: autonomy, newest-message steering,
  destructive-action boundaries, verification, and skill-loading protocol.
- `summarize_global`: use when the invariant is global but examples,
  inventories, or procedure detail can move elsewhere.
- `move_to_project`: use when the rule is about Farplane development,
  project-local paths, local roles, commands, or repo-specific doctrine.
- `move_to_skill_or_checklist`: use when the rule only matters after a task
  family or skill is selected.
- `move_to_validator_or_eval`: use when the rule is mechanical or repeatable
  enough to prove outside prompt text.
- `delete`: use only for confirmed duplication, stale policy, or behavior that
  is no longer desired.
- `needs_evidence`: use when the proposed move or deletion could change
  behavior and lacks proof.

For `delete`, `summarize_global`, or any `move_to_*`, include stronger evidence
than for `keep_global`: a before/after prompt diff plus a review, fixture task,
eval, transcript replay, or representative behavior check when behavior risk is
material.

## Preview Gate

Before editing policy, prompt, workflow, UX, or architecture guidance, show the
concrete delta:

```text
Before:
After:
Example:
Accepted:
Rejected:
Evidence:
```

Use representative wording, data, or workflow state. A vague note such as
"summarize skill taxonomy" is not enough when the discussion already produced
specific before/after examples.

## Ticket Fidelity Gate

When turning discussion into a ticket, preserve the concrete examples,
accepted and rejected options, and decision rationale that made the plan
reviewable. Put bulky examples in a ticket artifact and link them from the
ticket when the ticket body would get too large.

## Worked Examples

### Farplane Lifecycle Path

`Before:` Global template names a Farplane-only file path:
`docs/features/FEAT-0060-registry-backed-documentation-os.md`.

`After:` Global says to follow the project lifecycle or documentation spec when
present. Farplane project `AGENTS.md` carries the exact `FEAT-0060` path.

`Decision:` `move_to_project`.

### Skill Taxonomy

`Before:` Global template lists Farplane skill tiers and inventory examples.

`After:` Global keeps the skill-use protocol: read `SKILL.md`, bind signatures,
load relevant references, apply `qa_checklist.md`, and seed visible todos from
the active skill. Farplane project docs own tier taxonomy and inventories.

`Decision:` `summarize_global` plus `move_to_project`.

### Browser QA Routing

`Before:` Global names `agent-browser`, `qa-tester`, and Playwright as a
specific browser-proof route.

`After:` Global says material proof uses `Done / Proof` or Goal program as the
scoreboard, delegates independent QA/review when needed, and uses the
project's browser-operation tooling for live evidence. Farplane project docs
name the exact browser and QA lane preference.

`Decision:` `summarize_global` plus `move_to_project`.
