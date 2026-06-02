# Eval Best Practices

Use this when writing or revising task files and judge prompts.

## Task Design

- Start with 3-5 behaviors the harness must keep doing.
- Write one task per behavior; do not start with broad benchmark coverage.
- Keep task JSON simple: `id`, `title`, `query`, `reference_points`, `tags`,
  and `notes`.
- Use string `reference_points`; make each point visible in the answer or
  artifact.
- Use `tags` and `notes` to mark layer: `skill`, `workflow`, or
  `system-prompt`.
- Keep task prompts realistic. The task should look like a user request the
  harness would actually receive.

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
- Keep `prompts/agent.md` minimal. Usually it should be only `{query}` so the
  harness under test supplies its own instructions.
- Use fake command templates only for runner tests and deterministic smoke
  checks.
- For serious behavior claims, inspect task detail artifacts, not only
  `summary.json`.

## Expansion Rule

Start with one task. Add more only when the first run teaches something:

1. The task catches a real regression.
2. The judge disagrees with human judgment and needs revision.
3. The answer passes but misses an important workflow step.
4. A second layer, such as workflow or system-prompt behavior, is now the next
   bottleneck.
