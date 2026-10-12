---
name: doc-advisor
description: "Use for \"update the docs\", \"where should this doc live\", \"consolidate this\" or \"shrink this without losing anything\": a docs strategy, a grounded doc update, or a loss-checked consolidation."
source: local
department: delivery
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Doc Advisor

## Context

Use this for a ticket's docs decision, for writing or revising durable repo docs
(feature and system specs, runbooks, templates, registry companions, public
guidance), and for consolidating any artifact into its smallest owner-correct
form without losing behaviour, evidence, IDs or decisions. Documentation
architecture lore lives in [Documentation OS](../../docs/systems/documentation-os.md);
this skill owns the executable workflow. It does not edit skill packages
(`harness` maintain mode), Wiki entities (`manage-wiki`), or code (`code-health`).

## Skill Signature

```text
doc_advisor(doc_task, mode?: strategy | write | consolidate, target?, evidence?)
  -> docs_strategy | doc_delta + doc_quality_result | consolidation_frame + loss_check
reads: ticket, plan or diff, target doc, nearest owner and index, source evidence, consumers and backlinks
does: decides docs, writes for the reader's next action, or rebuilds an artifact to its owner contract
writes: Docs Strategy block, target doc, consolidated artifact or patch, permitted archive rows
returns: strategy or updated doc, checks run, loss check, review route, remaining risk
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Pick the mode and bind the reader.**
  `request + target -> mode + doc_contract | blocked`

  Rule: Ticket or implementation planning is `strategy`; a new or revised doc is
  `write`; "smaller, clearer, owner-correct" is `consolidate`. For `write`,
  name audience, doc type, owning file, source of truth, next action, canonical
  terms and proof surface before drafting.

  Assert:
  - One mode; the owning file exists or the reason a new owner is needed.
- [ ] **N2 — strategy: decide docs once.**
  `ticket + diff -> docs_strategy {outcome, doc_targets, no_docs_reason, validation}`

  Rule: `update_docs` names targets and the validator; `no_docs` names a
  concrete reason. Routine ticket closure is not a field; closing follows
  `tickets/README.md`.

  Assert:
  - A `no_docs` outcome carries a reason a reviewer could check.
- [ ] **N3 — write: ground, place, then draft for the next action.**
  `doc_contract + evidence -> doc_delta | owner_conflict`

  Rule: State `Grounding:` for local, official, current, peer or standard
  claims; use `research` when one source will not do. Put the current
  definition or task path near the top, one canonical term per concept, and
  link to the owner instead of copying doctrine. Load
  [doc architecture](references/doc-architecture.md) for placement and
  [feature/system specs](references/feature-system-specs.md) for `FEAT-*` or
  `SYS-*` boundaries.

  Example: broad docs governance grown inside one feature page -> a system spec
  owns the policy; the feature page keeps behaviour, surfaces, proof, limits.

  Assert:
  - No second source of truth; task-local proof stays in the ticket.
- [ ] **N4 — Update metadata and generated views from their sources.**
  `doc_delta -> front matter + regenerated registries | validator failure`

  Rule: Load [metadata](references/metadata-and-registries.md) before changing
  front matter, feature or system refs, or template metadata. Generated JSONL
  registries are outputs: edit the source, then run the generator.

  Assert:
  - No hand-edited generated row.
- [ ] **N5 — consolidate: score units, archive before delete, prove no loss.**
  `target + owner contract -> unit decisions + minimal artifact + loss_check | blocked`

  Rule: Inventory individual units, never category buckets. Hard constraints
  (IDs, evidence, gates, safety, owners, traceability) beat the value score.
  For knowledge targets score each candidate
  `importance 0..3 + recency 0..2 + factuality 0..2 + remembrance 0..3`;
  `keep_live` needs importance >= 2, factuality >= 2, remembrance >= 2 and not
  superseded; recency ranks but never overrides factuality. Before removing an
  exact row from a log or append-only artifact, bind an archive or canonical
  source that keeps its exact wording; none -> block the deletion. For
  `AGENTS.md` or `runtimes/AGENTS.md`, apply the Feature Fidelity Gate in
  `docs/templates/global-agents-qa-checklist.md` against
  `docs/systems/agent-kernel.md` and run
  `python3 bin/validators/check_harness_invariants.py`. Load
  [consolidate](references/consolidate.md) for the value function, response
  frame and Tidy Report.

  Assert:
  - Knowledge targets show every candidate's four scores, disposition, owner
    and stale evidence, then the full Tidy Report with `none` for empty lines.
  - A shorter artifact that lost a behaviour, ID, route or gate fails.
- [ ] **N6 — Finish-check and route review.**
  `finished work -> doc_quality_result + review route`

  Rule: Load [finish gate](references/finish-gate.md) before material
  closeout. Run only relevant validators (`docs/features/validate_features.py`,
  `bin/validators/check_doc_refs.py`, `check_skills.py --write` when those
  surfaces changed). Route canonical, public, cross-surface or policy-bearing
  docs to [review](../review/SKILL.md) with `documentation-quality`.

  Assert:
  - Failed checks, fixes, deferrals and remaining risk are named; no scalar
    readiness score.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Creating a new doc when an existing owner has the same audience, lifecycle
  and retrieval path.
- Treating skill references as canonical lore; system and feature docs own
  durable policy.
- Citing external best practice as Farplane policy without labelling it.
- Compacting an exact log into a summary without the archive gate, or keeping a
  true fact in memory when another surface retrieves it better.
- Self-approving a material skill compaction; route it through
  `harness` maintain mode and an independent reviewer.

## Reference Map

- [doc architecture](references/doc-architecture.md) - owner surface, doc type,
  split, merge or delete, density, lifecycle.
- [metadata and registries](references/metadata-and-registries.md) - front
  matter, feature and system refs, generated registries.
- [feature/system specs](references/feature-system-specs.md) - feature vs system
  vs local reference vs ticket artifact.
- [finish gate](references/finish-gate.md) - material docs closeout.
- [consolidate](references/consolidate.md) - value function, knowledge scoring,
  archive gate, response frame, Tidy Report.

## Output

- `strategy`: the `docs_strategy` block.
- `write`: the updated doc plus `doc_quality_result` (checks run, fixes,
  deferrals, review route, remaining risk).
- `consolidate`: the nine-part response frame, the changed artifact or patch,
  the loss check and proof; knowledge targets add the scored table and Tidy
  Report.
