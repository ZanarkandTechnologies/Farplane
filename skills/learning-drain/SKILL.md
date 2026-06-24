---
name: learning-drain
description: "Compatibility wrapper that turns recent TROUBLES/LESSONS rows into a skill-maintenance harden_skill handoff with dedupe and processed-state records."
tier: 3
group: harness
source: local
workflow: true
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Learning Drain

## Context

Use this skill only for legacy automations or direct requests that still say
`learning-drain`. The canonical weekly skill-upkeep interface is now
`skill-maintenance(mode: harden_skill)`.

This wrapper exists because older automations already call `learning-drain`.
It still owns the source-intake mechanics for `docs/TROUBLES.md` and
`docs/LESSONS.md`: dedupe, processed state, row pairing, caps, and safe
handoff. It should then route actionable skill-package work to
`skill-maintenance:harden_skill`.

The hot-path hook only logs. This skill drains the logs into action: it reads
recent trouble/lesson rows, dedupes against processed state, pairs related rows,
and creates a bounded hardening handoff for evals, gotchas, checklist
guardrails, tickets, or skill updates when a real harness/process fix is
implied.

New automations should call `skill-maintenance(mode: harden_skill)` directly
unless they need this legacy source-intake wrapper.

## Skill Signature

```text
learning_drain(project_root, since?, cap?, mode?)
  -> harden_skill_handoff? + processed_state_delta + no_change_reason?
state: reads(docs/TROUBLES.md, docs/LESSONS.md, .farplane/state/**/processed*.jsonl)
       writes(.farplane/state/learning-drain/processed.jsonl, ticket/thread refs when explicitly created)
gates: docs_present; rows_deduped; cap_respected; no_raw_transcripts; processed_state_written
routes: skill-maintenance:harden_skill | eval | optimize-harness | gap-analysis | direct-summary
fails: reprocesses old rows; deletes ledger history; spawns unbounded work; hides logic in automation prompt
```

## Drain Policy

- Keep `docs/TROUBLES.md` and `docs/LESSONS.md` append-only. Do not delete rows
  to mark them drained.
- Record processed rows in `.farplane/state/learning-drain/processed.jsonl`.
- Prefer the legacy processed path
  `.farplane/state/self-improve/weekly-drain-processed.jsonl` only as an input
  compatibility source; write new state to the flatter `learning-drain` path.
- Default cap is 5 actionable follow-ups per run.
- A follow-up is actionable only when the row implies a concrete change,
  regression eval, ticket, skill update, prompt/policy fix, or optimizer issue.
- Skill-package follow-ups should become `skill-maintenance(mode:
  harden_skill)` handoffs. `learning-drain` does not own final skill edits.
- Weak rows, duplicate rows, already-fixed rows, private/raw transcript risk, or
  rows with no clear owner produce `no_change` or `deferred`, not work.
- Pair a lesson with a trouble when the lesson source references the trouble or
  the text clearly describes the resolved prevention rule.
- Do not call Notion from the drain unless the operator or automation mode
  explicitly asks for a reminder ticket. Notion is optional output, never the
  drain brain.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the drain inputs.
   - [ ] Resolve `project_root`; default to the current repo.
   - [ ] Resolve `since`; default to rows not already recorded in processed
     state.
   - [ ] Resolve `cap`; default to 5 follow-ups.
   - [ ] Choose `mode`: `dry-run`, `manual`, or `automation`.
- [ ] 2. Read the learning sources and processed state.
   - [ ] Read `docs/TROUBLES.md` and `docs/LESSONS.md`.
   - [ ] Read `.farplane/state/learning-drain/processed.jsonl` when present.
   - [ ] Also read legacy
     `.farplane/state/self-improve/weekly-drain-processed.jsonl` when present.
- [ ] 3. Normalize candidate rows.
   - [ ] Create stable `doc_ref` values from file, line number, timestamp, and
     content hash.
   - [ ] Classify each row as `trouble`, `lesson`, `paired`, `duplicate`,
     `weak`, `private-risk`, `already-processed`, or `actionable`.
   - [ ] Pair related lesson and trouble rows before deciding follow-ups.
