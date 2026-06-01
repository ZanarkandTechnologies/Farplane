---
name: self-improve
description: Use when the user wants to improve an existing Codex skill, make a skill self-improving, build skill evals, compare skill variants, or run binary assertion based skill optimization through the autoresearch artifact contract.
tier: 3
group: self-improvement
source: local
---

# Self Improve

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] Read the target skill package: `SKILL.md`, direct checklist, references,
  scripts, and existing `self-improve/` memory.
- [ ] Use [plan](../plan/SKILL.md) when the improvement target, eval boundary,
  or editable scope is unclear.
- [ ] Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when comparing external skill examples or prior variants.
- [ ] Define the quality rubric and convert it into binary assertions before
  optimizing.
- [ ] Establish a baseline score before mutating the target skill.
- [ ] Use [autoresearch-plan](../autoresearch-plan/SKILL.md) to create the
  metric loop when repeated experiments are warranted.
- [ ] Use [autoresearch-exec](../autoresearch-exec/SKILL.md) to run bounded
  experiments after the session exists.
- [ ] Promote only durable lessons, evals, and accepted changes into the target
  skill package.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

Improve a target skill with binary evals and the shared autoresearch session
contract. This is a special case of autoresearch where the editable artifact is
a skill and the metric is eval pass rate.

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

Use `autoresearch-plan` first when the user wants a generic metric loop that is
not skill-specific.

## Workflow

1. **Read target skill:** inspect `SKILL.md`, its direct checklist, references, and
   scripts. Do not edit yet.
2. **Load skill memory:** read `self-improve/program.md` when present. If the
   user wants durable skill memory, create it before experiments.
3. **Classify maturity:** rewrite if the skill is broken or missing core
   workflow; optimize only when it is already roughly usable.
4. **Define rubric:** capture 3-6 human quality dimensions that matter.
5. **Build binary evals:** convert rubric dimensions into `pass/fail`
   assertions over realistic prompts and expected artifacts.
6. **Baseline:** run the eval suite against the current skill and record pass
   rate.
7. **Create autoresearch session:** use the shared artifacts with metric
   `skill_eval_pass_rate` and direction `higher`.
8. **Iterate:** change one part of the skill at a time, rerun evals, keep only
   improvements that do not break skill validation.
9. **Debrief:** summarize before/after behavior in rubric terms, update
   `program.md` with reusable lessons, and preserve evals only when durable.

Load `references/skill-evals.md` before designing eval cases. Load
`references/skill-memory.md` before writing skill-local memory.

Reference split:

- `references/architecture.md` for the self-improvement boundary
- `references/workflows.md` for eval and optimization phases
- `references/gotchas.md` for eval leakage and overfitting risks
- `references/skill-evals.md` for case/assertion design
- `references/skill-memory.md` for target-skill `program.md` and run history

## Artifact Layout

Use an experiment directory by default for scratch or early eval work:

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
secret-bearing, one-off, or too noisy for durable skill memory.

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

## Top Gotchas

1. Do not leak the intended answer into eval prompts.
2. Do not use judge-only subjective scores as the primary keep/discard metric.
3. Do not mutate the user's target skill until baseline evals exist.
4. Do not promote experimental evals into the skill package until they catch at
   least one real failure mode.
5. Do not optimize a skill that should be split into smaller skills first.
6. Do not fill target skill packages with bulky raw logs; store durable
   summaries, accepted evals, and reusable lessons.

## Outcome Contract

A self-improvement pass should leave:

- eval cases and assertions for the target skill
- deterministic eval runner/results when the prompt profile is used
- baseline score and changed-score logs
- an autoresearch session pointing to the eval runner
- updated `self-improve/program.md` when the user wants durable skill memory
- a concise before/after debrief
- only measured, reversible target skill edits
