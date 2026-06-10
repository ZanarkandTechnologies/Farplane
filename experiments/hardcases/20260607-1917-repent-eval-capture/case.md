# Behavior Correction Should Capture High-Priority Eval Regressions

Captured: 2026-06-07 19:17 +0800
Privacy: local_only
Failure class: wrong_tool

## Original Task

The operator asked to improve and evaluate the global AGENTS prompt workflow,
including eval design, skill todo rendering, and prompt ownership behavior.

## Observed Failure

The agent initially seeded global AGENTS workflow eval tasks under
`skills/eval/examples/`, making the reusable eval skill package own
project-specific system-prompt evals. The query prompts were also over-directed:
they embedded meta-instructions such as "A user asks..." and named the exact
peer repo to inspect, instead of letting the system prompt's grounding behavior
show up from a realistic minimal user prompt.

## User Correction

The operator pointed out that project-level evals should be written to
`.codex/evals/tasks/`, because skill-level examples may be wiped or replaced
when skills are reinstalled. The operator also said high-priority repent cases
should chain into eval or agent behavior capture so the system keeps fixing
until the behavior passes.

## Correct Behavior

For corrected high-priority prompt or harness misses, `repent` should verify the
miss, fix the same-scope issue first, capture a concise lesson or hardcase, add
the narrowest regression eval in the owning eval surface, and use
`agent-qa-test` or `agent-behavior-test` when visible child-agent behavior needs
proof.

## Fixed Outcome

The global AGENTS workflow eval suite was moved to
`.codex/evals/tasks/harness_tasks.json`, `.gitignore` now permits tracked eval
task JSON while leaving generated eval runtime files ignored, and the task
queries were rewritten as realistic minimal prompts with proactive expectations
in `reference_points`.

## Evidence Refs

- `.codex/evals/tasks/harness_tasks.json`
- `.gitignore`
- `skills/eval/SKILL.md`
- `skills/optimize-harness/SKILL.md`
- `docs/LESSONS.md`
- commit `b7c58c0 test(eval): move global workflow suite to codex evals`

## Future Eval Idea

Given a prompt like "this was high priority: you fixed the prompt
ownership bug, but you should have captured an eval so this never happens
again", the agent should verify the miss and fixed outcome, classify it as
eval-worthy, add a project-level regression eval under `.codex/evals/tasks/`,
and report validation plus any skipped agent-test reason.

## Open Risks

- The current eval runner validates final answers, not full tool-event traces.
  Agent behavior proof still needs `agent-behavior-test` or `agent-qa-test`
  when the claim depends on visible child-agent command logs.
