---
name: self-improve
description: Use when the user wants to improve an existing Codex skill, make a skill self-improving, build skill evals, compare skill variants, create skill-local memory, or provide eval/prompt context for native Goal-backed skill improvement.
tier: 3
group: self-improvement
source: local
skill_template_version: "0.2.0"
---

# Self Improve

## Context

Use this when a target skill, prompt, or harness surface needs measured
optimization against a metric. This skill owns experiment context, evals,
baselines, candidate comparison, skill-local memory, and promotion rules. It is
not a generic implementation planner and should not mutate a target before the
metric and proof path are clear.

Current mental model:

```text
Goal mode = durable loop runner
goal-crafter = writes the Goal contract
self-improve/ = target skill memory, evals, prompt candidates, and results
skill-maintenance = accepted writeback into SKILL.md/references/source copies
```

## Skill Signature

```text
self_improve_experiment(target_skill_or_surface, metric, search_space?, eval_suite?) -> best_candidate + experiment_log + promotion_recommendation
state: reads(target package, evals, metric, prior runs, candidate constraints); writes(program.md?, evals?, results?, promoted_change?)
gates: metric_named; baseline_recorded; candidates_compared; promotion_rule_met
routes: eval | goal-crafter | autoresearch-plan | skill-maintenance | review
fails: optimizes by taste; mutates before baseline; promotes unmeasured changes; bloats the target skill
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the target skill package or harness surface: `SKILL.md`, direct todo list, references,
  scripts, and existing `self-improve/` memory.
- [ ] 2. Clarify the improvement target, eval boundary, or editable scope with
  [plan](../plan/SKILL.md) when any of them is unclear.
- [ ] 3. Ground external examples or prior variants with
  [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when comparison is required.
- [ ] 4. Define the quality rubric and convert it into binary assertions before
  optimizing.
- [ ] 5. Establish a baseline score before mutating the target skill.
- [ ] 6. For durable iterative work, prefer native Goal mode as the loop runner;
  use this skill as the eval, prompt-profile, and skill-memory context surface.
- [ ] 7. Route to [autoresearch-plan](../autoresearch-plan/SKILL.md) only when
  the operator explicitly wants filesystem autoresearch artifacts in addition
  to a native Goal.
- [ ] 8. Promote only durable lessons, evals, and accepted changes into the target
  skill package, normally through [skill-maintenance](../skill-maintenance/SKILL.md).
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Improve a target by giving native Goal mode or a filesystem experiment loop the
context it needs to run a measured search. It does not need to own the durable
loop when a native `/goal` can do that directly.

## Trigger Conditions

Use when the user asks to:

- improve a skill
- make a skill self-improving
- add evals for a skill
- compare skill variants
- create or update a skill-local `program.md`
- add a prompt candidate/history workspace for prompt-like skills
- scaffold deterministic skill eval runners and result files
- preserve skill experiment memory inside the target skill package
- optimize `SKILL.md`, references, prompts, or bundled scripts with measured
  behavior
- prepare context files that a native Goal should read while optimizing a skill

Use `goal-crafter` first when the user wants a durable native Goal. Use
`autoresearch-plan` only when the user explicitly wants filesystem
autoresearch artifacts, separate experiment scripts, or a metric loop outside
native Goal mode.

## Workflow

1. **Read target skill:** inspect `SKILL.md`, its direct todo list, references, and
   scripts. Do not edit yet.
2. **Load skill memory:** read `self-improve/program.md` when present. If the
   user wants durable skill memory, create it before experiments.
3. **Classify maturity:** rewrite if the skill is broken or missing core
   workflow; optimize only when it is already roughly usable.
4. **Define rubric:** capture 3-6 human quality dimensions that matter.
5. **Build binary evals:** convert rubric dimensions into `pass/fail`
   assertions over realistic prompts and expected artifacts.
6. **Baseline:** run the eval suite against the current skill and record pass
   rate when deterministic evals exist. For subjective artifacts, record the
   current human-review rubric and latest feedback instead.
7. **Prepare Goal context:** make sure `program.md`, evals, latest results, and
   failure analysis tell Goal mode what to optimize, how to verify, and what
   not to regress.
8. **Iterate through native Goal mode:** change one bounded part of the skill
   at a time, rerun evals or present the review artifact, keep only
   improvements that do not break skill validation, and record the lesson.
9. **Debrief and write back:** summarize before/after behavior in rubric
   terms, update `program.md` with reusable lessons, preserve evals only when
   durable, and use `skill-maintenance` for accepted edits to
   `SKILL.md`/references/source copies.

Load `references/skill-evals.md` before designing eval cases. Load
`references/skill-memory.md` before writing skill-local memory.

Reference split:

- `references/architecture.md` for the self-improvement boundary
- `references/workflows.md` for eval and optimization phases
- `references/gotchas.md` for eval leakage and overfitting risks
- `references/skill-evals.md` for case/assertion design
- `references/skill-memory.md` for target-skill `program.md` and run history

## Goal Mode Integration

A native Goal improving a skill should dynamically read these target-skill
files when they exist:

```text
<target-skill>/SKILL.md
<target-skill>/references/*
<target-skill>/scripts/*
<target-skill>/self-improve/program.md
<target-skill>/self-improve/evals/*
<target-skill>/self-improve/results/latest_run.json
<target-skill>/self-improve/results/failure_analysis.md
<target-skill>/self-improve/prompts/current.txt
<target-skill>/self-improve/prompts/candidates/*
<target-skill>/self-improve/runs/*/notes.md
```

`program.md` should define the optimization target: desired behavior, rubric,
metric or human feedback schema, known failure modes, constraints, accepted
lessons, and promotion rules. When `program.md` is missing or stale, update it
before asking Goal mode to optimize.

## Artifact Layout

Use an experiment directory for scratch or early eval work when native Goal
context files are not yet durable enough:

```text
experiments/self-improve/<skill-name>/<date-slug>/
  evals/cases.jsonl
  evals/assertions.md
  results/scores.jsonl
  autoresearch.md
  autoresearch.sh
  autoresearch.jsonl
