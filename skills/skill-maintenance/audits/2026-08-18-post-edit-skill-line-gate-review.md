---
skill: skill-maintenance
date: 2026-08-18
review_type: implementation
context_ref: skills/skill-maintenance/audits/2026-08-18-post-edit-skill-line-gate.md
reviewer: reviewer
verdict: pass
overall_tas: TAS-A
---

# Post-Edit Skill Line Gate Review

## Review Summary

- work_type: material hook, validator, installer, docs, and skill-contract change
- search_scope: durable audit; changed hook, hook config, installer inventory, CLI hook doctor path, staged validator, focused tests, skill-maintenance and skill-creator contracts, skill best practices, hook/runtime docs, Codex official hook docs, and focused validation output
- rubrics_used: `code-quality`, `integration-readiness`, `evidence-quality`, `skill-contract`, plus `desloppify` as the cross-cutting search playbook
- overall_tas: TAS-A
- verdict: pass
- rerun_required: no
- hard_gate_failures: none

## Stage 1 - Task Compliance

Pass. The implementation satisfies the approved contract: after `apply_patch`
touches `skills/**/SKILL.md`, a resulting file above 200 physical lines returns
PostToolUse block feedback without undoing the edit, and strict pre-commit
enforcement repeats the same 200-line invariant.

Decisive evidence:

- `hooks/skill_file_line_gate.py:76` gates only `PostToolUse`, and
  `hooks/skill_file_line_gate.py:78` limits the hook to edit tool names.
- `hooks/skill_file_line_gate.py:56` extracts only patch-declared paths;
  `hooks/skill_file_line_gate.py:60` rejects paths outside the repo root; and
  `hooks/skill_file_line_gate.py:63` scopes enforcement to `skills/**/SKILL.md`.
- `hooks/skill_file_line_gate.py:93` counts physical lines with
  `splitlines()`, and `hooks/skill_file_line_gate.py:94` blocks only `> 200`.
- `hooks/skill_file_line_gate.py:103` tells the agent the edit remains applied
  and requires repair while preserving default-path behavior.
- `rules/git-review-gates.toml:18` selects the backstop only for
  `skills/**/SKILL.md`, and `rules/git-review-gates.toml:92` uses
  `--strict --max-lines 200`.
- Official Codex hooks docs confirm `PostToolUse` runs after `apply_patch`,
  receives `tool_input.command`, supports `decision: "block"` with
  `hookSpecificOutput.hookEventName: "PostToolUse"`, and does not undo the
  completed tool side effect.

## Rubric Results

### Code Quality - TAS-A

No P1/P2 defects found. The hook is small, pure around the core decision, and
uses explicit failure-default behavior: malformed or irrelevant payloads return
no output instead of disrupting normal tool use. Path handling resolves against
the current working directory, compares against the discovered repo root, and
ignores deleted, non-skill, and outside-repo paths. The staged validator reuses
the existing source-line guard with one strict flag rather than adding a second
line-count implementation.

### Integration Readiness - TAS-A

No P1/P2 defects found. `hooks.json:21` wires a PostToolUse matcher for
`apply_patch` aliases; `bin/core/farplane_cli_base.py:34` and `install.sh:139`
include `skill_file_line_gate.py` in the managed hook allowlist; and live
`farplane hooks doctor --json` reports the new hook target linked, executable,
and issue-free. The remaining operator trust step is expected Codex behavior
for changed hook hashes, not an implementation defect.

### Skill Contract - TAS-A

No P1/P2 defects found. `skills/skill-maintenance/SKILL.md:25` and
`skills/skill-creator/SKILL.md:27` now name the 200-line hard envelope without
turning size into permission to hide first-load behavior. The QA checklists and
`docs/skills/best-practices.md:229` preserve the responsibility-based split
rule, so the skill system remains source-preserving rather than count-chasing.
Edited skill entrypoints are under the cap: skill-maintenance is 169 lines and
skill-creator is 184 lines.

### Evidence Quality - TAS-A

No P1/P2 defects found. Evidence is traceable and replayable:

- `python3 -m unittest bin.tests.test_skill_file_line_gate bin.validators.test_check_source_line_growth bin.tests.test_install_bin_surface bin.tests.test_farplane_hooks_install bin.tests.test_final_response_gate` passed 44 tests.
- `python3 -m py_compile hooks/skill_file_line_gate.py bin/validators/check_source_line_growth.py` passed.
- `python3 bin/validators/check_harness_invariants.py` passed.
- `python3 bin/validators/check_doc_refs.py` passed 2207 refs.
- `git diff --check -- <reviewed paths>` passed.
- `farplane hooks doctor --json` passed with no issues and shows the
  PostToolUse command linked to the repo-owned hook.
- Manual hook invocation returned valid block JSON for a touched 201-line
  `skills/demo/SKILL.md`.

## Finding Log

- severity: low
  confidence: high
  rubric: evidence-quality
  summary: The current review environment did not expose an `lsp_diagnostics`
  tool, so Python syntax coverage used `py_compile` plus focused unit tests.
  This does not block pass for this Python-only hook and validator change.
  file_refs: `hooks/skill_file_line_gate.py`, `bin/validators/check_source_line_growth.py`
  next_action: none

## Blocking Findings

None.

## Next Action

Proceed to commit after the coordinating lane confirms the intended staged set
does not include unrelated user-owned work. After install, trust the changed
hook hash once through Codex `/hooks` before relying on live interactive
PostToolUse enforcement.

## Grounding

Local files, focused tests, live hook doctor output, and official Codex hooks
docs: <https://learn.chatgpt.com/docs/hooks>.
