---
title: "Initial Knowledge Tidier Skill Audit"
status: active
owner: skill-maintenance
created_at: 2026-06-23
updated_at: 2026-06-23
tags:
  - knowledge-tidier
  - skill-audit
refs:
  - skills/knowledge-tidier/SKILL.md
  - skills/knowledge-tidier/eval_task.json
---

# Initial Knowledge Tidier Skill Audit

## Claim

`knowledge-tidier` is a focused project-ops skill for ranking bloated knowledge
artifacts by importance, recency, factuality, and remembrance value, then
rewriting the live surface without deleting exact historical logs when the
source is semi-append-only.

## Checklist Verdict

- `first_load_sufficiency`: pass. The scoring model, todo path, gates, and
  output shape are in `SKILL.md`.
- `reference_load_precision`: pass. References name when to use each owner.
- `duplicated_instruction_count`: pass. The skill points to existing
  documentation/update/skill-maintenance owners instead of absorbing them.
- `composition_clarity`: pass. Signature names inputs, outputs, state, gates,
  routes, and failure modes.
- `proof_surface_fit`: pass with lightweight proof. `eval_task.json` covers
  routing generic policy away from memory and flagging stale factual claims.

## Deferred

No automated eval run was added in this pass. The eval rows are available for
the existing eval surface; skill validators are the immediate structural proof.
