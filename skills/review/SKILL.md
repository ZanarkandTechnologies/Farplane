---
name: review
description: Run an anchored 1-to-5 rubric review against the active ticket, scoring the right review families and using an anti-slop search playbook for code, UI, evidence, demos, and videos.
---

# Review Skill

Run a ticket-aware, rubric-driven review and return a scored verdict with clear
feedback about whether another pass is required.

## Purpose

Use this skill to review one active ticket by reading its `Proof Contract`,
selecting the right rubric families, inspecting the relevant code/evidence plus
the smallest neighboring surfaces needed to test consistency, and producing a
structured review result that the ticket links from `Evidence`.

This skill uses the anchored `1.0`-to-`5.0` review contract:

- `1.0`: failing, unsafe, contradictory, or largely absent
- `2.0`: partially relevant work exists, but trust is low because key claims
  still depend on inference, thin proof, or unresolved defects
- `3.0`: acceptable and directionally correct, but still ordinary, caveated, or
  incomplete in ways a skeptical reviewer would notice
- `4.0`: strong and trustworthy with only minor caveats; good enough to pass a
  `4.0` threshold when no hard gate fails
- `5.0`: exemplary, persuasive, and hard to improve materially within scope

Calibration rules:

- score `2.0` when the work has moved beyond total failure but is still not
  close to review-ready trust
- score `4.0` only when you would defend the result to a skeptical human
  reviewer without needing to add major caveats
- score `5.0` sparingly; it should require obvious positive evidence, not mere
  absence of defects

## First-Load Checklist

Ensure an agent can execute the core path after only reading this file.

- Trigger conditions:
  - after implementing a selected ticket
  - after writing a ticket plan that needs challenge/review
  - before claiming a ticket is ready for Stop-hook completion
  - whenever the user asks for review
- Workflow:
  1. read the active ticket
  2. read the ticket `Proof Contract` for declared metrics, rubric families,
     thresholds, hard gates, required evidence, and optional autoresearch session
  3. open the rubric index
  4. choose the matching rubric families, starting from the ticket-declared gates
  5. load `references/desloppify.md` when code, integration, cleanup, or evidence trust is in scope
  6. open each selected family file and use its skeptic questions
  7. inspect the changed surface plus the minimum neighboring code/docs/invariants needed to test consistency
  8. check metric traceability: declared metric -> verify command/result -> evidence artifact
  9. rank substantive findings by severity and confidence
  10. score each family on the anchored `1.0`-to-`5.0` scale
  11. explain the findings that prevented a lower or higher adjacent score
  12. write the structured review result
  13. return the scored verdict
- Core decision branches:
  - planning -> `spec-contract` + `implementation-plan`
  - code/backend/api -> `code-quality` + `integration-readiness` + `evidence-quality`
  - UI or user-facing workflow -> `user-intent-satisfaction` + the relevant quality/evidence families
  - UI source review -> add `ui-quality` + `frontend-guidelines` and run `web-design-guidelines` on changed UI files when source is available
  - `$ralph` or unattended-run work -> include autonomy-readiness checks in
    `implementation-plan`, `integration-readiness`, and `evidence-quality`
  - cleanup/refactor/runtime/doc simplification -> add `debloatability`
- Top 3 gotchas:
  - do not review before reading the active ticket and its `Proof Contract`
  - do not output only questions; return anchored scores, findings, and next actions
  - do not approve weak evidence or weak integration readiness
- Outcome contract:
  - the active ticket links the review result from `Evidence`
  - the review returns anchored scores, search scope, severity-ranked findings,
    verdict, rerun flag, hard-gate failures, blocking findings, and next action

## Documentation Index

- Primary rubric map: `references/review-rubric-index.md`
- Cross-cutting search playbook:
  - `references/desloppify.md`
- Family references:
  - `references/spec-contract.md`
  - `references/implementation-plan.md`
  - `references/code-quality.md`
  - `references/ui-quality.md`
  - `references/frontend-guidelines.md`
  - `references/user-intent-satisfaction.md`
  - `references/evidence-quality.md`
  - `references/demo-quality.md`
  - `references/video-quality.md`
  - `references/integration-readiness.md`
  - `references/debloatability.md`

## Review Flow

1. Read the active ticket first.
2. Read the ticket `Proof Contract`, including declared metrics, review rubric
   gates, hard gates, required evidence, and optional autoresearch session.
