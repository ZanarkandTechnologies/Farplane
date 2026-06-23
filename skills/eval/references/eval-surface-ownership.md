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
| One user ask and expected behavior | `eval_task.json` row | Profile or shared fixture |
| Skill-specific regression coverage | `skills/<skill>/eval_task.json` | Global harness task file |
| Cross-skill or system behavior coverage | `.farplane/evals/tasks/*` or reusable examples | One skill package |
| Judge strictness, tier rules, required output shape | Judge prompt or eval quality rubric | Task query |
| Runner behavior, profile selection, artifact layout, summary schema | `run_evals.py` plus tests and templates | Skill instructions only |
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
AGI Toy Shop context when the suite needs a new department, ticket, workflow,
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

## Task Shape

Keep eval tasks small and natural:

```json
{
  "id": "qa_ui_evidence_01",
  "title": "QA requires image evidence for UI work",
  "query": "Please verify the checkout UI change is actually working.",
  "reference_points": [
    "Uses the QA skill or equivalent QA workflow",
    "Requires browser or visual evidence for the UI claim",
    "Does not self-certify without captured proof",
    "Returns or points to image evidence in the final verdict"
  ],
  "tags": ["qa", "ui", "proof"],
  "notes": "Uses AGI Toy Shop checkout context from the shared fixture."
}
```

Do not put skill instructions, routing policy, or expected answers in the
`query`. Put shared setup in the fixture, expected behavior in
`reference_points`, and harness mechanics in the profile or runner.

## Placement Checklist

- If the change affects how Codex is launched, update the profile or runner.
- If the change affects what world the task takes place in, update AGI Toy
  Shop fixture context.
- If the change affects what one task asks or proves, update `eval_task.json`.
- If the change affects how results are judged, update judge prompt or rubric.
- If the change is structural and deterministic, add a validator or unit test.
- If the change is about which surface owns the fix, route through
  `harness-advisor`.
