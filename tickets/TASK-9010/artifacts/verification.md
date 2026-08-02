---
ticket_id: TASK-9010
artifact_type: verification
status: pass
created_at: 2026-08-02T10:10:00+08:00
---

# Verification

## Result

The first checkpointed visual-reasoning slice works as specified. The helper
preserves the source and immutable lineage, the installed skill selects the
workspace for reference-heavy tasks, and it avoids workspace ceremony for a
simple direct visual answer.

## Deterministic checks

- `python3 -m unittest skills/visual-reasoning/scripts/test_visual_workspace.py`
  passed 5/5 tests.
- `python3 skills/eval/scripts/check_eval_queries.py --root skills/visual-reasoning`
  passed.
- The real-image workspace at `artifacts/qa/example-workspace/` contains three
  checkpoints and two matching operation receipts.
- `source.png` and `checkpoints/000.png` both hash to
  `1cfb26914b02594a7e9f13ce9955c5ea6ccda5cff23cc6b6078f1e0932100eae`.
- `latest.png` and `checkpoints/002.png` both hash to
  `7b0f87e24ed2ed5b74be75deea89783d77c795ccd28a99f049cda44398f256bf`.
- Unit coverage includes initialization, sequential overlays, half-open crop
  dimensions, whole-batch rejection without publication, and gap/missing-
  receipt refusal.

## Behavior evidence

- Dense count behavior trace: TAS-A with a real workspace, checkpoint, count,
  and explicit missed/duplicate verification:
  `.farplane/evals/runs/20260801-224815-task-9010-visual-reasoning-dense-rerun-2/`.
- Installed-skill semantic rerun:
  `.farplane/evals/runs/20260802-014636-task-9010-visual-reasoning-installed-rerun/`.
  Dense counting and tangled-path cases each received TAS-A. The resume case
  created `checkpoints/002.png` plus `operations/002.json`, preserved staged
  `000/001` hashes, reobserved latest, and returned the required receipt; its
  judge process emitted malformed/unfinished output after the agent completed,
  so the completion reviewer owns the substitute evidence judgment.
- Deterministic CV boundary: TAS-A using PIL/NumPy, with mask, pixel counts,
  operation receipt, checkpoint, and an explicit interpretation boundary:
  `.farplane/evals/runs/20260802-011947-task-9010-visual-reasoning-receipt-rerun/`.
- Direct-answer routing: TAS-A without an unnecessary workspace in
  `.farplane/evals/runs/20260802-002033-task-9010-visual-reasoning-semantic-final/`.

The earlier pre-install eval attempts are not acceptance evidence: child Codex
runs had not yet received the repo-owned skill and routed image edits to the
generic image-generation skill. `farplane install` then linked
`visual-reasoning` into the live skill inventory; the installed rerun produced
the expected deterministic routes and receipts.

## Registry and integration

`python3 skills/skill-maintenance/scripts/check_skills.py --write` generated and
validated a 124-row skill registry, passed todo-tier and Tier-0 checks, and
included `visual-reasoning`. The aggregate command exits nonzero only for two
pre-existing out-of-scope surface-budget findings:

- `skills/content-impl-plan/qa_checklist.md`: 19 items, limit 5.
- `skills/content-impl-plan/evals/evals.json`: 19 tasks, limit 5.

No finding points to `skills/visual-reasoning/`.

## Residual risk

- This adapts the report's central reference-externalization idea at the
  harness layer; it does not reproduce trained point/box tokens inside a model.
- Background removal, SAM-style segmentation, OCR, detection, and OpenCV remain
  conditional adapters. The first version bundles no heavy CV dependency.
- Comparative quality lift over language-only reasoning still needs a later
  ablation on representative real tasks.

## Independent review

`artifacts/review/completion-review.md` passes the ticket at overall TAS-A,
with TAS-A for `skill-contract`, `integration-readiness`, and
`evidence-quality`. It accepts the resume artifact trail as substitute evidence
for the malformed judge subprocess and records no blocking findings.

## Complete-phase validation

The final replay of
`farplane validate ticket tickets/TASK-9010/ticket.md --phase complete --path skills/visual-reasoning`
passes `ticket.metadata`, `ticket.reward`, `ticket.completion-evidence`, and
`ticket.visual-companion`. Its only failing block is the aggregate
`skills.check`, which names exclusively the two pre-existing
`content-impl-plan` surface-budget violations recorded above.
