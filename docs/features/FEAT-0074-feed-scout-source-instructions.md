---
title: Feed Scout Source Instructions
status: implemented
owner: feed-scout
created_at: 2026-07-24
updated_at: 2026-07-24
tags:
  - farplane
  - feature
  - sys-0008
  - source-intelligence
refs:
  - skills/feed-scout/SKILL.md
  - skills/feed-scout/references/data-model.md
  - docs/features/FEAT-0072-persistent-icp-and-world-memory.md
feature_id: FEAT-0074
system_id: SYS-0008
category: source-intelligence
public: true
surfaces:
  - farplane/bindings.yaml
  - skills/init-advisor/references/BINDINGS_TEMPLATE.yaml
  - skills/feed-scout/SKILL.md
  - skills/feed-scout/references/data-model.md
  - skills/feed-scout/references/workflow.md
  - skills/feed-scout/evals/evals.json
source_refs:
  - skills/feed-scout/audits/2026-07-24-source-instructions.md
external_refs: []
evidence_refs:
  - bin/validators/test_check_farplane_project_files.py
  - skills/feed-scout/evals/evals.json
known_limits: >-
  Claim-relative source redundancy is conservative agent judgment rather than
  a persisted provenance graph; ambiguous relationships remain unknown and are
  sampled instead of suppressed.
metrics:
  - none mechanical
last_verified: 2026-07-24
experimental: true
superseded_by: false
track: >-
  Review instruction-driven Feed Scout reports and proposal-ledger rows for
  correct inheritance, primary-source preference, distinct channel evidence,
  one-hop source nomination, duplicate proposal reuse, and gate preservation.
---

# Feed Scout Source Instructions

Feed Scout gives every tracked entity and source one flexible task surface:

```text
source_task(entity.instructions?, source.instructions?, fixed_policy, evidence)
  -> items + source_proposals + promotion_candidates + feature_candidates
```

## Contract

- `instructions` replaces specialized prompt fields. Entity instructions are
  inherited; source instructions refine the task for one source.
- Instructions may request extraction, prioritization, bounded discovery, and
  proposals. They never grant mutation authority.
- Source additions use the existing proposal ledger and require review before
  config changes. Entity/thesis changes use promotion review. Product feature
  ideas remain planner candidates and may become separate reviewed tickets.
- `owned_sources.<source_id>` is the source identity/type hint. Source records
  do not repeat a `kind`; URL, handle, repo, org, or user coordinates support
  acquisition routing.
- Exact canonical URL/item dedupe remains separate from claim-relative source
  redundancy. Prefer sufficient first-party evidence, but preserve derivatives
  with original testimony, verification, contradiction, demonstrations,
  screenshots, or audience response.
- Only sources configured at run start may nominate source candidates.
  Nominees are ownership-checked, deduped through config and both ledgers,
  proposed once, and never recursively fetched or auto-added in that run.
- Existing privacy, logged-in access, spend, external-write, evidence, and
  authority gates remain fixed policy.

## Before / After / Example

> **Before:** `interest_prompt` described content relevance while proposed
> discovery/update fields would have fragmented source behavior.
>
> **After:** One `instructions` field describes the desired source task; fixed
> policy determines which reviewed artifact receives each proposed change.
>
> **Example:** A podcast instruction can request valuable guest discovery.
> Feed Scout retains original interview evidence, merges a verified guest-site
> nomination into one proposal-ledger row, and neither follows nor configures
> the nominee during that run.

## Proof

- Bindings validation accepts inherited/source `instructions` and rejects
  retired prompt fields plus redundant source `kind`.
- Skill eval fixtures cover flexible instruction routing, primary versus
  derivative evidence, and one-hop deduped podcast-guest nomination; they are
  JSON/query-linted in this change rather than claimed as a live model run.
- Feed Scout QA rechecks write authority, recursion stops, exact versus
  semantic dedupe, and privacy/spend gates.
