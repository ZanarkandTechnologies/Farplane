---
title: "Account config readiness implementation review"
status: pass
owner: reviewer
created_at: 2026-08-02
updated_at: 2026-08-02
context_ref: skills/skill-maintenance/audits/2026-08-02-account-config-readiness-contract.md
review_focus: implementation
overall_tas: TAS-A
verdict: pass
---

# Review Summary

## Final Lean Output Review

- work_type: focused output-contract review
- changed_files:
  - `docs/skills/system.md`
  - `skills/instagram-account/scripts/check_config.py`
  - `skills/instagram-account/scripts/test_check_config.py`
  - `skills/x-account/scripts/check_config.py`
  - `skills/x-account/scripts/test_check_config.py`
- rubrics_used: `skill-contract`, `code-quality`, `integration-readiness`, `evidence-quality`
- overall_tas: TAS-A
- verdict: pass
- rerun_required: no
- hard_gate_failures: none
- blocking_findings: none

Blocking findings: none. The successful payload is now the five-field contract
only: `skill`, `ready`, `read_ready`, `publish_ready`, `redacted`. Blocked
payloads add only `missing`, and the missing structure names required keys or
alternative credential groups without printing values. No verbose flag,
capability selector, config path, optional app/refresh diagnostic, or auth-mode
detail remains in default checker output.

Evidence:

- `python3 -m unittest discover -s skills/instagram-account/scripts`: pass, 5 tests.
- `python3 -m unittest discover -s skills/x-account/scripts`: pass, 7 tests.
- `python3 -m py_compile skills/instagram-account/scripts/check_config.py skills/instagram-account/scripts/test_check_config.py skills/x-account/scripts/check_config.py skills/x-account/scripts/test_check_config.py`: pass.
- `git diff --check -- docs/skills/system.md skills/instagram-account/scripts/check_config.py skills/instagram-account/scripts/test_check_config.py skills/x-account/scripts/check_config.py skills/x-account/scripts/test_check_config.py`: pass.
- Local success smokes for Instagram and X exit `0` and emit exactly the five keys.
- Local blocked smokes for Instagram token-only and X bearer-only exit `1` and emit only base keys plus actionable `missing` alternatives.
- Installed skill copies under `~/.codex/skills/instagram-account` and `~/.codex/skills/x-account` match the lean checker implementation.
- Installed Farplane live runs from the Farplane checkout exit `0` for Instagram and X with exactly the five-field success payload.
- Installed Gagazet live run for Instagram currently exits `0` with exactly the five-field success payload.
- Installed Gagazet live run for X exits `1` with `read_ready: false`, `publish_ready: false`, and `missing.read_any_of` / `missing.publish_any_of`; no secret values are printed.

Next action: advance the lean output refinement. No repair is required.

## Follow-Up Regression Review

- work_type: live regression fix review
- changed_files:
  - `skills/instagram-account/scripts/social_config.py`
  - `skills/x-account/scripts/social_config.py`
  - `skills/instagram-account/scripts/test_check_config.py`
  - `skills/x-account/scripts/test_check_config.py`
- rubrics_used: `code-quality`, `integration-readiness`, `evidence-quality`
- overall_tas: TAS-A
- verdict: pass
- rerun_required: no
- hard_gate_failures: none
- blocking_findings: none

Blocking findings: none. Catching only `tomllib.TOMLDecodeError` is the right
security/diagnostic tradeoff for this contract: the private file is explicitly a
best-effort fallback/cache, runtime environment values still take precedence via
`env_value()`, and malformed local cache content no longer blocks Doppler env
credentials or prints secret material. The diagnostic tradeoff is acceptable:
when the fallback is malformed and no env values exist, the checker reports
missing credential names rather than parse failure, which matches the accepted
"treat fallback as empty" repair.

Evidence:

- `python3 -m unittest discover -s skills/instagram-account/scripts`: pass, 5 tests.
- `python3 -m unittest discover -s skills/x-account/scripts`: pass, 7 tests.
- `python3 -m py_compile skills/instagram-account/scripts/social_config.py skills/instagram-account/scripts/test_check_config.py skills/x-account/scripts/social_config.py skills/x-account/scripts/test_check_config.py`: pass.
- `git diff --check -- skills/instagram-account/scripts/social_config.py skills/x-account/scripts/social_config.py skills/instagram-account/scripts/test_check_config.py skills/x-account/scripts/test_check_config.py`: pass.
- Manual malformed-fallback smoke with runtime Instagram env credentials: exit `0`, `ready: true`, `read_ready: true`, `publish_ready: true`, `redacted: true`, and no secret value printed.
- Manual malformed-fallback smoke with runtime X OAuth2 env credentials: exit `0`, `ready: true`, `read_ready: true`, `publish_ready: true`, `redacted: true`, and no secret value printed.
- Live command `farplane run -- python3 skills/instagram-account/scripts/check_config.py`: exit `0`, `ready: true`, `read_ready: true`, `publish_ready: true`, `config_file_exists: true`, `redacted: true`.
- LSP diagnostics remain unavailable in this lane; tool discovery exposed no callable LSP diagnostics tool and `pyright`/`mypy` are not installed. Runtime and compile checks are sufficient for this narrow Python loader fix.

Next action: advance the regression fix. No implementation repair is required.

