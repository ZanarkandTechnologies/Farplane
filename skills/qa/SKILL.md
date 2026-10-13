---
name: qa
description: "Use for \"test this\", \"QA this feature\", \"does the UI look right\" or \"try to break it\": claim-matched evidence, a validated QA receipt and verdict, plus the closeout demo once QA passes."
source: local
department: delivery
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# QA

## Context

Use `qa` when built work needs proof against one GitHub issue's `Done / Proof`
and `QA Strategy`: capture evidence, judge UI against `design.md`, attack a
claim, or record the closeout demo after a pass. It does not plan
(`impl-plan`), write eval rows (`eval`), check outbound copy
(`outbound-check`), or give the completion verdict (`review`). Builder ≠
tester ≠ judge: `qa-tester` operates the browser, and no lane approves
evidence it produced.

## Skill Signature

```text
qa(target, mode?: functional | visual | adversarial, closeout?: demo)
  -> result.json + report.md + best_evidence + verdict + learning
reads: issue body and comments, design.md for UI, runtime handoff, docs/qa runbook, captures
does: binds the proof policy, captures claim-matched evidence, judges it, validates the receipt
writes: .farplane/qa/<issue>/<run>/ artifacts; one gh issue comment with verdict and evidence
returns: QA_RESULT line, validated result.json, verdict, learning outcome
```

Default mode is `functional`; UI work adds `visual` judgment after capture.
`adversarial` runs on `agent_qa` proof weight, "try to break it", `$test`, or a
serious readiness claim. `closeout: demo` runs only after a pass.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the issue, proof policy, and runtime.**
  `issue + override? -> effective_proof_policy + runtime_target + mode | non-pass`

  Rule: The effective policy is the issue's `Done / Proof`, `QA Strategy`,
  optional `Agent Contract`, and `design.md`, plus a caller override that may
  tighten, never erase, obligations. Bind browser/API runtime from the issue,
  the caller handoff, or a verified `docs/qa/*.md` runbook; never guess a port,
  URL, account, fixture, or stale session. Retired sections (`Plan`,
  `Acceptance Criteria`, `Evidence`, `State`) are not QA truth.

  Assert:
  - A missing issue, policy, or runtime returns a non-pass receipt, not a
    judgment of loose logs.
- [ ] **N2 — functional: capture claim-matched evidence through the real mechanism.**
  `policy + runtime -> .farplane/qa/<issue>/<run>/ evidence | source gap`

  Rule: Use the runbook's fast entry, seed, or reset before exploring; it
  speeds capture, it does not prove the run. CLI proof uses commands, exit
  status, logs, files; API proof responses and traces; browser/UI proof
  screenshots, snapshot, console, page errors, via `qa-tester` on material
  work. Exercise the riskiest failure or stale-state path too. An unavailable
  external source stays a named gap beside the local checks that ran.

  Example: provider API down -> local check passes -> verdict `blocked` with a
  provider-observation blocker; never a zero or invented observation.

  Assert:
  - Every `Done` and `QA Strategy` obligation maps to `PASS | FAIL |
    not_provable` plus a concrete artifact path.
  - Three interaction cycles without a new declared state stop with a failure
    bundle and one testability request.
- [ ] **N3 — visual: judge captured UI against design.md with the four-part report.**
  `screenshots + DOM facts + design.md -> per-state report + design coverage + best image`

  Rule: For each declared state write Expected UI Spec, Observed Snapshot
  Report, Diff Report + Verdict, and Fix Plan. Geometry comes from DOM facts
  (bounding boxes as viewport percentages), not eyeballing. The first viewport
  proves only that viewport: scroll, hover, error, mobile, and theme states
  need their own capture; long pages need an operated scroll-to-bottom, desktop
  and mobile full-page captures, and readable top/middle/bottom frames.
  Artifact beats summary: a review score or clean log never overrides a failed
  veto in the screenshot. Load [visual](references/visual.md).

  Assert:
  - Each `design.md` ID has `-> evidence path -> PASS|FAIL|not_provable`; an
    uncovered required section is non-pass.
  - No image of the declared state means no visual pass.
- [ ] **N4 — adversarial: attack the claim with separate tester and judge lanes.**
  `claim + target -> claim_under_test + 2-4 cases + tester report + evidence review`

  Rule: Write `Claim:` and `Would fail if:` first; every case names the claim
  it tests and its falsifier. The tester lane collects artifacts and cannot
  self-approve; a separate evidence-review lane attacks scope mismatch, weak
  artifacts, and unsupported claims. Rerun on weak evidence, fix on wrong
  behavior, stop when a loop adds nothing new; a narrower passing slice never
  passes the original claim. Load [adversarial](references/adversarial.md);
  experiments add [scientific claim review](references/scientific-claim-review.md);
  case design and `behavior_trace` come from [eval](../eval/SKILL.md).

  Assert:
  - The verdict comes from the evidence-review lane, not the tester or builder.
