---
name: review
description: Run an anchored 1-to-5 rubric review against the active ticket, scoring the right review families for specs, plans, code, UI, evidence, demos, and videos.
---

# Review Skill

Run a ticket-aware, rubric-driven review and return a scored verdict with clear
feedback about whether another pass is required.

## Purpose

Use this skill to review one active ticket by selecting the right rubric
families, inspecting only the relevant code/evidence, and writing a `Review
Packet` back into the ticket.

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
  - after implementing a work package
  - after writing a plan that needs challenge/review
  - before claiming a ticket is ready for Stop-hook completion
  - whenever the user asks for review
- Workflow:
  1. read the active ticket
  2. open the rubric index
  3. choose the matching rubric families
  4. open each selected family file and use its skeptic questions
  5. inspect relevant code/evidence only
  6. score each family on the anchored `1.0`-to-`5.0` scale
  7. explain the findings that prevented a lower or higher adjacent score
  8. write the `Review Packet`
  9. return the scored verdict
- Core decision branches:
  - planning -> `spec-contract` + `implementation-plan`
  - code/backend/api -> `code-quality` + `integration-readiness` + `evidence-quality`
  - UI -> `ui-quality` + `code-quality` + `evidence-quality` plus demo/video when present
  - cleanup/refactor/runtime/doc simplification -> add `debloatability`
- Top 3 gotchas:
  - do not review before reading the active ticket
  - do not output only questions; return anchored scores, findings, and next actions
  - do not approve weak evidence or weak integration readiness
- Outcome contract:
  - the active ticket contains a `Review Packet`
  - the review returns anchored scores, verdict, rerun flag, hard-gate
    failures, blocking findings, and next action

## Documentation Index

- Primary rubric map: `references/review-rubric-index.md`
- Family references:
  - `references/spec-contract.md`
  - `references/implementation-plan.md`
  - `references/code-quality.md`
  - `references/ui-quality.md`
  - `references/evidence-quality.md`
  - `references/demo-quality.md`
  - `references/video-quality.md`
  - `references/integration-readiness.md`
  - `references/debloatability.md`

## Review Flow

1. Read the active ticket / work package.
2. Open `references/review-rubric-index.md`.
3. Determine which rubric families apply.
4. Open the reference file for each selected rubric family.
5. Read the changed code and/or evidence artifacts relevant to those rubric
   families.
6. Use the family skeptic questions and evidence cues to challenge the work.
7. Score the work against the selected rubric dimensions using the anchored
   `1.0`-to-`5.0` scale.
8. Write a `Review Packet` into the ticket.
9. Return:
   - overall score
   - overall threshold
   - verdict
   - rerun_required
   - evidence_quality
   - integration_readiness
   - traceability
   - freshness
   - hard-gate failures
   - rubric-level feedback
   - blocking findings
   - next_action

## Scoring Rules

- Overall verdict is `pass` only if every required rubric meets threshold.
- `evidence-quality` below threshold forces non-pass overall.
- `integration-readiness` below threshold forces non-pass overall.
- `block` is reserved for materially unsafe, off-target, or contradictory work.
- `revise` is the default when the work is directionally correct but not yet ready.
- Do not emit a score without evidence from inspected code, artifacts, or the ticket.
- Do not assign `2.0` or `4.0` by vibes alone; explain what separates the
  chosen score from the adjacent band.

## Agent Delegation

```text
delegate(
  role="code-reviewer",
  tier="THOROUGH",
  prompt="RUBRIC-DRIVEN REVIEW TASK

Read the active ticket first.
Open references/review-rubric-index.md first.
Determine which rubric families apply.
Open the matching family reference files.
Use the family skeptic questions, score guide, and evidence cues.
Select the matching rubric families and score the work against them on the anchored 1.0-5.0 scale.

Scope:
- active ticket/work package
- changed files and evidence artifacts

Return:
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
- rubric_sections with score/threshold/pass/dimension_scores/findings/next_action
- blocking_findings
- next_action"
)
```

## Output Format

```json
{
  "rubrics_used": ["ui-quality", "evidence-quality", "integration-readiness"],
  "summary": "Core flow works, but evidence and integration confidence are weak.",
  "overall_score": 3.6,
  "overall_threshold": 4.0,
  "verdict": "revise",
  "rerun_required": true,
  "evidence_quality": "fail",
  "integration_readiness": "fail",
  "traceability": "fail",
  "freshness": "pass",
  "hard_gate_failures": ["evidence-quality", "integration-readiness"],
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
- [ ] `references/review-rubric-index.md` read first
- [ ] matching family reference files used for anchored scoring
- [ ] Correct rubric family/families selected
- [ ] Ticket/spec compliance checked before code-quality nitpicks
- [ ] Relevant code/evidence actually inspected
- [ ] Scores use the anchored `1.0`-to-`5.0` scale, not percentages
- [ ] `2.0` and `4.0` are justified with concrete reasoning, not interpolation by vibe
- [ ] Verdict is explicit: `pass`, `revise`, or `block`
- [ ] `rerun_required` is explicit
- [ ] Completion-gate fields are explicit when evidence is in scope
- [ ] `next_action` is concrete
- [ ] `Review Packet` written back into the ticket

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
