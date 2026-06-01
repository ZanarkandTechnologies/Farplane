# Eval Onboarding Module

This module owns clean-room starter eval workflows for agents, prompts, skills,
and harness changes.

Keep examples synthetic. Do not copy private, interview, client, or third-party
task text into this module. When a private source inspires a shape, translate
only the abstract pattern into invented task names, prompts, and reference
points.

Prefer the smallest useful proof:

1. saved-output scoring for first evals
2. `agent-behavior-test` for live Codex or child-agent run capture
3. `agent-qa-test` for adversarial readiness proof
4. Promptfoo or another matrix runner only after the suite is stable enough to
   deserve provider/model comparison
