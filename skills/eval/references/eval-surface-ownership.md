---
owner: skills/eval
status: active
last_updated: 2026-06-23
---

# Eval Surface Ownership

Use this when deciding which part of the Farplane eval system to change.

## Rule

```text
eval_surface_change(need) -> owner_surface + proof
```

Profiles configure how the harness runs. Fixtures describe the world. Eval
tasks describe one behavior to test. The runner executes and records proof.
Judges decide whether the observed answer met the reference points.

## Surface Map

| Change needed | Primary surface | Do not put it in |
| --- | --- | --- |
| Model, reasoning, sandbox, approvals, web/search, MCP, skill enable/disable | Codex profile | Eval task query |
| Shared fictional company state, role assumptions, toy tickets, product facts, safety boundaries | AGI Toy Shop fixture context | Codex profile |
| One user ask and expected behavior | `evals/evals.json` row | Profile or shared fixture |
| Skill-specific regression coverage | `skills/<skill>/evals/evals.json` | Global harness task file |
| Cross-skill or workflow behavior coverage | `.farplane/evals/tasks/harness_tasks.json` or reusable examples | One skill package |
| AGENTS.md or system-prompt behavior coverage | `.farplane/evals/tasks/agents_md_tasks.json` | Skill-local task file |
| Judge strictness, tier rules, required output shape | Judge prompt or eval quality rubric | Task query |
| Pre-run aggregate prediction for a comparative/causal eval | Metric Card plus ticket/program, experiment plan, comparison artifact, or run notes | Task query, assertions, or runner schema by default |
| Runner behavior, profile selection, artifact layout, summary schema | `run_evals.py` plus tests and templates | Skill instructions only |
| Codex eval session/hook/notify isolation | `run_evals.py` mandatory argument tail | Optional Codex profiles |
| Deterministic structural invariant | Validator, lint, or unit test | LLM eval |
| Judgment-heavy placement or prioritization | `harness-advisor`, `review`, or eval rubric | Hook |

## AGI Toy Shop Fixture Policy

AGI Toy Shop is the default clean-room fixture for Farplane harness evals. Keep
generic eval examples inside this fictional company unless the behavior cannot
be tested honestly without real repo files.

Use AGI Toy Shop for:

- language, reasoning, routing, escalation, pushback, and planning behavior
- proof discipline, QA expectations, ticket hygiene, and artifact selection
- skill and workflow regressions that do not need real side effects
- hardcases that must be sanitized before becoming reusable evals

Do not create new fictional companies for ordinary harness evals. Extend the
AGI Toy Shop context when the eval set needs a new department, ticket, workflow,
UI, policy, or failure case. Use a real repo fixture only when the eval needs
actual files, validators, scripts, browser UI, or local state.

## Profile-Backed Skill Evals

For Codex skill evals, prefer profile-backed runs:

```bash
python3 .farplane/evals/run_evals.py run \
  --harness codex \
  --skill qa \
  --agent-profile farplane-qa-skill-eval \
  --label qa-native-profile
```

When `--agent-profile` is present, the runner relies on native Codex skill
discovery instead of injecting the owning `SKILL.md` into context. This means a
missing, disabled, poorly described, or non-triggering skill fails honestly.

If the profile should isolate one skill, configure Codex skill entries in the
profile to disable unrelated skill paths. Codex documents per-skill
disable/re-enable entries, not a single `allowed_skills` key.

## Scope Selection

```text
eval_scope(flags, files) -> task_files
```

File location is the canonical family signal:

- `.farplane/evals/tasks/harness_tasks.json` for harness and workflow evals.
- `.farplane/evals/tasks/agents_md_tasks.json` for AGENTS.md/system-prompt evals.
- `skills/<skill>/evals/evals.json` for skill-local evals.

No-scope `run` executes every known available family. Use `--harness-evals`,
`--agents-md`, `--skills`, or `--skill <name>` to narrow the run. `--harness`
is only the runner backend selector, such as `codex`, `claude`, or `custom`.

## Task Shape

Keep eval tasks small and natural:

```json
{
  "skill_name": "qa",
  "evals": [
    {
      "id": "qa_ui_evidence_01",
      "prompt": "Please verify the checkout UI change is actually working.",
      "expected_output": "A QA verdict supported by captured UI evidence.",
      "files": [],
      "assertions": [
        "Uses the QA skill or equivalent QA workflow",
        "Requires browser or visual evidence for the UI claim",
        "Does not self-certify without captured proof",
        "Returns or points to image evidence in the final verdict"
      ]
    }
  ]
}
```

Do not put skill instructions, routing policy, or expected answers in the
`prompt`. Put shared setup in the fixture, expected behavior in `assertions`,
and harness mechanics in the profile or runner.

## Placement Checklist

- If the change affects how Codex is launched, update the profile or runner.
- If the change affects what world the task takes place in, update AGI Toy
  Shop fixture context.
- If the change affects what one task asks or proves, update `evals/evals.json`.
- If the change affects how results are judged, update judge prompt or rubric.
- If the change predicts aggregate experimental movement, keep it outside the
  task query and compare it after the run; do not add runner schema fields
  unless a current machine consumer requires them.
- If the change is structural and deterministic, add a validator or unit test.
- If the change is about which surface owns the fix, route through
  `harness-advisor`.
