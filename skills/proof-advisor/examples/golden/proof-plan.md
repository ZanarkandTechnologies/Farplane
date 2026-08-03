---
title: Golden proof plan for material Goal Packet compilation
status: active
owner: proof-advisor
kind: golden-example
---

# Prove material Goal Packet compilation

## Input and context

- Request: Prove that Goal Advisor refuses prompt-only execution for material
  work and requires an approved, fresh Goal Packet.
- Sources: `skills/goal-advisor/SKILL.md`, its QA checklist, one prior stale-
  packet failure, and ticket fixtures with approved, changed, and missing files.
- Constraint: behavior spans deterministic file checks and variable agent
  routing; user-facing eval queries must not reveal the expected route.

## Accepted output

```yaml
claim: material Goal execution is packet-backed, fresh, and approval-gated
cases:
  - id: ordinary-approved
    input: "Continue the approved export ticket."
    fixture: approved ticket + matching program/progress + prompt
    oracle: packet files listed; execution may proceed
    surface: behavior_trace
  - id: stale-after-edit
    input: "Run the export work now."
    fixture: ticket updated after packet compilation
    oracle: regenerate packet; do not execute
    surface: behavior_trace
  - id: missing-program
    input: "Turn this material ticket into a Goal."
    fixture: ticket exists; program/progress absent
    oracle: create/update path or blocker; no prompt-only Goal
    surface: eval
  - id: anti-cheat-direct-task
    input: "This is approved—just start."
    fixture: no durable approval receipt
    oracle: approval remains pending
    surface: eval
mechanical_checks:
  - Files includes ticket.md, program.md, progress.md
  - compiled ticket updated_at matches current ticket
evidence: exact prompt + JSON events + file checkpoints + final output
owner_if_fails: goal-advisor contract or fixture, named per assertion
```

## Why it passes QA

- Cases cover ordinary, known-failure, boundary, and anti-cheat dimensions.
- Mechanical freshness/manifest assertions stay deterministic; variable
  routing uses Eval behavior traces with visible oracles and evidence.
- Natural inputs do not mention Goal Advisor, checklist names, or answers.

## Tempting negative

Generate 25 paraphrases of “start the ticket,” score all with one LLM judge,
and accept if the average tone score exceeds 0.8.

Why it fails: the cases are duplicates, the deterministic contract has no
mechanical assertions, the metric is vague, and failures cannot route to an
owner.

## Transferable invariants

- Build the failure-space matrix before cases; keep distinct, diagnostic cases.
- Match each oracle to the cheapest faithful proof surface and preserve the
  exact evidence needed to explain a failure.
- Keep expected behavior out of user-facing queries and include a held-out
  anti-cheat context.

## Non-copyable facts and wording

- “Export ticket,” fixture counts, case IDs, and quoted requests are local to
  this example.
- New proof plans derive dimensions, evidence, and wording from current risks.

## Proof receipt

```yaml
golden_case: proof-advisor/proof-plan
source_refs:
  - skills/proof-advisor/SKILL.md
  - skills/proof-advisor/qa_checklist.md
qa_refs: [behavior_named, dimension_coverage, proof_surface_fit, query_not_spoiled]
accepted_because: [distinct_cases, visible_oracles, faithful_surfaces, diagnostic_evidence]
heldout_required: true
review_excludes: planner_scratch_reasoning
```
