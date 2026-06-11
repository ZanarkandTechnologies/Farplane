---
name: autoresearch-plan
description: "Turn a fuzzy optimization goal into autoresearch scope, metric, direction, verification, guardrails, and execution artifacts."
tier: 3
group: self-improvement
source: local
---

# Autoresearch Plan

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the target docs, scripts, tests, active ticket, and existing
  autoresearch artifacts before proposing a session.
- [ ] Use the native planning phase when the goal, scope, metric, direction,
  verify command, or guard is not executable yet.
- [ ] Use [research:code-patterns](../research/SKILL.md#researchcode-patterns)
  only when a metric loop or eval harness needs local/peer implementation
  patterns.
- [ ] Lock the session primitives: goal, scope, metric, direction, verify,
  guard, max iterations, noise policy, and off-limits files.
- [ ] Dry-run the verify command and prove it emits one parseable metric.
- [ ] Write or update the session artifacts without overwriting existing runs
  blindly.
- [ ] Link ticket proof contract fields when the session supports ticketed
  work.
- [ ] Hand off to [autoresearch-exec](../autoresearch-exec/SKILL.md) only after
  the session contract is valid.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Set up a metric-driven improvement session. This skill plans the loop and writes
the session contract; `autoresearch-exec` runs the experiments.

## Trigger Conditions

Use when the user asks to:

- set up autoresearch for a target
- improve, optimize, or reduce something "given a metric"
- create a repeatable experiment loop
- validate whether a metric/verify command is suitable
- prepare `autoresearch.md`, `autoresearch.sh`, or a session baseline

Do not use when a session already exists and the user wants to continue running
experiments; use `autoresearch-exec`.

## Workflow

1. **Infer first:** inspect repo scripts, docs, tests, and target files before
   asking. Only ask for fields that cannot be inferred safely.
2. **Lock the session primitives:** Goal, Scope, Metric name/unit, Direction,
   Verify command, optional Guard command, max iterations, and noise policy.
3. **Validate scope:** confirm the editable scope resolves to real files and
   name read-only/off-limits surfaces.
4. **Screen Verify:** reject dangerous commands, outbound writes, embedded
   credentials, or subjective/manual metrics.
5. **Dry-run Verify:** run the candidate command once and prove it yields one
   numeric value or `METRIC name=value` line.
6. **Write session files:** create `autoresearch.md`, `autoresearch.sh`,
   optional `autoresearch.checks.sh`, and initialize `autoresearch.jsonl`.
7. **Ticket bridge:** when this session supports ticketed work, update the
   ticket `Proof Contract` with metric name, direction, verify command, guard
   command, minimum acceptable result when known, `Autoresearch warranted: yes`,
   and the session path.
8. **Hand off:** tell the user to run `autoresearch-exec` for bounded or
   unbounded execution.

## User Modes

- **Metric novice:** propose a safe metric, direction, guard, and max iteration
  default before asking for missing preferences.
- **Power operator:** accept provided commands, but still validate numeric
  output, side effects, and scope.
- **Skill author:** route skill-targeted optimization to `self-improve`; place
  durable runs under the target skill's `self-improve/runs/` when requested.
- **Safety-sensitive repo owner:** make off-limits files explicit and keep
  Verify/Guard free of secrets, network writes, deploys, or destructive actions.
- **Resume-focused agent:** write enough context into `autoresearch.md` and the
  config JSONL header that a fresh agent does not need chat memory.

## Session Files

The canonical artifact contract is in
`references/session-contract.md`. Load it when writing or reviewing session
files.

Reference split:

- `references/architecture.md` for ownership and boundaries
- `references/workflows.md` for the setup workflow
- `references/gotchas.md` for planning failure modes
- `references/metric-design.md` for metric and guard choices

Use `scripts/init_session.py` to scaffold files after the primitives are known:

```bash
python3 skills/autoresearch-plan/scripts/init_session.py \
  --goal "reduce type errors" \
  --scope "src/**/*.ts" \
  --metric-name type_errors \
  --direction lower \
  --verify-command "npm run typecheck 2>&1 | grep -c 'error TS'" \
  --guard-command "npm test" \
  --max-iterations 10
```

The script refuses to overwrite existing session files unless `--force` is
provided.

## Metric Design

Load `references/metric-design.md` when the metric is unclear, noisy, or could
reward the wrong behavior.

Good metrics:

- are mechanical and produce one number
- are cheap enough to run repeatedly
- match the user's goal rather than a proxy that can be gamed
- have a clear direction: `lower` or `higher`

Guard commands protect correctness and should not be optimized directly.

## Core Decision Branches

- **Goal is vague:** propose 3 metricable interpretations, recommend one, then
  ask only for the missing preference.
- **Metric is subjective:** stop and convert it to binary assertions, numeric
  score, or route to `self-improve` when the target is a skill.
- **Verify is slow/noisy:** add median runs, min delta, or bounded iterations.
- **Scope is broad:** narrow to the smallest file set that can move the metric.
- **User wants execution now:** finish the validated session first, then hand
  off to `autoresearch-exec`.
- **Ticketed work:** keep the ticket as the shared scoreboard. Do not copy the
  full session contract into the ticket; link the session path from the ticket
  `Proof Contract`.

## Top Gotchas

1. Do not start execution from this skill. Planning and execution are separate.
2. Do not accept "looks better" or judge-only scoring as the primary metric.
3. Do not let Verify mutate external systems, use secrets inline, or fetch and
   execute remote code.
4. Do not overwrite an existing session without reading `autoresearch.md` and
   `autoresearch.jsonl` first.
5. Do not use `autoresearch` for ticketed multi-lane implementation; use
   `impl-plan` and `$impl` when the work needs a ticket, QA, and review lanes.
6. Do not create skill-local memory for every scratch run; use it only when the
   target skill should carry durable evals and experiment lessons.

## Outcome Contract

At handoff, the project should contain:

- `autoresearch.md` with objective, scope, files, metric, constraints, and tried
  ideas
- executable `autoresearch.sh` that emits `METRIC <name>=<number>`
- optional executable `autoresearch.checks.sh`
- `autoresearch.jsonl` with a config header
- optional `autoresearch.ideas.md`
- a concise launch instruction for `autoresearch-exec`
