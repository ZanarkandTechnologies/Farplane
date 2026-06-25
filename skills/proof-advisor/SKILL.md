---
name: proof-advisor
description: "Turn behavior claims into proof plans, high-quality cases, proof-surface choices, and execution handoffs."
tier: 2
source: local
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.1.0"
  skill-qa-checklist: "0.1.0"
eval: eval_task.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash

---

# Proof Advisor

## Context

Use this skill when the hard part is deciding how to prove a behavior claim:
what cases matter, what oracle can judge them, which proof surface should run,
and what evidence would make the result trustworthy.

This skill owns proof selection and proof-case design. It does not execute
every proof surface itself. Deterministic behavior should become code, schema,
fixture, unit, integration, contract, browser, or validator checks when
possible. AI, prompt, agent, and skill behavior should become eval rows,
model/human judge criteria, `agent-behavior-test`, or `agent-qa-test` when
output variation or multi-step behavior is the thing being tested.

## Skill Signature

```text
proof_advice(claim_or_behavior, risk_context?, source_material?, proof_goal?)
  -> proof_plan
   + case_matrix
   + selected_cases
   + proof_surface_map
   + handoff
   + qa_verdict

state:
  reads(local contracts, tickets/specs, logs/traces/failures, existing tests,
        eval_task.json files, QA checklists, external source notes when needed)
  writes(proof plan, case matrix, eval rows, test-case drafts, QA findings,
         or handoff notes)

gates:
  target_behavior_named; source_material_classified; oracle_defined;
  cases_distinct_and_judgeable; proof_surface_fit; anti-cheat_reviewed

routes:
  testing | eval | agent-qa-test | agent-behavior-test | qa | visual-qa |
  skill-maintenance | review

fails:
  many_near_duplicate_cases; happy_path_only; vague_quality_case;
  query_teaches_answer; subjective_case_without_judge_criteria;
  deterministic_behavior_sent_to_llm_judge; no_failure_mode
```

## Phase Boundary

Run grounding and proof-case design inline by default. Route to:

- `testing` when the next step is choosing or running the proof command.
- `eval` when selected cases should become runnable eval rows or judge prompts.
- `agent-qa-test` when the claim needs tester evidence plus evidence review.
- `skill-maintenance` when case findings should harden a skill checklist,
  `eval_task.json`, or gotcha.
- `review` when a material case suite or reusable rubric needs independent
  judgment.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Name the target behavior and failure risk.
  - [ ] State what a good proof would establish, and what it would falsify.
  - [ ] Classify the target as deterministic software behavior, AI output
    behavior, agent/tool behavior, skill workflow behavior, or mixed.
- [ ] 2. Gather candidate sources.
  - [ ] Use real failures, corrections, logs, traces, support issues, tickets,
    specs, and existing tests first when available.
  - [ ] Use synthetic cases only to fill named coverage gaps, not to replace
    real failure analysis.
  - [ ] Load [source ledger](references/source-ledger.md) when external
    practice needs to shape the case-generation strategy.
- [ ] 3. Build the case space before writing cases.
  - [ ] Define dimensions such as behavior, user intent, persona or caller,
    scenario, input shape, fixture state, edge boundary, tool/state transition,
    expected oracle, and proof surface.
  - [ ] Include at least one ordinary success path, one known or likely failure
    mode, one boundary/edge case, and one negative or anti-cheat control when
    the behavior is prompt-like or skill-like.
- [ ] 4. Generate candidate cases in small batches.
  - [ ] Prefer `3-7` candidates before selection; do not ask for a giant list.
  - [ ] For each case, write user-realistic input, fixture assumptions,
    success criteria, failure signal, and expected evidence.
  - [ ] Keep eval queries natural; put expected behavior in reference points,
    fixtures, or the owning skill, not in the query.
- [ ] 5. Score and select cases with
  [proof-case rubric](references/proof-case-rubric.md).
  - [ ] Reject near-duplicates, vague goodness checks, hidden-oracle cases,
    impossible fixtures, and cases whose failure would not identify an owner.
  - [ ] Keep fewer high-signal cases over broad but blurry coverage.
- [ ] 6. Choose the proof surface for each selected case.
  - [ ] Use deterministic tests, validators, schemas, or scripts when the
    expected result is mechanically checkable.
  - [ ] Use `testing`, `eval`, `agent-qa-test`, `agent-behavior-test`, `qa`,
    `visual-qa`, or `review` according to proof-surface fit.
  - [ ] Use evals or model/human judges when the behavior is variable but the
    criteria are explicit.
  - [ ] Use agent QA or behavior capture when the behavior depends on tool use,
    multi-turn state, screenshots, artifacts, or evidence review.
- [ ] 7. Produce the case artifact or handoff.
  - [ ] For skill-local evals, write or hand off `skills/<skill>/eval_task.json`
    rows with realistic `query`, visible `reference_points`, tags, and notes.
  - [ ] For deterministic tests, hand off concrete fixtures, assertions, and
    command paths.
  - [ ] For QA, write claim under test, test cases, required evidence, and
    reviewer focus.
- [ ] 8. Finish with QA.
  - [ ] Run [proof-case QA checklist](qa_checklist.md) for material case suites.
  - [ ] If eval rows changed, also run `skills/eval/qa_checklist.md` and the
    cheap query-spoiler smoke check when available.
  - [ ] If a skill package changed, run
    `skills/skill-maintenance/qa_checklist.md` against the changed skill.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Case matrix row:

```text
case_id:
target_behavior:
source: real_failure | log_trace | ticket | spec | existing_test | synthetic_gap
input_or_query:
fixture_state:
expected_oracle:
failure_signal:
proof_surface: unit | integration | contract | browser | validator | eval | agent_qa | behavior_capture | manual
evidence_required:
owner_if_fails:
notes:
```

Selected-case summary:

```text
selected_cases:
  - case_id:
    why_selected:
    distinct_failure_mode:
    proof_surface:
    next_owner:
rejected_cases:
  - case_id:
    reason:
coverage_gaps:
  - gap:
    next_candidate_source:
```

## Gotchas

- Do not treat "unit test" as the name for every AI proof. Use "case" for the
  shared unit, then choose the proof surface.
- Do not generate `50` cases before discovering the dimensions that make cases
  distinct.
- Do not fix an eval by adding the answer, skill name, or reference points to
  the user query.
- Do not use an LLM judge for behavior that a parser, schema, unit assertion,
  fixture diff, or deterministic script can check.
- Do not write cases whose pass/fail result would be impossible to explain or
  impossible to route to an owner.

## Reference Map

- [references/source-ledger.md](references/source-ledger.md) - read when
  external eval/testing practice should shape the case-generation workflow.
- [references/proof-case-rubric.md](references/proof-case-rubric.md) - read when
  scoring, selecting, rejecting, or reviewing proof cases.
- [qa_checklist.md](qa_checklist.md) - run before claiming material proof-case
  design is ready.
- [../testing/SKILL.md](../testing/SKILL.md) - route proof-surface execution and
  testing backpressure decisions.
- [../eval/SKILL.md](../eval/SKILL.md) - route runnable eval rows, judges,
  fixture ownership, and eval-run proof.

## Output

- `proof_plan`
- `case_matrix`
- `selected_cases`
- `proof_surface_map`
- `handoff`
- `rejected_cases`
- `coverage_gaps`
- `qa_verdict`
