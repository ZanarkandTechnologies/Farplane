---
kind: goal-progress
status: active
created_at: 2026-06-12
updated_at: 2026-10-13
template_id: goal-loop-progress
template_version: "0.2.2"
---

<!-- Two shapes for a Goal on a GitHub issue. Only a project without a GitHub
repository saves them as local files (`tickets/README.md`, legacy section). -->

## Current Goal state

<!-- Last section of the issue body. After every Goal turn replace only this
section (goal-advisor Issue commands, Writeback); everything above stays
byte-identical so the freshness hash holds. History lives in Goal turn comments.
Only an optimization Goal whose candidates compare records its best-so-far
result; feature work records completed proof and the remaining next_action. -->

```yaml
updated_at:
turn:
decision: execute | diagnose | report_now | request_feedback | stop | blocked
remaining_budget:
drift_verdict: aligned | drifting | blocked | complete_candidate | not_run
next_action:
blocker:
```

## Goal turn comment

<!-- Post one top-level comment per Goal turn, heartbeat, feedback resume, or
drift checkpoint (`gh issue comment <n> -R <owner/repo> --body-file <file>`).
Every one starts with `**Goal turn N**` (add `(heartbeat)` for heartbeats) so
first load finds it. Keep it compact, link artifacts instead of pasting
transcripts, and keep private evidence under `.farplane/`: the repository may
be public. When a tree is listed, name the selected node and its result. A rule
change gets its own comment headed `Decision:`; the executor then returns
`request_feedback` or goes back to goal-advisor, which alone updates `## Goal
program` `### Binding Decisions` and asks for approval again. -->

```markdown
**Goal turn N** · YYYY-MM-DD HH:MM +0800

- `trigger:` native_goal | scheduled_heartbeat | human_feedback_received | manual_resume
- `intent:`
- `action:`
- `observation:`
- `evidence:`
- `learning:`
- `decision:` execute | diagnose | report_now | request_feedback | stop | blocked
- `remaining_budget:`
- `drift_verdict:` aligned | drifting | blocked | complete_candidate | not_run
- `drift_evidence:`
- `next_action:`
- `blocker:`
```

Review waits use labels and the blocker text, as `tickets/README.md` says; do
not keep a review ledger in the body.