3. Open `references/review-rubric-index.md`.
4. Determine which rubric families apply, starting from ticket-declared rubric gates.
5. Open the reference file for each selected rubric family.
6. For code, cleanup, integration, or evidence-heavy review, open
2. Open `references/review-rubric-index.md`.
3. Determine which rubric families apply.
4. Open the reference file for each selected rubric family.
   - for UI source review, also open `references/frontend-guidelines.md`
5. For code, cleanup, integration, or evidence-heavy review, open
   `references/desloppify.md`.
7. Read the changed code/evidence plus the smallest neighboring files, docs,
   constants, schemas, or invariants needed to test consistency.
8. Use the family skeptic questions and evidence cues to challenge the work.
9. Check metric claims separately from rubric scores. Metrics are mechanical
   signals; rubrics are review judgment frames. A good number does not excuse
   weak evidence or integration readiness.
10. Rank substantive findings with severity, confidence, and concrete file refs.
11. Score the work against the selected rubric dimensions using the anchored
   `1.0`-to-`5.0` scale.
12. Write the review result and make sure the ticket links it from `Evidence`.
13. Return:
   - work_type
   - search_scope
   - overall score
   - overall threshold
   - verdict
   - rerun_required
   - evidence_quality
   - integration_readiness
   - metric_traceability
   - traceability
   - freshness
   - hard-gate failures
   - finding_log
   - rubric-level feedback
   - blocking findings
   - next_action

When Stop hook requests visible completion review with a nonce, also write a
ticket-scoped completion receipt under
`tickets/TASK-XXXX/artifacts/review/<timestamp>-completion-receipt.json` and
link it from the ticket `Evidence` section. That receipt should include:

- `receipt_type: "completion_review"`
- `ticket_id`
- `nonce`
- `reviewed_at`
- `reviewer_mode: "visible_review_lane"`
- `reviewed_artifacts`
- `verdict`
- `satisfies_user_query`
- `user_query_reason`
- `obvious_next_step`
- `review_artifact`

The calling lane should then use that same nonce as the one-time completion
password in its next final response:

- `COMPLETION_PASSWORD: <nonce>`

## Scoring Rules

- Overall verdict is `pass` only if every required rubric meets threshold.
- Ticket-declared rubric gates in the `Proof Contract` are minimum review
  obligations. The reviewer may add relevant families, but must not drop a
  declared hard gate without recording why the ticket contract is wrong.
- `evidence-quality` below threshold forces non-pass overall.
- `integration-readiness` below threshold forces non-pass overall.
- Missing, stale, unparseable, or untraceable ticket-declared metric evidence
  forces non-pass when the metric is required for completion.
- When the selected ticket already defines a coherent scope, treat artificial
  downscoping to a smaller internal "first slice" as a planning/execution
  failure unless the ticket or blockers made that narrower boundary explicit.
- For `$ralph` or long-running autonomous work, missing or vague
  `Autonomy Readiness` is an integration/evidence risk, not a cosmetic docs
  nit.
- select `user-intent-satisfaction` for user-facing completion review when the ticket clearly expresses the intended user ask.
- select `frontend-guidelines` for UI source review and record whether `web-design-guidelines` passed, failed, or was skipped with a concrete reason.
- `block` is reserved for materially unsafe, off-target, or contradictory work.
- `revise` is the default when the work is directionally correct but not yet ready.
- Do not emit a score without evidence from inspected code, artifacts, or the ticket.
- Do not stop at the changed file when neighboring constants, docs, invariants,
  or interfaces could invalidate the claim.
- Prefer high-signal findings about bugs, regressions, inconsistency, contract
  drift, dead weight, and weak evidence over cosmetic commentary.
- Do not assign `2.0` or `4.0` by vibes alone; explain what separates the
  chosen score from the adjacent band.
- Do not bluff willingness-to-pay, competitor strength, or market-value judgments unless the ticket/spec actually carries explicit evidence for them.

## Agent Delegation

```text
delegate(
  role="code-reviewer",
  tier="THOROUGH",
  prompt="RUBRIC-DRIVEN REVIEW TASK

Read the active ticket first.
Read the ticket Proof Contract for metrics, rubric gates, hard gates, required evidence, and optional autoresearch session.
Open references/review-rubric-index.md before scoring.
Determine which rubric families apply, starting from ticket-declared gates.
Open references/desloppify.md for code, cleanup, integration, and evidence-heavy review.
Open the matching family reference files.
Use the family skeptic questions, score guide, and evidence cues.
Select the matching rubric families and score the work against them on the anchored 1.0-5.0 scale.
Check metric traceability separately from rubric scores when the ticket declares metrics.

Scope:
- active ticket
- changed files and evidence artifacts
- the minimum neighboring files, invariants, docs, or constants needed to test consistency and integration risk

Return:
- work_type
- search_scope
- rubrics_used
- overall_score (1.0-5.0)
- overall_threshold
- verdict (pass|revise|block)
- rerun_required
- evidence_quality (pass|fail)
- integration_readiness (pass|fail)
- traceability (pass|fail)
- freshness (pass|fail)
- hard_gate_failures
- finding_log with severity/confidence/rubric/summary/file_refs/evidence/next_action
- rubric_sections with score/threshold/pass/dimension_scores/findings/next_action
- blocking_findings
- next_action"
)
```

