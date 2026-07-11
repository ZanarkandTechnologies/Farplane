# Self Improve Architecture

`self-improve` is skill-specific improvement memory and measured candidate
comparison.

Inputs:

- target skill or harness surface
- metric or human rubric
- feedback class: `immediate` or `delayed`
- realistic prompts or bounded intervention
- binary assertions or delayed-signal provider
- original experiment ticket and Goal Packet for delayed feedback

Outputs:

- experiment-local eval cases
- optional target-skill `self-improve/program.md` memory
- baseline skill score
- metric card or no-metric rationale
- eval, review, human-feedback, or Goal-loop comparison plan
- immediate measured result or delayed `waiting_signal` state
- measured skill edits
- before/after debrief

The target skill is not mutated until the eval baseline exists.

## Storage Boundary

Use `.farplane/self-improve/` for scratch runs and bulky logs. Use
`skills/<target-skill>/self-improve/` only for durable evals, run summaries, and
lessons that future improvement passes should read before editing.

Delayed experiment state does not belong in this scratch-memory layout. Keep
the expectation in the original ticket's `Reward.kpi_rewards[]`, loop policy
in `program.md`, and append-only observations in `progress.md`. Work Pulse
derives due check-in eligibility from those files.
