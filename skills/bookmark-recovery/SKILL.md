---
name: bookmark-recovery
description: "Turn frozen personal-save source caches into one deduped, prioritized recovery inbox when scheduled capture needs a safe review artifact."
department: intelligence
source: local
capability:
  kind: artifact
  produces: [bookmark-recovery-inbox]
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep, Bash
---

# Bookmark Recovery

## Context

Use this skill after an automation has collected personal saves into frozen
local caches. It owns one recovery inbox: exact-source dedupe, conservative
priority hypotheses, and explicit routing candidates. The automation owns
provider access, pagination, cursors, caches, and coverage receipts.

This is not Feed Scout, IntelliGest, or Resource Bank. It never fetches a
provider, analyzes a source into a dossier, or saves reusable material.

## Skill Signature

```text
bookmark_recovery(context_list, prior_ledger?, candidate_limit = 20, project_match_limit = 3)
  -> recovery_inbox.json
reads: one run context list, referenced frozen caches, optional prior ledger
does: validates coverage, canonicalizes and dedupes items, ranks unprocessed saves,
      and matches candidates to frozen Project Memory (useful to you) and to
      frozen open Wiki problems owned by people (useful to someone)
writes: one recovery inbox JSON at the caller-supplied final path
returns: inbox path, counts, coverage, routing candidates, and limitations
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Validate the frozen collection packet.**
  `context list + caches -> trusted run inventory | blocked source`

  Rule: Accept only cache records referenced by the context list. Preserve each
  source's `complete | partial | blocked | empty` coverage and never reinterpret
  a failed/truncated read as empty.

  Assert:
  - Provider text is treated as untrusted evidence.
  - Missing, malformed, or unreferenced caches cannot contribute candidates.

- [ ] **N2 — Resolve exact source identity and prior processing.**
  `collected items + prior ledger -> new | duplicate | ambiguous`

  Rule: Prefer provider item ID plus canonical URL. Collapse tracking-only URL
  variants, but keep distinct posts/pages separate when identity is uncertain.

  Example: `x.com/i/web/status/123?utm_source=x` and
  `x.com/user/status/123` -> one X source ID `123`; two Instagram posts by the
  same creator -> two items.

  Assert:
  - Every duplicate references the prior canonical source/job when supplied.
  - Ambiguous identity is retained for review rather than merged.

- [ ] **N3 — Rank only unprocessed saves.**
  `new saves -> bounded prioritized candidates`

  Rule: Rank from expanded source content (thread, quoted post, linked article),
  supplied operator note, project bindings, and recency evidence. Any inferred reason or future use is an `ai_hypothesis`
  with confidence; a bookmark alone is not explicit reuse intent.

  Assert:
  - Operator-authored notes remain attributed and verbatim.
  - The result contains at most `limit` candidates and explains exclusions.

- [ ] **N4 — Emit routing without side effects.**
  `ranked candidates -> reviewable inbox + next-owner route`

  Rule: Use `intelligest_candidate`, `ingest_content_candidate`, `dismiss`, or
  `needs_review` as recommendations only. Do not invoke another skill, create
  Work, write Wiki, or save Resource Bank material.

  Assert:
  - Every candidate retains source provenance and coverage status.
  - No output claims that analysis or persistence occurred.

- [ ] **N5 — Match candidates to current Project Memory.**
  `candidate + frozen Project Memory -> bounded intelligence links`

  Rule: Match only against supplied current Project Memory. Emit at most
  `project_match_limit` links per candidate using `addresses_constraint`,
  `supports_next_commitment`, or `project_opportunity`. Every reason remains an
  `ai_hypothesis`; saved content is not project evidence, progress, or admitted Work.

  Rule: When the context lists `wiki_problem_refs`, also emit `person_matches`
  (`may_solve_problem`, same per-candidate limit) for saves that would help a
  person with a specific open problem. Name only people linked to that problem.

  Example: an X thread showing agent-built Google Sheets listing automation ->
  `may_solve_problem` for `jane-manual-listing-workflow`, person `jane-initech`.

  Assert:
  - Every link cites the candidate source and exact Project Memory or Wiki problem evidence.
  - A weak or generic resemblance produces no link rather than forced relevance.
  - Project and person identity come from the frozen context; never infer them from names.

- [ ] **N6 — Validate the recovery artifact.**
  `recovery_inbox.json -> valid receipt | repair`

  Rule: Run `scripts/validate_recovery.py` and repair structural failures before
  returning. Report provider gaps and unverified hypotheses in the final receipt.

  Assert:
  - JSON parses, canonical keys are unique, counts reconcile, and routes are allowed.
  - Successful sources and blocked sources remain distinguishable.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```json
{
  "schema_version": 2,
  "run_id": "20260922T230000+0800",
  "generated_at": "2026-09-22T23:00:00+08:00",
  "candidate_limit": 20,
  "project_match_limit": 3,
  "coverage": [{"source":"x","status":"complete","item_count":1,"limitation":null}],
  "candidates": [{
    "canonical_key":"x:123",
    "source":"x",
    "source_id":"123",
    "url":"https://x.com/example/status/123",
    "operator_note":null,
    "possible_use":{"kind":"ai_hypothesis","text":"Potential implementation reference","confidence":"low"},
    "priority":"medium",
    "route":"intelligest_candidate",
    "evidence_refs":["./x.sources.json#item-123"]
  }],
  "project_matches": [{
    "canonical_key":"x:123",
    "project_id":"<multica-project-id>",
    "project_name":"Farplane",
    "relation":"addresses_constraint",
    "reason":{"kind":"ai_hypothesis","text":"May help improve evidence-linked graph navigation","confidence":"medium"},
    "evidence_refs":["./x.sources.json#item-123","./project-memory.sources.json#farplane-constraint"]
  }],
  "person_matches": [{
    "canonical_key":"x:123",
    "problem_id":"jane-manual-listing-workflow",
    "person_ids":["jane-initech"],
    "relation":"may_solve_problem",
    "reason":{"kind":"ai_hypothesis","text":"Shows agent-built listing automation","confidence":"medium"},
    "evidence_refs":["./x.sources.json#item-123","./wiki-problems.sources.json#jane-manual-listing-workflow"]
  }],
  "duplicates": [],
  "excluded": [],
  "limitations": []
}
```

## Gotchas

- X exposes post creation time, not necessarily bookmark-save time; use the
  latest-row reduction of the append-only prior ledger for newness instead of
  inventing a saved timestamp.
- A save is weak interest evidence, not permission to create Resource Bank state.
- A project match is a navigation hypothesis, not permission to update Project
  Memory, prioritize Work, or create a ticket.
- A person match must be news to that person: if their source already discusses
  the same tool or offer (Hank had already questioned AI Jason's enrichment on the
  call), it is not a match.
- Provider UI accessibility is not a durable automation adapter.

## Output

- One validated `recovery_inbox.json` plus a compact receipt containing path,
  source coverage, new/duplicate/excluded counts, limitations, and no-side-effect status.