## Output Format

```json
{
  "work_type": ["backend"],
  "search_scope": {
    "changed_files": ["src/review.ts"],
    "related_files": ["src/reviewTypes.ts", "docs/specs/review-gates.md"],
    "invariants_checked": ["MEM-0006"],
    "docs_checked": ["skills/review/references/code-quality.md"]
  },
  "rubrics_used": ["code-quality", "evidence-quality", "integration-readiness"],
  "summary": "Core flow works, but evidence and integration confidence are weak.",
  "overall_score": 3.6,
  "overall_threshold": 4.0,
  "verdict": "revise",
  "rerun_required": true,
  "evidence_quality": "fail",
  "integration_readiness": "fail",
  "metric_traceability": "not_applicable",
  "traceability": "fail",
  "freshness": "pass",
  "hard_gate_failures": ["evidence-quality", "integration-readiness"],
  "finding_log": [
    {
      "severity": "high",
      "confidence": "high",
      "rubric": "evidence-quality",
      "summary": "Edge-state claims are not backed by attached proof.",
      "file_refs": ["tickets/archive/TASK-0047/ticket.md"],
      "evidence": [
        "The ticket claims broader coverage than the attached artifacts prove."
      ],
      "next_action": "Capture the missing edge-state artifacts before rerunning review."
    }
  ],
  "rubric_sections": [
    {
      "name": "evidence-quality",
      "score": 2.8,
      "threshold": 4.0,
      "pass": false,
      "dimension_scores": {
        "sufficiency": 3.0,
        "traceability": 2.0,
        "inspectability": 3.0
      },
      "findings": [
        "Primary interaction is described, but the ticket does not attach proof for edge states."
      ],
      "next_action": "Capture proof for the missing edge states and attach it to the ticket."
    }
  ],
  "blocking_findings": [
    "Missing proof for the empty state and regression behavior."
  ],
  "next_action": "Run another build pass focused on the unproven states, then re-run QA and review."
}
```

## Required Checklist

- [ ] Active ticket read first
- [ ] Ticket `Proof Contract` read before selecting rubrics
- [ ] `references/review-rubric-index.md` read before scoring
- [ ] `references/desloppify.md` used when code, integration, cleanup, or evidence trust is in scope
- [ ] matching family reference files used for anchored scoring
- [ ] `references/frontend-guidelines.md` used when UI source files changed
- [ ] Correct rubric family/families selected
- [ ] Ticket-declared rubric gates and hard gates honored or explicitly challenged
- [ ] Metric claims checked for traceability when the Proof Contract declares metrics
- [ ] Ticket/spec compliance checked before code-quality nitpicks
- [ ] Relevant code/evidence actually inspected
- [ ] Neighboring surfaces searched when consistency or contract drift could exist
- [ ] Scores use the anchored `1.0`-to-`5.0` scale, not percentages
- [ ] `2.0` and `4.0` are justified with concrete reasoning, not interpolation by vibe
- [ ] Verdict is explicit: `pass`, `revise`, or `block`
- [ ] `rerun_required` is explicit
- [ ] Completion-gate fields are explicit when evidence is in scope
- [ ] Substantive findings include severity or priority, concrete file refs, and a next action
- [ ] `next_action` is concrete
- [ ] Review result written and linked from the ticket `Evidence` section

## Use with the Loop

### With Work

Use this after the builder pass and before the Stop hook accepts completion.

### With Planning

Use this to challenge a plan before implementation begins.

### With QA

Use QA artifacts as evidence, but do not let the reviewer substitute for QA.

### With Debloating

Use this to identify dead code, stale compatibility layers, duplicated docs, or
runtime surfaces that no longer earn their keep.

### With Desloppify

Use `references/desloppify.md` as the cross-cutting search playbook when the
ticket could hide AI-slop, invariant drift, dead weight, or shallow repo-local
reasoning behind superficially plausible changed files.
