---
name: learning-drain
description: "Turn recent TROUBLES/LESSONS rows into deduped optimizer follow-ups and processed-state records when a weekly learning drain is due."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0039
  - FEAT-0041
allowed-tools: Read, Glob, Grep, Bash
---

# Learning Drain

## Context

Use this skill for the weekly layer after the every-N-turn learning logger has
already written compact rows into `docs/TROUBLES.md` and `docs/LESSONS.md`.

The hot-path hook only logs. This skill drains the logs into action: it reads
recent trouble/lesson rows, dedupes against processed state, pairs related rows,
and creates bounded follow-ups for `optimize-harness`, tickets, evals, or skill
updates when a real harness/process fix is implied.

Automations should be thin pointers to this skill. They should not contain the
drain logic themselves.

## Skill Signature

```text
learning_drain(project_root, since?, cap?, mode?)
  -> optimizer_followups[] + processed_state_delta + no_change_reason?
state: reads(docs/TROUBLES.md, docs/LESSONS.md, .farplane/state/**/processed*.jsonl)
       writes(.farplane/state/learning-drain/processed.jsonl, ticket/thread refs when explicitly created)
gates: docs_present; rows_deduped; cap_respected; no_raw_transcripts; processed_state_written
routes: optimize-harness | eval | skill-maintenance | gap-analysis | direct-summary
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
     [skill-maintenance](../skill-maintenance/SKILL.md).
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
- follow-ups:
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
  "disposition": "optimizer-followup|eval-followup|ticket-created|deferred|duplicate|no-change",
  "followup_ref": "optimize-harness:<short-id>",
  "ticket_ref": "tickets/TASK-0000/ticket.md",
  "thread_ref": "",
  "notes": "compact sanitized reason"
}
```

## Gotchas

- Do not make this a scheduler. Weekly cadence belongs to automation or Goal;
  this skill owns the drain behavior.
- Do not reprocess every row every week. Processed state is the idempotence
  surface.
- Do not let one noisy logger run spawn a flood of optimizer threads.
- Do not call `optimize-harness` for weak rows that only need ordinary memory.
- Do not edit `docs/TROUBLES.md` or `docs/LESSONS.md` except through the
  separate learning logger path.
- Do not treat a Notion ticket as proof that the issue was optimized.

## Reference Map

- [automation prompt](references/automation-prompt.md) - use when installing or
  updating a weekly automation that invokes this skill.
- [processed-state rules](references/processed-state.md) - JSONL idempotence,
  hashing, and compatibility details.
- [optimize-harness](../optimize-harness/SKILL.md) - route concrete harness
  behavior gaps into fix/proof/review loops.
- [eval](../eval/SKILL.md) - create durable regression cases when the expected
  behavior is testable.
- [skill-maintenance](../skill-maintenance/SKILL.md) - apply skill-system and
  registry changes.
- [docs/TROUBLES.md](../../docs/TROUBLES.md) - raw correction and pain log.
- [docs/LESSONS.md](../../docs/LESSONS.md) - distilled prevention lessons.
