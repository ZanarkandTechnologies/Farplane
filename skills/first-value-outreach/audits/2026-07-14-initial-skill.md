---
skill: first-value-outreach
date: 2026-07-14
change_type: behavior
owner: skill-creator
status: pass
review_route: reviewer
before_ref: skills/lead-scout/SKILL.md + skills/personalized-offer/SKILL.md
after_ref: skills/first-value-outreach/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/archive/TASK-0371/artifacts/verification.md
  - tickets/archive/TASK-0371/artifacts/review.md
eval_required: yes
---

# First Value Outreach Initial Skill Audit

## Change

- Before: qualified prospect research handed directly to generic outreach or a
  personalized commercial offer requiring an accepted use case.
- After: one skill owns a bounded useful contribution, correction-first unsent
  message, learning objective, and stop condition before commercial packaging.
- Why: discovery, first contribution, and commercial offer have different
  triggers, outputs, success criteria, and failure modes.
- Tradeoff accepted: maintain one additional Tier 3 marketing skill and its
  proof surfaces for a cleaner lifecycle boundary.

## First-Principles Reasoning

- Objective: earn access to real problems by contributing before asking.
- Placement logic: a new Tier 3 skill has a stable trigger and reusable
  workflow that neither `lead-scout` nor `personalized-offer` owns.
- Expected behavior delta: agents create a small standalone-useful artifact and
  correction ask instead of vague free help, premature pitching, or overbuilt
  demos.
- Proof needed: structure validators, five focused behavior evals, checklist
  application, and independent review.

The first independent review returned TAS-B and identified two repaired gaps:
the upstream `customer-research` contract did not discover the new handoff, and
the optional-demo branch did not distinguish realism preparation from the
actual implementation owner or prove a justified demo case.

## QA Verdicts

| Check | Verdict | Evidence |
| --- | --- | --- |
| Ownership and stable trigger | pass | Signature and neighbor boundaries in `SKILL.md` |
| First-load sufficiency | pass | Trigger, inputs, routes, gates, todos, proof, and output are first-load visible |
| Reference load precision | pass | Each neighbor, checklist, template, example, and eval surface has a named load condition |
| Missing/noisy context balance | pass | Normal workflow remains first load; artifact shape and calibration are external |
| Duplication and maintenance locality | pass | Behavior lives in `SKILL.md`; template owns fields; example owns taste; QA owns runtime review |
| Prompt size and section necessity | pass | Seven todos and only template-supported sections |
| Composition clarity | pass | Reads, writes, routes, gates, failures, and downstream handoff are explicit |
| Instruction/todo alignment | pass | Mandatory runtime actions are represented in signature gates or numbered todos |
| Proof surface fit | pass | Variable agent behavior uses evals; structure uses deterministic validators; quality uses reviewer |
| Case quality and anti-cheat design | pass | Five distinct user prompts do not name the skill or leak the desired workflow vocabulary |
| QA preflight and finish gate | pass | Todo 1 loads QA; Todo 7 reapplies QA and routes material review |

## Proof Artifacts

- Skill-local evals: `skills/first-value-outreach/evals/evals.json`
- Positive example: `skills/first-value-outreach/examples/construction-operator/example.md`
- Validator and eval receipts:
  `tickets/archive/TASK-0371/artifacts/verification.md`;
  the repaired final suite passed five of five behavior cases at verdict A.
- Reviewer receipt: first review TAS-B; repaired final review TAS-A in
  `tickets/archive/TASK-0371/artifacts/review.md`.
- Eval required: yes; executed with pass rate `1.0`.
- `no_self_improve_reason`: defer an optimization loop until one operator-approved
  real prospect trial produces response-quality evidence.

## Before Behavior

- Agents could search and research prospects, then either ask vaguely for work
  or jump to a commercial offer and proof package.

## After Behavior

- Agents must earn the first conversation with a bounded, useful, inspectable
  contribution and a correction-first ask before downstream offer shaping.

## Followups

- Run the skill on the finalized Valefor construction candidates after this
  baseline package passes validation and review.
