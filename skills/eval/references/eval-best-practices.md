# Eval Best Practices

Use this when writing or revising task files and judge prompts.

## Task Design

- Start with 3-5 behaviors the harness must keep doing.
- Write one task per behavior; do not start with broad benchmark coverage.
- Keep task JSON simple: `id`, `title`, optional `context`, `query`,
  `reference_points`, `tags`, and `notes`.
- For skill-specific behavior, store the task next to the owning skill as
  `skills/<skill-name>/eval_task.json`. Use `.farplane/evals/tasks/*` for
  active project work and `skills/eval/examples/*` for reusable cross-skill
  examples.
- Keep `query` as the realistic user request. Put suite-wide fixture setup,
  company background, role assumptions, and safety boundaries in `config.json`
  plus `contexts/*`, rendered by the agent prompt with `{context_block}`.
- Use task `context` only when a task needs to override the suite default. Use
  explicit `"context": ""` for real-repo tasks that should receive no toy
  fixture context.
- Use string `reference_points`; make each point visible in the answer or
  artifact.
- Use `tags` and `notes` to mark layer: `skill`, `workflow`, or
  `system-prompt`.
- Keep task prompts realistic. The task should look like a user request the
  harness would actually receive.
- Prefer safe toy-company scenarios when the behavior under test is response
  judgment, workflow shape, escalation, pushback, planning, or artifact
  selection rather than actual repo mutation.
- Use AGI Toy Shop as the default clean-room toy company for generic harness
  evals: a small app company fully run by agents, with docs, skills, tickets,
  storefront, toy inventory, customer support, safety review, marketing, and
  release operations. Store this as the default context file instead of
  repeating it in every task.
- Avoid prompts that ask the target agent to install, delete, push, deploy,
  rotate secrets, mutate live config, or touch a real user path unless that
  exact side effect is the behavior being tested and the runner is sandboxed.
- Make toy scenarios concrete enough to grade: include shared company context,
  role assumptions, known limitations, and safety boundaries in the context
  file; keep realistic pressure such as urgency, stakeholder confusion, or an
  over-broad ask in `query` when that is what the user would actually say.
- Use private or external eval suites only as clean-room pattern inspiration:
  borrow task shape, realism, and rubric style; do not copy restricted content,
  proprietary fixtures, exact examples, private repo names, prompts, or data.

## Admission And Aggregation

- Adding a feature should trigger a proof-surface decision, not an automatic
  eval row.
- Write an eval when the feature is behavioral, prompt-like, workflow-like,
  easy to regress silently, or came from a high-priority correction.
- Prefer a deterministic test, validator, or static check when the feature is
  structural and the expected output can be checked mechanically.
- Skip a new eval when the change is tiny, one-off, already covered by a
  stronger proof surface, or the eval would only assert wording.
- Use a broad "response format" eval as a smoke canary for always-on behavior
  bundles, but do not overload one task with every important behavior. Broad
  canaries catch drift; narrow evals diagnose regressions.
- If a broad canary fails twice or hides the cause of failure, split the missed
  behavior into its own focused eval or deterministic check.
- Prefer modular skill-local evals when the behavior belongs to one skill. A
  skill-local `eval_task.json` should be runnable without chat context and
  should not depend on another skill's private fixture unless the task says so.

## Judge Design

- Do not ask the judge for 0-100 scores. Small numeric differences are false
  precision and create bad optimization incentives.
- Prefer boolean reference-point checks plus coarse tiers: `A`, `B`, `C`, or
  `D`.
- Treat only `A` as pass. Use `B` for near misses that are useful but still
  worth fixing.
- Put rubric policy in `prompts/judge.md`, not in task JSON.
- Make the judge cite which reference points were met or missed.
- Do not average tier results mechanically. Let the most severe issue constrain
  the overall verdict.
- Add `repeatability` when judging skills, prompts, workflows, or reusable
  harness behavior. It should fail when another agent would need chat context,
  duplicated instructions, or hidden decisions to run the artifact again.
- Use `D` when the answer cannot be judged because evidence or context is
  missing.
- Keep the judge output machine-readable and boring.

## Harness Realism

- Run the task through the target harness CLI when behavior depends on system
  prompts, skills, tools, or repo instructions.
- Keep `prompts/agent.md` minimal. Usually it should be
  `{context_block}User request:\n{query}` so the harness under test supplies its
  own instructions while the eval runner can provide clean-room fixture context
  separately from the user request.
- Use fake command templates only for runner tests and deterministic smoke
  checks.
- For serious behavior claims, inspect task detail artifacts, not only
  `summary.json`.
- Match realism to risk:
  - Use AGI Toy Shop scenarios for language, reasoning, routing, escalation,
    and planning behaviors.
  - Use real repo scenarios only for behaviors that cannot be tested honestly
    without local files, validators, skills, or scripts.
  - If a real repo scenario is required, make the query inspect-only or
    sandboxed unless the eval runner owns an isolated fixture checkout.

## Expansion Rule

Start with one task. Add more only when the first run teaches something:

1. The task catches a real regression.
2. The judge disagrees with human judgment and needs revision.
3. The answer passes but misses an important workflow step.
4. A second layer, such as workflow or system-prompt behavior, is now the next
   bottleneck.
