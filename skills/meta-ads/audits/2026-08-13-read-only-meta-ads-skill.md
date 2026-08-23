---
skill: meta-ads
date: 2026-08-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/ad-advisor/SKILL.md
after_ref: skills/meta-ads/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/meta-ads/scripts/test_check_config.py
  - skills/meta-ads/evals/evals.json
  - .farplane/evals/runs/20260813-150535-meta-ads-read-tas-a/summary.json
  - .farplane/evals/runs/20260813-150610-meta-ads-credentials-tas-a/summary.json
  - .farplane/evals/runs/20260813-150718-meta-ads-write-gate-pass/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: `ad-advisor` could design a spend-gated campaign but did not own a
  live, read-only Meta account reporting route.
- After: `meta-ads` owns the bounded read-only CLI route and hands every write
  or strategy request back to `ad-advisor`.
- Why: account facts need a small, separately auditable operator surface;
  campaign strategy and spend control remain one owner.
- Tradeoff accepted: the first release deliberately cannot mutate campaigns.

## First-Principles Reasoning

- Objective: safely retrieve actual Meta account facts without credentials or
  spend actions leaking into planning work.
- Placement logic: no existing local skill owns live account reads; the new
  package reuses the installed read-only CLI rather than adding an SDK or
  campaign-management implementation.
- Expected behavior delta: an agent can check runtime readiness, discover an
  accessible account, and return a bounded report with clear routing.
- Proof needed: config checker tests, CLI smoke test, registry validation,
  behavioral eval review, and independent skill-contract review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | TAS-A reviewer re-review; all three routes produced complete guarded replies. |
| `reference_load_precision` | pass | CLI guide is loaded only after a read branch; it covers the declared branch commands. |
| `missing_context_rate` | pass | Read, blocked, and mutation-route evals passed TAS-A. |
| `noisy_context_rate` | pass | First load retains only the execution, guard, and handoff contract. |
| `duplicated_instruction_count` | pass | Reporting stays in `meta-ads`; strategy and mutations remain in `ad-advisor`. |
| `prompt_size_tokens` | pass | Independent reviewer found no first-load bloat blocker. |
| `task_success_rate` | pass | Three focused candidate evals passed TAS-A. |
| `review_tas_rate` | pass | Reviewer re-review returned TAS-A. |
| `maintenance_locality` | pass | One package owns the CLI guide, checker, tests, QA, evals, and audit. |
| `composition_clarity` | pass | Read-only report, blocked report, and spend-gated handoff boundaries are explicit. |

## Proof Artifacts

- Skill-local evals: `skills/meta-ads/evals/evals.json`.
- Structure validation: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed on 2026-08-13.
- Config checker tests: `python3 -m unittest discover -s skills/meta-ads/scripts -p 'test_*.py' -v` passed (3 tests).
- Query lint: `python3 skills/eval/scripts/check_eval_queries.py --root .` passed.
- Behavioral evals: the focused read, missing-credentials, and mutation-route
  candidate runs above all passed TAS-A.
- Reviewer receipt: independent reviewer re-review returned TAS-A for
  `skill-contract`, `eval-quality`, `integration-readiness`, and
  `evidence-quality`; no hard-gate failures.
- Install: `bash install.sh --skills-only --skill meta-ads` installed the
  repo-owned package into `~/.codex/skills/meta-ads`; the live config checker
  returned `ready: true`, `read_ready: true`, `publish_ready: false`.
- Evidence gaps: a fresh live campaign/account report is blocked because the
  injected Meta token expired after earlier identity/account-discovery success.
  Refresh the private token, then rerun a bounded insights read before claiming
  live account data.

## Before Behavior

- Account reporting had no dedicated local owner; campaign advice had to infer
  facts or stop at a generic CLI handoff.

## After Behavior

- `meta-ads` reports read-only facts through `meta-ads-open-cli`, blocks safely
  without private runtime readiness, and routes spend-affecting work.

## Followups

- Refresh the Meta token and run a bounded live `insights` report when fresh
  campaign data is needed.