- [ ] **N5 — Write and validate the receipt.**
  `evidence + judgments -> report.md + result.json + QA_RESULT | invalid`

  Rule: `report.md` holds the tested path, obligation-to-evidence map, UI
  `Design coverage` table, rationale, blockers, residual risk, and learning.
  Write `result.json` from the template, then run
  `python3 skills/qa/scripts/validate_qa_result.py <result.json>`. A read-only
  preview emits the schema inline (`evidence=inline-result.json`), lists only
  existing artifacts, and uses `best_evidence: null` when evidence is absent.

  Assert:
  - The validator exits 0; never invent commands, captures, judgments, or
    future paths to satisfy the schema.
- [ ] **N6 — Post to the issue and classify learning.**
  `validated receipt -> gh issue comment + learning outcome`

  Rule: Post one `gh issue comment <n> --body-file` with verdict, receipt
  summary, and strongest evidence attached (a local path is not shared).
  Learning is `ticket_only` (one-off), `cookbook_update` (verified reusable
  route + runbook ref), or `instrumentation_ticket` (missing hook); a candidate
  shortcut stays `ticket_only` until a run verifies it.

  Assert:
  - A read-only preview describes this writeback without claiming it ran.
- [ ] **N7 — closeout: record the Before/After/Example demo after QA passes.**
  `passing result.json + verified evidence -> final.mp4 + evidence-map.json | blocked`

  Rule: `feature` issues, material Goals and `$demo` only. QA must pass first;
  every claim cites an evidence-map entry; no generated visuals stand in for
  product proof. Render via `/pr-to-video` or `/hyperframes`, probe the media,
  get independent TAS-A review, put it on the repo's `demos` pre-release with
  `scripts/demo_shelf.py upload`, and lead the closing proof comment with the
  `🎬 Demo:` line it prints. Load [closeout demo](references/closeout-demo.md).

  Assert:
  - A non-pass QA result returns a blocker routed back to N2 or N3.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

`report.md` opens with `Ticket / Proof Policy: <issue ref> / <policy>` and
`Verdict: pass | revise | fail | blocked | not_provable`. Canonical
`result.json` (every field required):

```json
{"schema_version": "1", "ticket_id": "ZanarkandTechnologies/Farplane#41",
 "phase": "qa", "proof_type": "ui", "runtime_target": "http://127.0.0.1:3000",
 "proof_policy": "Done + QA Strategy + visual", "verdict": "pass",
 "summary": "qa proved the required behavior",
 "gate_results": {"contract": "pass", "mechanism": "pass", "journey": "pass",
                  "adversarial": "pass", "receipt": "pass"},
 "best_evidence": ".farplane/qa/41/run/screens/final.png",
 "artifacts": [".farplane/qa/41/run/report.md", ".farplane/qa/41/run/screens/final.png"],
 "blockers": [], "residual_risk": [],
 "judgment_receipts": [".farplane/qa/41/run/visual.md"],
 "learning": {"outcome": "ticket_only", "ref": null}}
```

## Gotchas

- A `qa-tester` capture run that also "approves" the UI skipped N3; capture is
  not judgment. A hero-only image passed as long-page proof never saw the
  objection section.
- Pointing `QA_RESULT evidence=` at `best_evidence`: it names the validated
  `result.json` receipt.
- Writing per-run files into `tickets/`: issues are GitHub Issues; files go to
  `.farplane/qa/<issue>/<run>/` and the verdict goes on the issue.

## Reference Map

- [guide](references/guide.md) - routes, browsers, evidence, receipt, learning.
- [runbooks](references/runbooks.md), [template](references/runbook-template.md),
  [UI browser proof](references/ui-browser-proof.md) - reusable `docs/qa` pages.
- [visual](references/visual.md) - four-part report, geometry, coverage, review.
- [adversarial](references/adversarial.md),
  [scientific claim review](references/scientific-claim-review.md) - lanes,
  cases, rerun loop, prompts, experiment diagnosis.
- [closeout demo](references/closeout-demo.md) - gates, story spine, render.

## Output

Executed QA writes `report.md`, `result.json`, and supporting artifacts under
`.farplane/qa/<issue>/<run>/`, posts the verdict on the issue, and finishes:

```text
QA_RESULT: verdict=<pass|revise|fail|blocked|not_provable> evidence=<result.json path> reason=<short reason>
```

`scripts/validate_qa_result.py` enforces the [receipt
invariants](references/guide.md#receipt-invariants); a structurally valid pass
can still be rejected by final review as too weak.
