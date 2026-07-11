# Self Improve Workflows

## Eval-First Skill Optimization

1. Read target skill and references.
2. Read `self-improve/program.md` when the target skill already has durable
   improvement memory.
3. Classify whether it needs rewrite or optimization.
4. Define rubric dimensions.
5. Use metric-advisor when provider, guard metrics, anti-metrics, or no-metric
   rationale are unclear.
6. Convert rubric into binary assertions.
7. Build at least 3 eval cases.
8. Baseline pass rate or baseline reviewer/human judgment.
9. Classify feedback as immediate or delayed.
10. For immediate feedback, iterate one skill change at a time through native
    Goal mode or a bounded candidate-comparison pass and decide in-window.
11. For delayed feedback, record baseline/exposure and exact Reward rows, then
    use Goal Advisor to compile the experiment-specific evidence, scoring,
    decision, writeback, idempotency, and source-gap procedure into the
    original `program.md` `Check-In Program` before entering `waiting_signal`.
12. Debrief before/after behavior and update durable skill memory with lessons.

Use 3-5 cases for smoke validation. Use 20-100 diverse cases before trusting an
overnight or unattended optimization run.

## Skill-Memory Setup

Use this path when the operator wants the skill itself to remember experiments:

1. Run `scripts/init_skill_memory.py <skill-dir> --goal "<goal>"`.
2. Fill `self-improve/program.md` with the skill contract, rubric, and first
   hypotheses.
3. Put reusable binary evals in `self-improve/evals/`.
4. Create one run directory per candidate-comparison session under
   `self-improve/runs/<YYYYMMDD-HHMM-slug>/`.
5. After each run, copy the short lesson into `program.md` and leave bulky raw
   logs in `.farplane/` unless they are safe and useful.

## Prompt-Profile Optimization

Use this path when a skill is mostly prompt/instruction behavior:

1. Scaffold with `scripts/init_skill_memory.py <skill-dir> --prompt-profile`.
2. Put the active instruction in `prompts/current.txt`.
3. Generate 2-5 variants in `prompts/candidates/`.
4. Run `evals/runner.py` against candidate outputs.
5. Promote the best variant into `prompts/history/` with score in the filename.
6. Patch the real skill only after the candidate beats current and guard checks
   pass.

## Rewrite Before Optimize

Use this path when the skill lacks:

- clear trigger conditions
- a first-load workflow
- outcome contract
- reference navigation
- concrete validation behavior

Rewrite the skill first, then add evals.

## Delayed Check-In

Use this only when the real signal cannot mature inside the current execution
window:

1. Keep the intervention and expected result in the original experiment
   ticket.
2. Add one or more `Reward.kpi_rewards[]` rows with `check_in_at`; do not add
   experiment metadata.
3. Use Goal Advisor to fill `program.md` `Check-In Program` with its packet
   inputs, exact evidence sources, ordered procedure, writeback, decision
   thresholds, idempotency, and missing-source behavior.
4. Append baseline and exposure observations to `progress.md`.
5. Let Work Pulse derive matured rows and hand the same ticket/program/progress
   plus row indexes and evidence refs to one worker.
6. Have that worker read `program.md` first, execute `Check-In Program`, update
   only matured rows, append progress, and return `accept`, `kill`, `iterate`,
   or `monitor`.

### Exact Goal Packet Contract

```text
ticket.md / Reward.kpi_rewards[]:
  kpi_id
  expected_reward
  check_in_at
  actual_result
  reward_score
  reward_score_reason

program.md:
  Metric Provider.signal + minimum
  Heartbeat Policy.wake_condition
  Check-In Program:
    mode: delayed_reward
    inputs: original ticket/program/progress + matured row indexes + evidence
    procedure: ordered evidence collection, attribution, comparison, scoring
    writeback: matured Reward rows + append-only progress entry
    decisions: accept_when + kill_when + iterate_when + monitor_when
    idempotency: preserve future/completed rows; correction note on rescore
    source_gap: record gap + monitor/next check-in unless explicitly overridden
  Stop Conditions.complete_when + pause_when
  Rollout Policy.promotion_rule + rollback_or_hold_rule

progress.md:
  append-only baseline, exposure, observations, and decisions
```

A row is due when `check_in_at <= now` and either `actual_result` or
`reward_score` is empty. Work Pulse resumes the original non-terminal ticket,
hands every matured row to one worker, and leaves future/completed rows alone.
It does not reproduce the decision rules stored in `program.md`.

Decisions:

- `accept`: keep/promote and close;
- `kill`: prune/rollback and close;
- `iterate`: update the hypothesis and resume work now;
- `monitor`: remain dormant and update the same ticket's next check-in.

For immediate feedback, keep `Check-In Program` to
`mode: not_applicable` plus a reason. Do not fill any delayed procedure fields.

## Decision Branches

- Rewrite a target missing its first-load contract before optimizing it.
- If no honest metric exists, use metric-advisor, eval/review, or human
  feedback instead of a fake score.
- Read existing target-local memory before proposing another hypothesis.
- Include scripts in evals when they carry fragile behavior.
- Use the prompt profile for prompt-like targets.
- Add cases before trusting a narrow suite; use simplicity guards when scores
  improve by adding bloat.
- Keep Goal as the loop runner and this skill as measured context/evidence.
