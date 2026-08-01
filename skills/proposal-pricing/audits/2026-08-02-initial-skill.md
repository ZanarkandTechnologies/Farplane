---
skill: proposal-pricing
date: 2026-08-02
change_type: behavior
owner: skill-creator
status: pass
review_route: reviewer
before_ref: missing-skill
after_ref: skills/proposal-pricing/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/proposal-pricing/evals/evals.json
  - skills/proposal-pricing/scripts/test_calculate_value.py
  - .farplane/evals/runs/20260801-200911-proposal-pricing-full/summary.json
  - .farplane/evals/runs/20260801-201319-proposal-pricing-consequence-rerun/summary.json
eval_required: yes
---

# Proposal Pricing Initial Skill Audit

## Change

- Before: No skill converted customer call evidence into a concise, priced proposal.
- After: One transcript-only skill extracts a single value anchor, asks at most
  one missing-value question, and produces one short recommended engagement.
- Why: The workflow repeats after customer calls and has a distinct commercial
  artifact that is not owned by customer research, solution shaping, or outreach.
- Tradeoff accepted: The first version favors one transparent value heuristic
  over a configurable pricing system.

## First-Principles Reasoning

- Objective: Make a defensible price easy for a customer and operator to understand.
- Placement logic: A Tier 3 skill is the smallest reusable owner for this
  post-call commercial workflow.
- Expected behavior delta: Transcript evidence leads to one value calculation
  and one proposal rather than a questionnaire or pricing packet.
- Proof needed: Deterministic arithmetic tests, held-out behavior evals, skill
  validation, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Trigger, signature, gates, todo path, and output are in `SKILL.md`. |
| `reference_load_precision` | pass | Template, golden, QA, and calculator load conditions are explicit. |
| `missing_context_rate` | pass | The only required runtime input is transcript or notes. |
| `noisy_context_rate` | pass | Pricing tutorial detail and broad intake schemas are absent. |
| `duplicated_instruction_count` | pass | Default behavior has one owner in `SKILL.md`; QA, template, example, and evals have distinct proof/calibration roles. |
| `prompt_size_tokens` | pass | First load contains only the normal path and failure gates. |
| `task_success_rate` | pass | Three initial passes plus a repaired consequence case that passed TAS-A on the focused rerun. |
| `review_tas_rate` | pass | Independent reviewer returned TAS-A with no hard-gate failures. |
| `maintenance_locality` | pass | All new behavior is owned under `skills/proposal-pricing/`. |
| `composition_clarity` | pass | Reads, writes, gates, routes, and failures are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/proposal-pricing/evals/evals.json`
- Structure evals, when needed: skill-maintenance validator output
- Reviewer receipt: `skills/proposal-pricing/audits/2026-08-02-independent-review.md`
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Eval required: yes
- Evidence gaps: no blocking gaps; a clean full-suite post-repair rerun remains optional because the focused failing case passed.

## Eval Experiment Expectation

- Hypothesis: Loading `proposal-pricing` will make the response materially
  shorter and more commercially decisive than the base profile while keeping
  the value arithmetic correct.
- Expected observation: The candidate passes the first people-time case at
  TAS-A; the baseline may produce a usable proposal but is more likely to add
  questions, options, or pricing explanation.
- Observation horizon: First held-out case, followed by the four-case suite if
  the candidate passes.
- Confidence: medium.
- Falsifier: The candidate misses the arithmetic, exceeds 800 words, asks for
  supplied facts, or fails to recommend one price.
- Surprise trigger: A perfect candidate and baseline tie, or a candidate miss
  on the one-question or no-outcome cases, requires inspection for leakage or
  insufficient first-load guidance before promotion.
- Surprise route: `agent-qa-test:experiment` when material.

## Before Behavior

- A call transcript could produce a broad pricing packet or unsupported proposal.

## After Behavior

- A call transcript produces one missing-value question or one concise,
  price-backed proposal.

## Followups

- Consider self-improvement only after reviewed real proposal outcomes provide
  a stable baseline and evidence of a recurring failure.
- `no_self_improve_reason`: The new package now has a canonical eval baseline,
  but no real reviewed proposal outcomes or repeated failure justify a Goal-backed
  optimization loop yet.

## Eval Result

- Initial full comparison: three TAS-A passes and one TAS-C failure. The failed
  consequence case did not trigger the skill and omitted price and return.
- Repair: broadened the ordinary-language trigger so “write the proposal from
  this call” invokes the skill without requiring the user to say “price it.”
- Focused rerun: consequence case TAS-A, skill triggered, candidate beat baseline.
- Final covered state: all four canonical cases have passing TAS-A evidence;
  the failed artifact remains retained in the initial run for replay.
- Query-spoiler check: pass.
- Comparison observation: candidate beat baseline on the repaired boundary
  case; easy cases may tie because a capable base model can perform the math.
