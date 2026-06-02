# Autoresearch Session: Terminal Warehouse Landing Benchmark

## Goal

Improve `landing-page` so Terminal Industries-style industrial landing pages
produce a spec first, then asset and implementation phases that can be visually
compared against a gold reference.

## Scope

- Target skill: `skills/landing-page`
- Related delegation profile: `frontend-pi-kimi`
- Gold reference: `https://terminal-industries.com/`
- Benchmark task: warehouse computer-vision enterprise landing page

## Metric

- `skill_eval_pass_rate`
- Direction: higher
- Runner: `python3 skills/landing-page/self-improve/evals/runner.py`

## Baseline Evidence

- Empty candidate baseline: `0.078947`
- Observed artifact candidate: run `runner.py` after this session's candidate
  output file is written.
- Pi/Kimi model evidence:
  - `terminal-style-warehouse-baseline`: created `SPEC.md`, then stalled.
  - `terminal-style-warehouse-build-pass-2`: created partial `index.html`,
    timed out.
  - `terminal-style-render-repair-pass`: repaired CSS/JS partially, timed out.
  - `terminal-style-assets-only-pass`: created SVG assets, timed out before
    handoff.

## Guardrails

- Do not treat a timed-out external CLI run as a successful handoff.
- Do not optimize only for exact string evals; preserve visual and artifact
  proof requirements.
- Do not lower the Terminal-quality bar to code-native SVG placeholders.