- work_type: material skill-system implementation review
- search_scope:
  - Contract: `skills/skill-maintenance/audits/2026-08-02-account-config-readiness-contract.md`
  - Rubrics: `docs/review/rubrics/review-rubric-index.md`, `skill-contract.md`, `integration-readiness.md`, `evidence-quality.md`, `code-quality.md`, `documentation-quality.md`, `desloppify.md`
  - QA: `skills/skill-maintenance/qa_checklist.md`, `skills/instagram-account/qa_checklist.md`, `skills/x-account/qa_checklist.md`
  - Changed files: `docs/skills/system.md`, `skills/instagram-account/SKILL.md`, `skills/instagram-account/scripts/check_config.py`, `skills/instagram-account/scripts/test_check_config.py`, `skills/x-account/SKILL.md`, `skills/x-account/scripts/check_config.py`, `skills/x-account/scripts/test_check_config.py`
  - Neighboring surfaces: `skills/instagram-account/scripts/social_config.py`, `skills/x-account/scripts/social_config.py`, repo searches for `check_config`, readiness fields, capability selectors, debug residue, and secret literals
- rubrics_used:
  - `skill-contract`: selected because skill files and skill-system behavior changed.
  - `integration-readiness`: selected as a hard gate because the change alters readiness/exit semantics used by agents.
  - `evidence-quality`: selected as a hard gate because the contract makes specific proof claims.
  - `code-quality`: added for the Python checker/test changes.
  - `documentation-quality`: added for the canonical `docs/skills/system.md` policy delta.
- overall_tas: TAS-A
- verdict: pass
- rerun_required: no
- hard_gate_failures: none

## Findings

No blocking findings.

## Family Verdicts

- `skill-contract`: TAS-A. `SKILL.md` routes agents to one package-local `scripts/check_config.py` before live API work and explicitly forbids a capability selector: `skills/instagram-account/SKILL.md:75`, `skills/x-account/SKILL.md:74`. The first-load rule remains concise and operational.
- `integration-readiness`: TAS-A. The contract in `docs/skills/system.md:74` through `docs/skills/system.md:82` matches both implementations: `ready` and exit `0` now require read plus publish readiness in `skills/instagram-account/scripts/check_config.py:25` and `skills/x-account/scripts/check_config.py:35`; optional app/refresh credentials remain diagnostic.
- `evidence-quality`: TAS-A. Focused tests and manual smokes prove the main partial/full readiness claims, exit semantics, and redaction behavior. The reproduced `check_skills.py` failure is unrelated to this change and matches the contract's residual-evidence note.
- `code-quality`: TAS-A. The code change is localized, readable, and avoids new flags or selectors. No debug residue or broad exception swallowing found in the changed scripts.
- `documentation-quality`: TAS-A. The canonical policy is placed in `docs/skills/system.md` near the tracked/private config boundary and states the envelope, no-selector rule, redaction rule, and exit semantics without adding secret fields to frontmatter.

## Evidence

- `python3 test_check_config.py` in `skills/instagram-account/scripts`: pass, 2 tests.
- `python3 test_check_config.py` in `skills/x-account/scripts`: pass, 2 tests.
- `python3 -m unittest discover -s skills/instagram-account/scripts -p 'test_check_config.py'`: pass, 2 tests.
- `python3 -m unittest discover -s skills/x-account/scripts -p 'test_check_config.py'`: pass, 2 tests.
- `python3 -m py_compile skills/instagram-account/scripts/check_config.py skills/instagram-account/scripts/test_check_config.py skills/x-account/scripts/check_config.py skills/x-account/scripts/test_check_config.py`: pass.
- Manual smoke, Instagram token only with isolated `FARPLANE_STATE_DIR`: exit `1`, `read_ready: true`, `publish_ready: false`, `ready: false`, `redacted: true`, no secret value printed.
- Manual smoke, Instagram token plus user ID with isolated `FARPLANE_STATE_DIR`: exit `0`, `read_ready: true`, `publish_ready: true`, `ready: true`, `redacted: true`.
- Manual smoke, X bearer only with isolated `FARPLANE_STATE_DIR`: exit `1`, `read_ready: true`, `publish_ready: false`, `ready: false`, `redacted: true`, no secret value printed.
- Manual smoke, X OAuth2 access token with isolated `FARPLANE_STATE_DIR`: exit `0`, `read_ready: true`, `publish_ready: true`, `ready: true`, `redacted: true`.
- `python3 skills/skill-maintenance/scripts/check_skills.py`: nonzero only for existing `skills/content-impl-plan` QA/eval surface budget failures; skill todo sections, registry, template registry, todo tiers, and Tier 0 phase protocol passed.
- LSP diagnostics: no callable LSP diagnostics tool was exposed by tool discovery, and `pyright`/`mypy` were not installed. Python compile and focused runtime tests were used as the available substitute.

## Finding Log

- severity: low
  confidence: high
  rubric: evidence-quality
  summary: LSP diagnostics could not be run in this environment.
  file_refs: none
  evidence: tool discovery exposed no LSP diagnostics tool; `command -v pyright` and `command -v mypy` returned no executable.
  next_action: No implementation rerun required for this pass; use LSP diagnostics if the lane later exposes the tool.

## Next Action

Advance the implementation. No repair pass is required for the account config readiness change.
