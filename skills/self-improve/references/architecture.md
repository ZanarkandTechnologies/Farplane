# Self Improve Architecture

`self-improve` is a skill-specific autoresearch setup.

Inputs:

- target skill directory
- human rubric
- realistic prompts
- binary assertions

Outputs:

- experiment-local eval cases
- optional target-skill `self-improve/program.md` memory
- baseline skill score
- autoresearch session configured around eval pass rate
- measured skill edits
- before/after debrief

The target skill is not mutated until the eval baseline exists.

## Storage Boundary

Use `experiments/self-improve/` for scratch runs and bulky logs. Use
`skills/<target-skill>/self-improve/` only for durable evals, run summaries, and
lessons that future improvement passes should read before editing.
