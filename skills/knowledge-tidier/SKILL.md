---
name: knowledge-tidier
description: "Turn bloated knowledge artifacts into ranked keep/cut/reroute decisions when docs, memory, or context surfaces need pruning."
tier: 3
group: project-ops
source: local
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Knowledge Tidier

## Context

Use this skill when a knowledge artifact has grown into mixed signal, stale
facts, duplicate doctrine, vague claims, and genuinely useful reusable context.
This includes `docs/MEMORY.md`, long docs, lesson ledgers, context packets,
strategy notes, and other files whose value depends on what future agents or
humans should actually remember.

This skill is not a prose-polishing pass. Use
[doc-advisor](../doc-advisor/SKILL.md) when the main job is reader-quality
writing, examples, terminology, or doc architecture. Use
[update-memory](../update-memory/SKILL.md) for whole-project context refresh.

The job is ranking and routing: inspect the artifact, find the nonsense and
low-value sections, score what remains, keep only important factual knowledge,
preserve exact source logs when the file is semi-append-only, and route owner
specific rules to their better home instead of making one bloated knowledge
file carry everything.

Use `consolidate(target = target_file, structure = memory | docs_tree | file,
value_function = knowledge_score + default consolidate value function)` for the
keep/merge/move/delete decision pass. This skill binds knowledge-specific
archive, factuality, and owner-surface constraints around that primitive.

## Skill Signature

```text
knowledge_tidier(target_file, archive_ref?, owner_surfaces?, window?)
  -> kept_knowledge_delta + archive_delta? + routed_handoffs + skipped_items
state: reads(target_file, archive_ref, AGENTS.md, relevant specs/skills/docs)
       writes(target_file, archive only when preserving exact source rows)
gates: source_preserved; scoring_applied; owner_checked; no_data_loss;
       stale_facts_flagged; validators_or_review_run
routes: consolidate | documentation | update-memory | skill-maintenance | review
fails: deletes exact logs without archive; keeps generic policy; preserves
       stale or non-factual claims; duplicates always-loaded prompts
```

## Scoring Model

Score each candidate section, row, bullet, or claim before keeping it live:

```text
knowledge_score(candidate) = importance + recency + factuality + remembrance
```

- `importance` from 0-3: cost if future agents forget it.
- `recency` from 0-2: current or recently changed behavior gets more weight;
  old but still binding facts can still pass through importance.
- `factuality` from 0-2: concrete, source-backed, and falsifiable beats taste,
  aspiration, or vague doctrine.
- `remembrance` from 0-3: value not already carried by `AGENTS.md`, specs,
  skills, tickets, validators, or code.

Keep live only when:

```text
keep_live = importance >= 2
         && factuality >= 2
         && remembrance >= 2
         && not superseded
```

High-importance rows that fail remembrance should route to the existing owner
surface. Low-factuality rows become questions, tickets, or archive-only notes.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind sources and preservation path.
   - [ ] Resolve `target_file`, such as `docs/MEMORY.md`, a long doc, a
     context packet, or a lesson ledger.
   - [ ] Find or create an archive path before removing exact historical rows
     from semi-append-only files.
   - [ ] Read the nearest `AGENTS.md`, lifecycle spec, and relevant owner docs
     to detect duplicated doctrine.
- [ ] 2. Extract candidate knowledge.
   - [ ] Treat dated rows, bullets, headings, and source-row groups as
     candidates.
   - [ ] Preserve exact old wording in the archive when the source is a log or
     semi-append-only ledger.
   - [ ] Mark stale facts, vague claims, generic advice, superseded paths,
     duplicate doctrine, and owner-surface duplicates.
- [ ] 3. Score and classify each candidate.
   - [ ] Call `consolidate(..., structure = memory | docs_tree | file)` with
     the adapted `knowledge_score` value function for keep/merge/rewrite/move/delete
     decisions.
   - [ ] Classify domain disposition as `keep-live`, `merge`, `route-owner`,
     `archive-only`, `stale`, or `needs-question`.
   - [ ] Prefer factual project-specific constraints over generic agent policy.
- [ ] 4. Rewrite the live knowledge surface.
   - [ ] Keep a short admission rule or reader contract when useful.
   - [ ] Keep only sections or rows that pass the live threshold.
   - [ ] Apply the accepted `consolidate` merge/rewrite decisions to older
     passing rows, preserving source refs.
   - [ ] Remove or route duplicated `AGENTS.md`, spec, skill, validator,
     ticket-template, and style rules.
- [ ] 5. Report routed handoffs.
   - [ ] Send doc-quality rewrites to [doc-advisor](../doc-advisor/SKILL.md).
   - [ ] Send skill behavior hardening to
     [skill-maintenance](../skill-maintenance/SKILL.md).
   - [ ] Send broad project refresh to [update-memory](../update-memory/SKILL.md).
   - [ ] Name stale facts that need human or file confirmation.
- [ ] 6. Verify and review.
   - [ ] Run doc link validators when links or refs changed.
   - [ ] Run skill checks when this skill changed.
   - [ ] Use [review](../review/SKILL.md) for material canonical memory changes
     when an independent reviewer lane is available.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Candidate table:

```text
| Candidate | Importance | Recency | Factuality | Remembrance | Action | Owner |
| --- | ---: | ---: | ---: | ---: | --- | --- |
```

Tidy report:

```text
Knowledge Tidy Report
- target:
- archive:
- kept live:
- consolidated:
- routed to owners:
- archived only:
- stale or questionable:
- validators:
- review route:
```

## Gotchas

- Do not compact important logs into a tiny summary without preserving exact
  source rows.
- Do not keep a claim in a knowledge file just because it is true; keep it only
  when that file is the best retrieval owner.
- Do not hide always-needed behavior in a rarely read doc. Put always-needed
  behavior in `AGENTS.md`, a skill checklist, a spec, a validator, or a ticket
  template.
- Do not treat recency as more important than factuality. Recent guesses should
  not outrank older binding constraints.
- Do not let source-row IDs become the main reading experience; use them for
  traceability after the human-readable knowledge.

## Reference Map

- [filesystem lifecycle](../../docs/features/FEAT-0060-registry-backed-documentation-os.md) - read for
  artifact roles, read defaults, drain rules, and archive/delete boundaries.
- [doc-advisor](../doc-advisor/SKILL.md) - use for durable doc-quality
  rewrites outside memory ranking.
- [update-memory](../update-memory/SKILL.md) - use for broad project context
  refresh across README, docs, history, lessons, and troubles.
- [consolidate](../consolidate/SKILL.md) - use for the shared unit inventory,
  value scoring, merge/move/delete decisions, and loss check.
- [skill-maintenance](../skill-maintenance/SKILL.md) - use when a knowledge
  item should harden skill behavior through evals, gotchas, or checklist
  changes.
- [review](../review/SKILL.md) - use for material canonical knowledge changes.

## Output

- Updated live artifact with only high-value current knowledge.
- Archive reference that preserves exact historical wording.
- Tidy report naming kept, routed, archived, stale, and questionable items.
- Validators or explicit blocker.
