# Todos

- [ ] Identify the filesystem/build/debug goal and the safest working
  directory before running commands.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) for local
  evidence: file paths, scripts, package manager, branch, dirty files, and
  existing command patterns.
- [ ] Prefer `rg`, `rg --files`, narrow file reads, and parallel read-only
  commands for exploration.
- [ ] Run the smallest command that proves or advances the task; avoid noisy
  chained shell output.
- [ ] Preserve unrelated dirty changes and avoid destructive commands.
- [ ] Capture reproducible commands and important output for the caller.
- [ ] Use [advise](../advise/SKILL.md) when there is a real safety or runtime
  tradeoff.
- [ ] Use [review](../review/SKILL.md) before treating command-heavy repo
  changes as complete.
