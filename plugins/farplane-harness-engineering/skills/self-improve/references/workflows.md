# Self Improve Workflows

## Eval-First Skill Optimization

1. Read target skill and references.
2. Read `self-improve/program.md` when the target skill already has durable
   improvement memory.
3. Classify whether it needs rewrite or optimization.
4. Define rubric dimensions.
5. Convert rubric into binary assertions.
6. Build at least 3 eval cases.
7. Baseline pass rate.
8. Create an autoresearch session with `skill_eval_pass_rate`.
9. Iterate one skill change at a time through `autoresearch-exec`.
10. Debrief before/after behavior and update durable skill memory with lessons.

Use 3-5 cases for smoke validation. Use 20-100 diverse cases before trusting an
overnight or unattended optimization run.

## Skill-Memory Setup

Use this path when the operator wants the skill itself to remember experiments:

1. Run `scripts/init_skill_memory.py <skill-dir> --goal "<goal>"`.
2. Fill `self-improve/program.md` with the skill contract, rubric, and first
   hypotheses.
3. Put reusable binary evals in `self-improve/evals/`.
4. Create one run directory per autoresearch session under
   `self-improve/runs/<YYYYMMDD-HHMM-slug>/`.
5. After each run, copy the short lesson into `program.md` and leave bulky raw
   logs in `experiments/` unless they are safe and useful.

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
