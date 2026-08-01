---
skill: close-ticket
date: 2026-08-02
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/TASK-0422/artifacts/qa/agent-qa/video-first/result.json
after_ref: skills/close-ticket/SKILL.md
reasoning_basis: reviewer
proof_artifacts:
  - tickets/TASK-0422/artifacts/demo/2026-08-02-video-first-preview/review.json
  - tickets/TASK-0422/artifacts/demo/2026-08-02-video-first-preview/github-video-rendered.png
  - https://github.com/ZanarkandTechnologies/Farplane/issues/1#issuecomment-5153011968
eval_required: yes
---

# Close Ticket Authenticated Attachment Retry Audit

## Change

- Before: the skill named browser upload but did not state that `gh auth` and
  browser authentication are separate, implied a stable file input, and did
  not require the issue Proof line to be repaired after upload.
- After: `gh` owns issue text/state, the authenticated web composer owns binary
  attachments, signed-out runs preserve an exact retry point, upload waits for
  a real user-attachment URL, the rendered player is checked, and Proof links
  the canonical demo comment.
- Why: the live canary produced a correct issue and a reviewed local MP4 but
  remained text-only until the browser was authenticated and the semantic file
  chooser path was exercised.
- Tradeoff accepted: binary upload remains browser-bound because GitHub does not
  document an issue-attachment upload API for `gh`; the workflow pauses for
  sign-in instead of introducing an unsafe or storage-heavy fallback.

## First-Principles Reasoning

- Objective: make a feature closeout glanceable on GitHub while retaining safe,
  idempotent local cleanup.
- Placement logic: normal-path responsibility, auth, upload, retry, and proof
  gates belong in first-load `SKILL.md`; reusable falsifiers belong in evals;
  evidence-oriented prevention belongs in `qa_checklist.md`.
- Expected behavior delta: agents no longer treat CLI login as browser login,
  claim `gh --body-file` uploads a binary, abandon the marked issue after
  sign-in, or leave `Demo: pending` after a successful upload.
- Proof needed: JSON/eval validation, skill-system validation, live-copy match,
  bounded agent QA for the two new cases, and independent skill review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | CLI/browser split and complete upload/resume recipe are in `SKILL.md`. |
| `reference_load_precision` | pass | Default path stays first-load; no new reference is required. |
| `missing_context_rate` | pass | Auth, URL, marker, rendered-player, Proof-link, close, and Core gates remain explicit. |
| `noisy_context_rate` | pass | Added only the observed default upload and auth recovery path. |
| `duplicated_instruction_count` | pass | SKILL owns behavior; QA owns evidence checks; README is a short operator summary. |
| `prompt_size_tokens` | unknown | Raw length is diagnostic only; validator/reviewer will judge first-load cost. |
| `task_success_rate` | unknown | Two deterministic source-contract traces pass; real candidate-agent adherence was not proven and is not claimed. |
| `review_tas_rate` | pass | Independent re-review reached TAS-A with no implementation-readiness blockers. |
| `maintenance_locality` | pass | All behavior changes stay inside `skills/close-ticket/`. |
| `composition_clarity` | pass | `gh`, browser composer, remote verification, and Core have distinct ownership. |

## Proof Artifacts

- Skill-local evals: two new cases cover browser sign-in resume and rejection of
  fake `gh` binary upload. Their deterministic stub traces pass 2/2 but are
  explicitly artifact proof, not candidate-agent QA.
- Structure evals: `skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt:
  `tickets/TASK-0422/artifacts/review/2026-08-02-attachment-retry-skill-review.json`
- Validator: pending.
- Eval required: yes; baseline is the prior 3/3 video-first behavior receipt.
  The new cases passed deterministic source-contract tracing 2/2; independent
  evidence review rejected the stronger candidate-agent label. The observed
  live canary separately proves the actual browser attachment mechanism.
- Evidence gaps: full canary close/Core cleanup is separate from this skill
  hardening and remains pending while issue #1 is open.

## Generated Registry Boundary

- `check_skills.py --write` regenerated the shared registries from the entire
  already-dirty workspace. The resulting unrelated rows reflect existing
  user-owned source changes and are not authored, reverted, or claimed by this
  close-ticket hardening.
- The intended generated delta for this skill is only the `close-ticket` row;
  `sync_skill_registry.py --check` passes against current workspace truth.
- Review and staging scope is the owner-local `skills/close-ticket/**` package.
  Shared generated-registry churn remains unstaged so it is not silently
  bundled with this skill change.

## Before Behavior

- A signed-out web composer was reported as a generic blocker despite valid CLI
  auth, and the skill did not say how to resume that exact issue after sign-in.
- The upload recipe assumed a discoverable file input and omitted rendered-media
  verification and Proof-link repair.

## After Behavior

- Preserve issue, packet, and next digest; ask for browser sign-in; resume the
  same marker; activate the semantic file chooser; wait for the user-attachment
  URL; submit once; verify with `gh` and the rendered issue fragment; repair the
  Proof link; then close and hand off to Core.

## Followups

- Finish the live TASK-9006 PNG/close/Core/retry canary before claiming complete
  end-to-end closeout readiness.
