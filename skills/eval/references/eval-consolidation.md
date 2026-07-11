---
title: Eval Consolidation
owner: skills/eval
status: active
created_at: 2026-06-13
updated_at: 2026-06-13
---

# Eval Consolidation

Use this reference when running the weekly eval drain or revising eval files
that have accumulated redundant lesson/trouble-derived coverage.

## Lifecycle Rule

Immediate eval creation is the safety net. Do not delay a testable
lesson/trouble-derived regression until the weekly drain.

```text
lesson_or_trouble -> optimize_harness -> immediate evals/evals.json row
weekly_eval_drain -> fetch changed eval files -> consolidate(..., structure = eval_suite) per file
```

The eval drain exists to reduce noise after coverage exists. It should produce
fewer, stronger rows only when the merged row preserves the same visible
failure modes.

## Automation Shape

```text
eval_drain_automation(project_root, processed_state, cap?)
  -> changed_eval_files + consolidation_reports + processed_state_delta

fetch_evals_edited_since_last_run(project_root, processed_state)
  -> changed_eval_files + content_hashes

for each changed_eval_file:
  consolidate(
    target = changed_eval_file,
    structure = eval_suite,
    constraints = { preserve_evidence: true }
  )
    -> unit_decisions + less_noisy_eval_rows + archive_notes + lost_coverage_risks
```

Run discovery with:

```bash
python3 skills/eval/scripts/fetch_evals_edited_since_last_run.py \
  --project-root . \
  --state .farplane/state/eval-drain/processed.jsonl \
  --pretty
```

## Consolidate Binding

For each changed `skills/<skill>/evals/evals.json`, use the shared
`consolidate` frame with eval-specific bindings:

```text
target = skills/<skill>/evals/evals.json
structure = eval_suite
unit = eval_case
constraints = {
  preserve_evidence: true,
  preserve_ids: true,
  owner_boundary: "owning skill evals/evals.json"
}
value_function = default consolidate value
               + distinct_failure_mode
               + hardcase_value
               + judgeability
               - query_noise
               - duplicate_coverage
```

Map `consolidate` actions into eval dispositions:

- `keep`: unique failure mode, hardcase, or high-signal boundary case.
- `merge`: rows test the same behavior with superficial query differences.
- `rewrite`: row is valuable but noisy, unrealistic, vague, or overfit.
- `move`: row belongs in another skill or workflow eval file.
- `delete`: row is fully covered by a stronger replacement and archive notes
  preserve the old ID and failure mode.
- `defer`: coverage risk is ambiguous and needs human or reviewer judgment.

Prefer the newer eval when it captures a real recent miss and is not merely a
wording variant. Older evals should survive only when they cover a distinct
behavior, boundary, owner surface, or hardcase value.

## Subagent Prompt

Use this prompt shape for each changed eval file:

```text
Context:
- Ticket: tickets/TASK-0200/ticket.md
- Eval file: <skills/name/evals/evals.json>
- Guide: skills/eval/references/eval-consolidation.md
- Rubric: skills/eval/references/eval-writing-rubric.md

Task:
Run consolidate(target = <eval file>, structure = eval_suite). Review only this
eval file and the listed references. Produce a consolidation report with:
- keep_ids
- merge_groups with replacement row drafts
- rewrite_ids with revised row drafts
- archive_notes mapping superseded IDs to replacements
- lost_coverage_risks
- final recommendation: apply | revise | defer

Rules:
- Do not delay immediate eval creation.
- Do not remove unique hardcases or distinct failure modes.
- Favor less noisy evals, not fewer evals at any cost.
- Keep task JSON schema simple and runnable.
- Do not edit unrelated files.
```

## Report Shape

```json
{
  "schema_version": 1,
  "eval_file": "skills/eval/evals/evals.json",
  "keep_ids": ["eval_hardcase_metadata_01"],
  "merge_groups": [
    {
      "source_ids": ["eval_a", "eval_b"],
      "replacement_id": "eval_stronger_behavior_01",
      "rationale": "Both rows test the same visible behavior.",
      "replacement_row": {}
    }
  ],
  "rewrite_ids": [],
  "archive_notes": [
    {
      "old_id": "eval_a",
      "disposition": "merged",
      "replacement_id": "eval_stronger_behavior_01",
      "preserved_failure_mode": "reject vague eval tasks"
    }
  ],
  "lost_coverage_risks": [],
  "recommendation": "apply"
}
```

## Processed State

After accepted consolidation, append one JSONL row per processed eval file:

```json
{
  "schema_version": 1,
  "eval_ref": "skills/eval/evals/evals.json",
  "content_hash": "sha256:...",
  "drained_at": "2026-06-13T00:00:00Z",
  "disposition": "consolidated|kept|deferred|no-op",
  "report_ref": "tickets/TASK-0200/artifacts/eval-drain/eval.json",
  "notes": "compact sanitized reason"
}
```

Use content hashes for idempotence. Filesystem mtimes are discovery hints only.
