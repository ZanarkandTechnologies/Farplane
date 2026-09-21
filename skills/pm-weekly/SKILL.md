---
name: pm-weekly
description: "Turn a complete frozen week of Farplane Project Memory and coverage evidence into grounded project reviews, a company rollup, and next-week memory JSON."
tier: 3
source: local
template_uses:
  skill-template: "0.6.2"
group: operations
allowed-tools: Read, Write, Glob, Grep
---

# PM Weekly

## Context

Use once after the final Daily run freezes the complete reporting set. This
skill reads local evidence and writes one JSON handoff. The Weekly automation
owns rendering, Multica effects, and readback. This workflow is adapted from
Zanarkand AI's operated Company OS Weekly.

## Skill Signature

```text
pm_weekly(frozen_week, project_memories, prior_reports?, output_path)
  -> weekly_extraction_json
reads: frozen inventory, coverage, Project Memory, prior reports
does: consolidates results, money movement, constraints, and carry-forward
writes: exactly output_path
returns: extraction path + ready|blocked
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Require the complete frozen set.**
  `inventory + coverage + memories -> complete set | blocked`

  Rule: require one readable current-week memory for every expected Project.
  Sparse evidence is valid; a missing or wrong-week Project blocks rollup.

  Assert:
  - Excluded, archived, and duplicate Projects remain excluded.
  - Missing coverage stays unknown and never becomes a healthy-week claim.

- [ ] **N2 — Compose each Project review.**
  `Project Memory + prior report -> weekly Project result`

  Rule: lead with verified money movement and delivered results, then the
  constraint closest to the next monetization event, consequential decisions,
  and one next-week commitment. Do not rate activity, effort, or people.

  Assert:
  - Each claim cites its Daily memory or frozen source.
  - Unknown money movement and proxy evidence are labelled honestly.
  - When the commercial frame is missing, `decisions` asks the operator for the
    smallest defining choice needed to continue or explicitly stop the Project.

- [ ] **N3 — Roll up the company without averaging away blockers.**
  `complete Project reviews -> company review`

  Rule: include every Project once; elevate shared results, material money
  movement, cross-project constraints, and operator decisions. Preserve
  conflicting Project states rather than manufacturing a portfolio score.

  Assert:
  - Quiet or evidence-limited Projects remain visible.
  - One Project's success never masks another Project's blocker.

- [ ] **N4 — Carry forward only unresolved commitments.**
  `current memory + review -> next-week memory`

  Rule: carry the latest supported commercial frame, money state, unresolved
  constraint, decisions, and next commitment. Remove resolved attention and
  avoid repeating one dependency across sections.

  Assert:
  - Closed Projects receive no new next-week memory.
  - No new strategy, target, owner, date, or task is invented.

- [ ] **N5 — Propose bounded existing-task actions.**
  `Project reviews -> actions[]`

  Rule: propose only evidence-backed comment, checkpoint, status, or priority
  updates on exact existing Multica issues. Weekly reports proposals for new
  work but does not admit, assign, or execute them.

  Assert:
  - Each action includes issue ID, expected revision, reason, and sources.
  - The issue ID belongs to the frozen Project inventory.
  - The action matches the exact allowlist below and contains no extra fields.
  - Provider-facing text excludes private paths and opaque IDs.

- [ ] **N6 — Emit one complete JSON handoff.**
  `Project reviews + company review + carry-forward -> extraction JSON`

  Rule: Step 4 renders the declared artifacts and applies authorized actions.
  This skill writes no Markdown, provider state, or secondary memory.

  Assert:
  - Artifact paths are unique and every expected Project is represented.
  - Blockers prevent partial company rollup rather than being silently omitted.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## JSON Contract

```json
{
  "week": "...",
  "status": "ready|blocked",
  "project_reviews": [{"project_id": "...", "sections": [], "sources": []}],
  "company_review": {"sections": [], "sources": []},
  "next_week_memories": [{"project_id": "...", "memory": {}}],
  "actions": [],
  "blockers": []
}
```

Project sections follow [Project report](templates/project-report.md); the
company sections follow [Company report](templates/company-report.md).

### Action Contract

Every action has exactly `type`, `issue_id`, `expected_revision`, `reason`,
`sources`, and `payload`. `issue_id` must exist in the frozen Project inventory
and `expected_revision` must equal its frozen revision. Reject the whole action
when either check fails, when a field is extra, or when `payload` contains
creation, assignment, agent, squad, autopilot, run, execution, or start fields.

| `type` | Exact `payload` fields | Allowed values |
| --- | --- | --- |
| `comment` | `body` | non-empty evidence-backed text |
| `checkpoint` | `body` | non-empty replacement for the existing issue's `Current Goal state` section |
| `status` | `status` | `todo`, `in_progress`, `in_review`, or `blocked` |
| `priority` | `priority` | `low`, `medium`, `high`, or `urgent` |

Step 4 rechecks the current revision immediately before applying an action.
Mismatch, duplicate intent, unknown type, or malformed payload yields a blocked
receipt and no mutation. Terminal transitions belong to the canonical verified
close route outside Company OS. Do not invoke or report closeout from this skill.

## Gotchas

- A complete set with sparse evidence produces a qualified report, not a failure.
- Cross-project repetition is not a reusable SOP unless receiver-accepted evidence supports it.
- Weekly reports a proposed new task; only the planner admits it later.
- Omit unrelated closeout discussion and execution receipts; this skill neither
  closes issues nor runs work.

## Output

Return the extraction path, status, represented Project count, money-movement
summary, unresolved constraints, action count, blockers, and
`provider_effects: none`.
