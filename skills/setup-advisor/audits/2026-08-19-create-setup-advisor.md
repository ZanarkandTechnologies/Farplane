---
skill: setup-advisor
date: 2026-08-19
change_type: behavior
owner: skill-creator
status: pass
review_route: reviewer
before_ref: skills/init-advisor/SKILL.md
after_ref: skills/setup-advisor/SKILL.md
reasoning_basis: first_principles + advise + external_implementation + eval + reviewer
proof_artifacts:
  - skills/setup-advisor/tests/test_setup_wizard.py
  - skills/setup-advisor/evals/evals.json
  - .farplane/evals/runs/20260819-070304-20260819-setup-advisor-cutover-postchecks
  - .farplane/evals/runs/20260819-070651-20260819-setup-advisor-secret-names-only
  - .farplane/evals/runs/20260819-070406-20260819-setup-advisor-final
  - .farplane/evals/runs/20260819-071643-20260819-setup-advisor-review-repair-r2
  - skills/setup-advisor/audits/2026-08-19-review.md
eval_required: yes
---

# Setup Advisor Creation Audit

## Change

- Before: Farplane could scaffold projects and diagnose configuration, but it
  explicitly stopped at interactive service setup and had no generic human-gate
  wizard contract.
- After: `setup-advisor` owns operated external-service setup, generates a
  wizard only for irreducible human gates, and returns one redacted verified
  setup receipt.
- Why: Arbitrary service provisioning is reusable across projects but is not
  part of Farplane substrate initialization or recurring automation ownership.
- Tradeoff accepted: The first release uses current official docs rather than a
  prebuilt provider catalog, so repeated providers may cost more discovery
  until stable recipes earn their own conditional references.

## First-Principles Reasoning

- Objective: minimize operator setup work without weakening external-action,
  secret, or verification boundaries.
- Placement logic: a Tier 3 Operations skill is the smallest reusable owner;
  `init-advisor`, root prompts, subagents, hooks, and Core commands are rejected
  as primary surfaces.
- Expected behavior delta: the agent now automates safe setup first and hands
  the user a precise wizard only for actions the agent cannot perform.
- Proof needed: template syntax/runtime tests, four natural behavioral evals,
  skill-system validation, installed-package inspection, and reviewer TAS-A.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | All four cases have an A candidate run from first-load context. |
| `reference_load_precision` | pass | Official docs stay inline for ordinary providers; separate research is conditional. |
| `missing_context_rate` | pass | Fixture-backed evals cover repo, CI, cutover, secret, and routing inputs. |
| `noisy_context_rate` | pass | Five top-level todos and one conditional template; no provider catalog loaded. |
| `duplicated_instruction_count` | pass | QA is a five-item guardrail; operational detail remains in `SKILL.md`. |
| `prompt_size_tokens` | pass | `SKILL.md` is 181 lines and passes the surface-budget validator. |
| `task_success_rate` | pass | Final integrated candidate run earned 4/4 A. |
| `review_tas_rate` | pass | Native reviewer rereview returned TAS-A with no blockers. |
| `maintenance_locality` | pass | Skill-local template, tests, evals, fixtures, QA, and audit own the behavior. |
| `composition_clarity` | pass | Explicit boundaries preserve `init-advisor` and `automation-advisor` ownership. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/setup-advisor/evals/evals.json`
- Structure evals, when needed: skill creator and maintenance QA checklists
- Reviewer receipt: `skills/setup-advisor/audits/2026-08-19-review.md`
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed all checks on 2026-08-19.
- Template proof: `bash -n skills/setup-advisor/templates/setup-wizard.sh` passed; `python3 -m unittest skills/setup-advisor/tests/test_setup_wizard.py` passed 2/2. `shellcheck` was unavailable.
- Eval required: yes; routing, automation-first behavior, secret boundaries,
  and completion semantics are behavioral.
- Candidate evidence:
  - Final integrated run `20260819-071643-20260819-setup-advisor-review-repair-r2`:
    4/4 A after read-only grounding was made explicit and generated cache state
    was removed.
  - Full run `20260819-070406-20260819-setup-advisor-final`: automation-first,
    cutover, and init-boundary earned A; secret-boundary exposed an unsafe
    plain-value verification command and was repaired.
  - Focused run `20260819-070651-20260819-setup-advisor-secret-names-only`:
    secret-boundary earned A after changing the contract to names-only checks.
  - Focused run `20260819-070304-20260819-setup-advisor-cutover-postchecks`:
    cutover earned A after requiring distinct pre/post consumer probes.
  - Full rerun `20260819-070801-20260819-setup-advisor-final-r2` was 2 A / 2 B
    because the stochastic answers overclaimed doc inspection or omitted
    repeatability detail; all four reference behaviors have an A candidate
    proof, but one simultaneous 4/4 run was not obtained.
- Baseline comparison: deferred. No isolated baseline Codex profile exists in
  the local eval harness, and creating a live profile would mutate operator
  configuration. Readiness therefore rests on candidate behavior evidence and
  independent review rather than a comparative-lift claim.
- Initial independent review: TAS-B. It blocked on the latest integrated run's
  grounding overclaims and a generated `__pycache__`; both findings were
  repaired. Independent rereview returned TAS-A with no blocking findings.

## Before Behavior

- Agents stopped at interactive cloud or credential work and returned manual
  instructions without a reusable setup artifact.

## After Behavior

- Agents discover the full contract, operate authorized steps, produce only the
  remaining human-gate wizard, and report verified per-service status.

## Followups

- `no_self_improve_reason`: the skill has no production baseline yet; establish
  ordinary usage and eval evidence before opening a Goal-backed optimization
  loop.
- `rerun_rule`: fix and rerun the smallest failing eval before readiness.
