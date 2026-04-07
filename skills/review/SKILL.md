---
name: review
description: Run a rubric-driven review against the active ticket, selecting the right review families for specs, plans, code, UI, evidence, demos, and videos.
---

# Review Skill

Run a ticket-aware, rubric-driven review and return a scored verdict with clear
feedback about whether another pass is required.

## Purpose

Use this skill to review one active ticket by selecting the right rubric
families, inspecting only the relevant code/evidence, and writing a `Review
Packet` back into the ticket.

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
  4. inspect relevant code/evidence only
  5. score the ticket
  6. write the `Review Packet`
  7. return the scored verdict
- Core decision branches:
  - planning -> `spec-contract` + `implementation-plan`
  - code/backend/api -> `code-quality` + `integration-readiness` + `evidence-quality`
  - UI -> `ui-quality` + `code-quality` + `evidence-quality` plus demo/video when present
  - cleanup/refactor/runtime/doc simplification -> add `debloatability`
- Top 3 gotchas:
  - do not review before reading the active ticket
  - do not collapse QA evidence review into the whole review
  - do not approve weak evidence or weak integration readiness
- Outcome contract:
  - the active ticket contains a `Review Packet`
  - the review returns score, verdict, rerun flag, blocking findings, and next action

## Documentation Index

- Primary rubric map: `references/review-rubric-index.md`
- Secondary lenses from `../code-review/references/`:
  - `planning-rubric.md`
  - `ui-rubric.md`
  - `api-rubric.md`
  - `backend-rubric.md`
  - `code-quality.md`
  - `error-handling.md`
  - `type-design.md`
  - `simplification.md`

## Review Flow

1. Read the active ticket / work package.
2. Open `references/review-rubric-index.md`.
3. Determine which rubric families apply.
4. Read the changed code and/or evidence artifacts relevant to those rubric families.
5. Score the work against the selected rubric dimensions.
6. Write a `Review Packet` into the ticket.
7. Return:
   - overall score
   - verdict
   - rerun_required
   - rubric-level feedback
   - blocking findings
   - next_action

## Agent Delegation

```text
delegate(
  role="code-reviewer",
  tier="THOROUGH",
  prompt="RUBRIC-DRIVEN REVIEW TASK

Read the active ticket first.
Open references/review-rubric-index.md first.
Determine which rubric families apply.
Select the matching rubric families and score the work against them.

Scope:
- active ticket/work package
- changed files and evidence artifacts

Return:
- rubrics_used
- overall_score
- verdict (pass|revise|block)
- rerun_required
- rubric_sections with score/threshold/pass/findings/next_action
- blocking_findings
- next_action"
)
```

## Output Format

```json
{
  "rubrics_used": ["ui-quality", "evidence-quality", "integration-readiness"],
  "summary": "Core flow works, but evidence and integration confidence are weak.",
  "overall_score": 78,
  "overall_threshold": 85,
  "verdict": "revise",
  "rerun_required": true,
  "rubric_sections": [
    {
      "name": "evidence-quality",
      "score": 2.5,
      "threshold": 4.0,
      "pass": false,
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
- [ ] Correct rubric family/families selected
- [ ] Ticket/spec compliance checked before code-quality nitpicks
- [ ] Relevant code/evidence actually inspected
- [ ] Verdict is explicit: `pass`, `revise`, or `block`
- [ ] `rerun_required` is explicit
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