- [ ] 4. Select bounded follow-ups.
   - [ ] Route harness/process behavior gaps to
     [optimize-harness](../optimize-harness/SKILL.md).
   - [ ] Route durable regression behavior to [eval](../eval/SKILL.md).
   - [ ] Route skill-template or registry changes to
     [skill-maintenance](../skill-maintenance/SKILL.md) with
     `mode: harden_skill`.
   - [ ] Create at most `cap` follow-ups; mark overflow as `deferred`.
- [ ] 5. Write processed-state.
   - [ ] In `dry-run`, print the would-write state rows without mutating files.
   - [ ] In `manual` or `automation`, append one JSONL row per processed source
     row with `doc_ref`, `content_hash`, `drained_at`, `disposition`,
     `followup_ref`, `thread_ref`, `ticket_ref`, and `notes`.
   - [ ] Never write raw transcript text or secrets into processed state.
- [ ] 6. Return the drain report.
   - [ ] Include source counts, skipped counts, follow-ups, deferred rows,
     processed-state path, and next action.
   - [ ] Mention whether an automation invoked the skill and keep the
     automation prompt out of the behavioral logic.
- [ ] 7. Finish with eval or validator proof when changing this skill.
   - [ ] Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`
     after skill edits.
   - [ ] Keep `eval_task.json` coverage for dedupe, pairing, cap, and
     automation-as-pointer behavior.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

Return or write:

```text
Learning Drain Report
- mode:
- source files:
- candidate rows:
- skipped rows:
- paired rows:
- harden_skill_handoff:
- other follow-ups:
- deferred rows:
- processed-state path:
- no-change reason:
- next action:
```

Processed-state JSONL row shape:

```json
{
  "schema_version": 1,
  "doc_ref": "docs/TROUBLES.md:42",
  "content_hash": "sha256:...",
  "drained_at": "2026-06-13T00:00:00Z",
  "disposition": "harden-skill-handoff|optimizer-followup|eval-followup|ticket-created|deferred|duplicate|no-change",
  "followup_ref": "skill-maintenance:harden_skill:<short-id>",
  "ticket_ref": "tickets/TASK-0000/ticket.md",
  "thread_ref": "",
  "notes": "compact sanitized reason"
}
```

## Gotchas

- Do not make this a scheduler. Weekly cadence belongs to automation or Goal;
  this skill owns the drain behavior.
- Do not treat this wrapper as the skill-improvement brain. New weekly skill
  upkeep should call `skill-maintenance(mode: harden_skill)`.
- Do not reprocess every row every week. Processed state is the idempotence
  surface.
- Do not let one noisy logger run spawn a flood of hardening or optimizer
  threads.
- Do not call `optimize-harness` for weak rows that only need ordinary memory.
- Do not edit `docs/TROUBLES.md` or `docs/LESSONS.md` except through the
  separate learning logger path.
- Do not treat a Notion ticket as proof that the issue was optimized.

## Reference Map

- [automation prompt](references/automation-prompt.md) - legacy prompt for
  automations that still invoke this wrapper.
- [processed-state rules](references/processed-state.md) - JSONL idempotence,
  hashing, and compatibility details.
- [optimize-harness](../optimize-harness/SKILL.md) - route concrete harness
  behavior gaps into fix/proof/review loops.
- [eval](../eval/SKILL.md) - create durable regression cases when the expected
  behavior is testable.
- [skill-maintenance](../skill-maintenance/SKILL.md) - canonical
  `harden_skill` owner for turning lessons/troubles into evals, gotchas, and
  skill-package changes.
- [docs/TROUBLES.md](../../docs/TROUBLES.md) - raw correction and pain log.
- [docs/LESSONS.md](../../docs/LESSONS.md) - distilled prevention lessons.
