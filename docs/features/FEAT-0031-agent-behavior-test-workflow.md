---
title: Retired agent behavior test workflow
status: retired
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-07-16
tags: [farplane, feature, sys-0005]
refs:
  - skills/eval
  - skills/agent-qa-test
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
feature_id: FEAT-0031
system_id: SYS-0005
category: proof
public: true
surfaces:
  - skills/eval
source_refs:
  - docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md
external_refs: []
evidence_refs:
  - skills/eval/audits/2026-07-16-agent-behavior-test-consolidation.md
  - skills/eval/tests/test_run_evals.py
known_limits: "Retired as a standalone skill after Eval behavior_trace reached prompt, event, log, checkpoint, artifact, schema, score, and baseline parity. Native-subagent-only evidence routes to Agent QA."
metrics: []
last_verified: 2026-07-16
experimental: false
superseded_by: FEAT-0039
---

# Retired agent behavior test workflow

The standalone Agent Behavior Test skill is retired. Its CLI-backed capture
contract now belongs to [FEAT-0039 Farplane evals](FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md)
through Eval `behavior_trace`; adversarial tester/evidence-review orchestration
remains in [Agent QA](FEAT-0034-adversarial-agent-qa-test-skill.md).

```text
eval(behavior_trace, prompt, task, optional_baseline)
  -> exact_prompt + jsonl_events + stdout_stderr + final_output
   + command_usage_checkpoint_scores + artifact_inventory
   + optional_schema_verdict + baseline_comparison
```

## Boundary

- Use Eval `behavior_trace` for one isolated Codex CLI run.
- Use Agent QA when tester evidence needs an adversarial evidence-review lane or
  the only available capture is a native subagent report.
- There is no compatibility alias or second runner.

## Proof

- `python3 skills/eval/tests/test_run_evals.py`
- `python3 skills/eval/scripts/check_eval_queries.py --root .`
- Source/live Eval runner and behavior schema must remain byte-identical.

## Change History

- 2026-06-26: Feature created.
- 2026-07-16: Retired the standalone skill after Eval behavior-trace parity;
  current behavior moved to FEAT-0039 without an alias.
