---
name: consolidate
description: "Compress artifacts into their minimal owner-correct form while preserving required behavior, evidence, IDs, decisions, and future actionability."
tier: 1
source: local
template_uses:
  skill-template: "0.4.4"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Consolidate

## Context

Use `consolidate` when an artifact or entity set must become smaller, clearer,
or more owner-correct without losing required value. It rebuilds the target
against its owning contract; it does not merely summarize it for a reader.
For knowledge surfaces, it also owns the former knowledge-pruning workflow:
rank factual value, preserve source rows when required, and route material to
the surface that should retrieve it.

## Skill Signature

```text
consolidate(target, structure?, template?, constraints?, value_function?, proof?)
  -> inventory + unit_decisions + minimal_artifact_or_patch
   + loss_check + handoff_or_blocker
reads: target, owning contract, consumers, backlinks, and available evidence
does: inventories, scores, routes, and rebuilds natural units
writes: target or proposed patch; permitted archive and handoffs when required
returns: response frame, changed artifact or patch, loss check, and proof
```

Supported structures include `file`, `directory`, `registry`, `skill`,
`eval_suite`, `gotchas`, `checklist`, `docs_tree`, `memory`, and `other`.
Actions are `keep | merge | rewrite | move | delete | promote | demote | defer`.
Knowledge-facing dispositions are `keep-live | merge | route-owner |
archive-only | stale | needs-question`.

## Value And Knowledge Gates

Use the default value function unless the owning contract supplies a clearer
one:

```text
value(unit) = execution_value + proof_value + routing_value + reuse_value
            + memory_value + user_value - fluff - duplication
            - stale_risk - wrong_owner_risk
```

Hard constraints beat scoring. Preserve required IDs, evidence, gates, safety,
owner boundaries, source traceability, and actionability before optimizing
size.

For knowledge targets with `structure = memory | docs_tree | file`, adapt the
default without dropping it:

```text
knowledge_score(candidate) = importance + recency + factuality + remembrance
importance: 0..3    recency: 0..2    factuality: 0..2    remembrance: 0..3
keep_live = importance >= 2
         && factuality >= 2
         && remembrance >= 2
         && not superseded
```

`recency` informs ranking but never overrides factuality. Before removing an
exact row from a log or semi-append-only artifact, bind a lifecycle-permitted
archive or canonical source that preserves its exact wording. If none exists,
block deletion. Do not invent a tracked archive when the owning lifecycle
requires promotion to history, a spec, or another canonical owner instead.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

1. Bind `target`, `structure`, the exact owning template or inferred contract,
   hard constraints, and proof obligation. For knowledge surfaces, resolve the
   exact-row preservation path before any destructive decision.
2. Inventory natural units and their consumers, backlinks, IDs, evidence,
   current owner, and stale or superseded signals. Missing evidence makes a
   factual claim `needs-question` or `stale`; do not silently rewrite it.
3. Score and classify every unit. Apply the full default value function; for
   knowledge targets also record all four knowledge dimensions and the live
   threshold result. Route high-importance duplicates to their existing owner
   instead of keeping a second copy.
4. Rebuild the minimal owner-correct artifact. Preserve passing live knowledge
   and source refs; route reusable procedures to `skill-maintenance`, project
   knowledge and doc-quality work to `doc-advisor` and owning project files,
   sourced entity deltas to `manage-wiki`, and material canonical changes to
   `review`. Return the standard frame and, for knowledge targets, the Tidy
   Report below.
5. Run the loss check and applicable validator, eval, or review. Restore, move,
   defer, or block any lost behavior, evidence, ID, route, safety condition,
   metric, owner boundary, or future action. A shorter artifact is insufficient
   unless it remains at least as useful and more owner-correct.
   For `AGENTS.md` or `templates/global/AGENTS.md`, first load the Agent Kernel
   canonical feature inventory at `docs/systems/agent-kernel.md` and apply the
   bidirectional Feature Fidelity Gate in
   `docs/templates/global-agents-qa-checklist.md`: every documented behavior
   group remains implemented, and every surviving or added AGENTS section
   remains documented. Section presence alone does not prove behavior
   preservation; any unexplained loss or weakened high-risk behavior fails the
   consolidation. Preserve independent reasoning before agreement and its
   non-sycophantic response opening, then run
   `python3 bin/validators/check_harness_invariants.py` plus affected behavior
   evals before completion.
   Assert: for a knowledge target, the visible response includes every
   candidate's four numeric scores, disposition, owner, and named evidence for
   stale or changed facts, followed by the complete Tidy Report. Do not replace
   this evidence with only a generic Before/After summary. Emit every Tidy
   Report label verbatim and write `none` when a category is empty. Keep
   `archive or canonical source:` and `archived only:` as separate lines; do
   not rename, combine, or omit them.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Required response frame:

```text
1. Bound target:
2. Owning template or contract:
3. Hard constraints:
4. Value function:
5. Unit inventory:
6. Unit decisions:
7. Minimal artifact, patch, or handoff:
8. Loss check:
9. Proof:
```

For knowledge targets, add:

```text
Knowledge Tidy Report
- target:
- archive or canonical source:
- kept live:
- consolidated:
- routed to owners:
- archived only:
- stale or questionable:
- validators:
- review route:
```

Use a candidate table when more than a few knowledge units are present:

```text
| Candidate | Importance | Recency | Factuality | Remembrance | Disposition | Owner |
```

## Gotchas

- Do not optimize word, row, or file count ahead of hard constraints or value.
- Do not call category buckets an inventory; inspect individual rows, bullets,
  sections, cases, or files before deleting them.
- Do not keep a true fact in memory when another surface is its better retrieval
  owner, and do not promote ticket-local proof into project memory.
- Do not compact exact logs into summaries without the archive/source gate.
- For material skill edits, route the patch through `skill-maintenance` and an
  independent reviewer rather than self-approving it.

## Output

- The required response frame and, for knowledge targets, a Tidy Report.
- For knowledge targets, a scored candidate table with evidence-backed stale
  classifications; never silently replace an old factual row.
- An updated artifact or patch with unit decisions and routed handoffs.
- A loss check plus validator, eval, review evidence, or explicit blocker.