```

For durable skill self-improvement, store memory inside the target skill package:

```text
skills/<target-skill>/self-improve/
  program.md
  evals/cases.jsonl
  evals/assertions.md
  runs/<YYYYMMDD-HHMM-slug>/
    autoresearch.md
    autoresearch.sh
    autoresearch.jsonl
    scores.jsonl
    notes.md
```

Use `scripts/init_skill_memory.py` to scaffold the target-skill memory surface:

```bash
python3 skills/self-improve/scripts/init_skill_memory.py skills/prd \
  --goal "make PRD authoring more decisive and easier to resume"
```

For prompt-like skills, add the prompt/profile eval harness:

```bash
python3 skills/self-improve/scripts/init_skill_memory.py skills/prd \
  --goal "make PRD authoring more decisive and easier to resume" \
  --prompt-profile
```

That also creates:

```text
self-improve/prompts/current.txt
self-improve/prompts/candidates/
self-improve/prompts/history/
self-improve/evals/test_cases.jsonl
self-improve/evals/assertions.py
self-improve/evals/runner.py
self-improve/results/scores.jsonl
self-improve/results/latest_run.json
self-improve/results/failure_analysis.md
```

Only promote evals and run summaries into the target skill package after they
prove reusable. Keep raw scratch logs in `experiments/` when they are bulky,
secret-bearing, one-off, or too noisy for durable skill memory. For accepted
changes to first-load instructions, use `skill-maintenance` so mandatory logic
lands in the source `SKILL.md` rather than being buried in references or
installed copies.

## Core Decision Branches

- **Skill is missing the first-load contract:** rewrite the skill before
  optimizing.
- **No binary metric exists:** build evals first; do not optimize by taste.
- **Target skill has `self-improve/program.md`:** read it as durable memory
  before proposing a new hypothesis.
- **Target skill has scripts:** include script behavior in evals when scripts
  carry the fragile logic.
- **Target skill is prompt-like:** use `--prompt-profile` and compare
  `current`, `candidates`, and score-bearing `history`.
- **Eval pass rate improves but skill becomes bloated:** use a simplicity guard,
  usually line count or duplicated-rule count.
- **Eval suite is too narrow:** add cases before trusting the optimization.
- **Native Goal can carry the loop:** keep this skill focused on context,
  memory, evals, and evidence; do not create parallel loop machinery.

## Gotchas

1. Do not leak the intended answer into eval prompts.
2. Do not use judge-only subjective scores as the primary keep/discard metric.
3. Do not mutate the user's target skill until baseline evals exist.
4. Do not promote experimental evals into the skill package until they catch at
   least one real failure mode.
5. Do not treat old autoresearch artifacts as mandatory when native Goal mode
   is the simpler durable loop.
6. Do not optimize a skill that should be split into smaller skills first.
7. Do not fill target skill packages with bulky raw logs; store durable
  summaries, accepted evals, and reusable lessons.

## Reference Map

- [references/architecture.md](references/architecture.md) - self-improvement
  boundary and ownership model.
- [references/workflows.md](references/workflows.md) - eval and optimization
  phases.
- [references/gotchas.md](references/gotchas.md) - eval leakage and
  overfitting risks.
- [references/skill-evals.md](references/skill-evals.md) - case and assertion
  design.
- [references/skill-memory.md](references/skill-memory.md) - target-skill
  `program.md` and run history.
- [eval](../eval/SKILL.md) - proof and hardcase-marked eval cases.
- [skill-maintenance](../skill-maintenance/SKILL.md) - accepted writeback to
  skill source files.

## Templates

Experiment spine:

```text
target + metric + search_space + eval_suite -> baseline -> candidates -> comparison -> promotion
```

Promotion note:

```text
Target:
Metric:
Baseline:
Candidates:
Best candidate:
Promotion rule:
Accepted writeback:
Residual risk:
```

## Output

A self-improvement pass should leave:

- eval cases and assertions for the target skill
- deterministic eval runner/results when the prompt profile is used
- baseline score and changed-score logs
- Goal-readable context in `program.md`, latest results, failure analysis, and
  prompt/eval files
- updated `self-improve/program.md` when the user wants durable skill memory
- a concise before/after debrief
- only measured, reversible target skill edits
