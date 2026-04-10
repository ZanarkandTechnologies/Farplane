---
name: review
description: Run an anchored 1-to-5 rubric review against the active ticket, scoring the right review families and using an anti-slop search playbook for code, UI, evidence, demos, and videos.
---

# Review Skill

Run a ticket-aware, rubric-driven review and return a scored verdict with clear
feedback about whether another pass is required.

## Purpose

Use this skill to review one active ticket by selecting the right rubric
families, inspecting the relevant code/evidence plus the smallest neighboring
surfaces needed to test consistency, and writing a `Review Packet` back into
the ticket.

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
  4. load `references/desloppify.md` when code, integration, cleanup, or evidence trust is in scope
  5. open each selected family file and use its skeptic questions
  6. inspect the changed surface plus the minimum neighboring code/docs/invariants needed to test consistency
  7. rank substantive findings by severity and confidence
  8. score each family on the anchored `1.0`-to-`5.0` scale
  9. explain the findings that prevented a lower or higher adjacent score
  10. write the `Review Packet`
  11. return the scored verdict
- Core decision branches:
  - planning -> `spec-contract` + `implementation-plan`
  - code/backend/api -> `code-quality` + `integration-readiness` + `evidence-quality`
  - UI or user-facing workflow -> `user-intent-satisfaction` + the relevant quality/evidence families
  - cleanup/refactor/runtime/doc simplification -> add `debloatability`
- Top 3 gotchas:
  - do not review before reading the active ticket
  - do not output only questions; return anchored scores, findings, and next actions
  - do not approve weak evidence or weak integration readiness
- Outcome contract:
  - the active ticket contains a `Review Packet`
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
  - `references/user-intent-satisfaction.md`
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
5. For code, cleanup, integration, or evidence-heavy review, open
   `references/desloppify.md`.
6. Read the changed code/evidence plus the smallest neighboring files, docs,
   constants, schemas, or invariants needed to test consistency.
7. Use the family skeptic questions and evidence cues to challenge the work.
8. Rank substantive findings with severity, confidence, and concrete file refs.
9. Score the work against the selected rubric dimensions using the anchored
   `1.0`-to-`5.0` scale.
10. Write a `Review Packet` into the ticket.
11. Return:
   - work_type
   - search_scope
   - overall score
   - overall threshold
   - verdict
   - rerun_required
   - evidence_quality
   - integration_readiness
   - traceability
   - freshness
   - hard-gate failures
   - finding_log
   - rubric-level feedback
   - blocking findings
   - next_action

## Scoring Rules

- Overall verdict is `pass` only if every required rubric meets threshold.
- `evidence-quality` below threshold forces non-pass overall.
- `integration-readiness` below threshold forces non-pass overall.
- select `user-intent-satisfaction` for user-facing completion review when the ticket clearly expresses the intended user ask.
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
Open references/review-rubric-index.md first.
Determine which rubric families apply.
Open references/desloppify.md for code, cleanup, integration, and evidence-heavy review.
Open the matching family reference files.
Use the family skeptic questions, score guide, and evidence cues.
Select the matching rubric families and score the work against them on the anchored 1.0-5.0 scale.

Scope:
- active ticket/work package
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
  "traceability": "fail",
  "freshness": "pass",
  "hard_gate_failures": ["evidence-quality", "integration-readiness"],
  "finding_log": [
    {
      "severity": "high",
      "confidence": "high",
      "rubric": "evidence-quality",
      "summary": "Edge-state claims are not backed by attached proof.",
      "file_refs": ["tickets/TASK-0047-upgrade-review-into-a-desloppify-pass.md"],
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
- [ ] `references/review-rubric-index.md` read first
- [ ] `references/desloppify.md` used when code, integration, cleanup, or evidence trust is in scope
- [ ] matching family reference files used for anchored scoring
- [ ] Correct rubric family/families selected
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

### With Desloppify

Use `references/desloppify.md` as the cross-cutting search playbook when the
ticket could hide AI-slop, invariant drift, dead weight, or shallow repo-local
reasoning behind superficially plausible changed files.
