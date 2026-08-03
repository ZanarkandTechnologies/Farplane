---
skill: outreach-impl-plan
date: 2026-07-15
change_type: behavior
owner: skill-creator
status: pass
review_route: reviewer
before_ref: skills/content-impl-plan/SKILL.md + skills/first-value-outreach/SKILL.md
after_ref: skills/outreach-impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/archive/TASK-0377/artifacts/verification.md
  - tickets/archive/TASK-0377/artifacts/review/completion-review.md
eval_required: yes
---

# Outreach Impl Plan Initial Skill Audit

## Change

- Before: acquisition specialist skills produced separate research,
  contribution, offer, copy, CRM, and metric artifacts without one campaign
  compiler.
- After: one parent planner compiles evidence-bounded waves, advisor actions,
  campaign lock, CRM proposal, metrics, and approval inventory into an
  executable campaign ticket.
- Why: the operator accepted the proven `content-impl-plan` parent/child/action
  list structure for outreach.
- Tradeoff accepted: one additional Tier 3 orchestrator in exchange for visible
  campaign sequencing without duplicating child work.

## First-Principles Reasoning

- Objective: turn an acquisition strategy into a reviewable and executable
  relationship-development program.
- Placement logic: stable reusable trigger and output distinct from market
  discovery, person research, contribution design, or commercial offer shaping.
- Expected behavior delta: campaign plans become small-wave learning programs
  with complete action rows and explicit permission boundaries.
- Proof needed: five focused evals, skill-system validators, a real Valefor
  trial artifact, installed-source comparison, and independent TAS-A review.

## QA Verdicts

| Check | Verdict | Evidence |
| --- | --- | --- |
| Stable trigger and ownership | pass | Signature and Context separate parent planning from child execution |
| First-load sufficiency | pass | Inputs, gates, routes, six todos, lock, proof, and output are visible |
| Reference precision | pass | Checklist, examples, structural reference, contribution, and offer owners have conditions |
| Context balance | pass | Runtime contract remains first load; field-heavy artifact shape is in the template |
| Duplication and locality | pass | Parent owns sequence/lock; child skills retain specialist workflows |
| Composition clarity | pass | AdvisorAction and state/read/write/handoff contracts are explicit |
| Proof fit | pass | Variable campaign behavior uses evals; deterministic structure uses validators |
| Case quality | pass | Five distinct cases cover happy path, bulk outreach, CRM, composition, and metrics |
| QA preflight | pass | Todo 1 loads QA and Todo 6 reapplies it |

## Proof Artifacts

- Eval suite: `skills/outreach-impl-plan/evals/evals.json`
- Example: `skills/outreach-impl-plan/examples/industrial-expert-wave/example.md`
- Verification: `tickets/archive/TASK-0377/artifacts/verification.md`; final behavior
  suite passed `5/5 A` and full skill-system checks passed.
- Review: `tickets/archive/TASK-0377/artifacts/review/completion-review.md` — independent TAS-A.
- `no_self_improve_reason`: wait for the first approved live campaign and
  response evidence before creating an optimization loop.

## Before Behavior

- Strategy and candidate artifacts required manual coordination and could blur
  plan approval with CRM or send permission.

## After Behavior

- One approval-ready campaign ticket controls waves, child handoffs, learning,
  state boundaries, and permissions without executing them.

## Followups

- Run the planner on Valefor's construction candidate wave and use operator
  feedback on that artifact as the first real quality signal.
