# Clean Mode

Load after `SKILL.md` selects `clean`. Metrics prioritise the work; they do not
replace judgment.

## Target selection

```text
priority = smell_score x change_frequency x feature_relevance
smell_score = complexity + nesting + size + duplication + coverage_gap
            + lint_static_issues + boundary_violations
```

Spend the pass on changed or high-churn code. Stable old code nobody touches is
not a target, however ugly. Duplication that has already caused divergent fixes
beats cosmetic issues; high complexity with low coverage beats both.

## Transformations

- Extract pure logic from side effects.
- Split mixed responsibilities by caller need, never by line count.
- Replace duplicated logic with one owner module, not a generic utility bucket.
- Rename only where it removes ambiguity at call sites.
- Tighten types or schemas when that makes behaviour easier to prove.
- Run the proof after each risky move; keep behaviour changes out.

## Anti-gaming

- Do not split one clear function into scattered helpers to cut lines.
- Do not hide complexity behind an over-general abstraction with unclear
  callers.
- Do not treat coverage percentage as proof when assertions are weak.
- Optimise the metric that matches the current maintenance pain, not all of
  them equally.

## Stop conditions

- The behaviour boundary cannot be proven: lock it first or stop.
- The cleanup would change public behaviour (for example an API response
  shape): that is a separate feature or ticket.
- The highest-priority target belongs to another owner or ticket.
- Metrics improve only by making code harder to read or test.

## Tooling

Choose by stack and smell; install nothing without operator approval or a setup
ticket.

- JS/TS: ESLint or Oxlint (complexity, depth, hooks, floating promises), Knip
  (unused exports and deps), dependency-cruiser or Madge (cycles, boundaries),
  jscpd (duplication), Stryker (mutation, high budget only).
- Python: Ruff, Radon (complexity), mypy or pyright, vulture (dead code),
  mutmut (mutation).
- Cross-language: Semgrep for structural rules; cloc/scc for size inventory
  only, never as a quality score.

Record adopted commands in the Validation section of the project's `AGENTS.md`
(lint, complexity, duplication, dependency boundaries, dead code, mutation).

## Report

```text
metric_delta: target, before, after, proof, tradeoff
```
