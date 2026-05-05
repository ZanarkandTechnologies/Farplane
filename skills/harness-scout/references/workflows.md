# Workflows

## Single Source

1. Extract source content with [summarize](../../summarize/SKILL.md).
2. Search `docs/sources/registry.jsonl` by canonical URL, canonical key, title,
   and linked local artifacts. Reuse the matching `SRC-*` record when present.
3. Classify source visibility and apply the untrusted-input boundary.
4. Redact private or sensitive extracts before writing tracked files.
5. Create or update a run folder under `experiments/harness-scout/runs/`.
6. Extract concrete feature candidates.
7. Search `docs/features/registry.jsonl` and nearby local docs/skills; use
   [codebase-analysis](../../codebase-analysis/SKILL.md) when the match depends
   on local implementation behavior.
8. Use [external-patterns](../../external-patterns/SKILL.md) or
   [documentation](../../documentation/SKILL.md) only when source claims need
   code or official-doc verification.
9. Score each candidate.
10. Write `decision-matrix.md`.
11. Update the `SRC-*` record with local artifacts, feature refs, and the final
    source decision.
12. Create `handoff.md` only for strong `adopt` or `adapt` candidates.

## Multi-Source Theme

1. Create one run folder per source.
2. Normalize duplicate feature candidates.
3. Build a project comparison matrix when feature support differs by source.
4. Use [best-of-worlds](../../best-of-worlds/SKILL.md) for synthesis.
5. Update the source registry for provenance and the feature registry only for
   durable local feature knowledge.
6. Ticket only the chosen now-scope.

## Benchmark Scorecard

1. Pick one small task.
2. Compare `current-codexter`, `source-proposed`, and
   [best-of-worlds](../../best-of-worlds/SKILL.md).
3. Score each `1-10` across completion, evidence, trust, resume quality,
   overhead, and maintainability.
4. Record confidence and anti-metrics.
5. If the manual scorecard is too weak but the candidate is still important,
   route to [autoresearch-plan](../../autoresearch-plan/SKILL.md) for a real
   metric-backed benchmark plan.
6. Treat the scorecard as a judgment aid, not a scientific benchmark.

## Skill-Change Follow-Up

1. If the adopted idea changes a skill, route the follow-up through
   [self-improve](../../self-improve/SKILL.md) instead of editing the skill
   directly from source inspiration.
2. Keep the source run as evidence and define skill-specific binary evals.
3. Run [review](../../review/SKILL.md) after the eval or skill proposal changes
   durable artifacts.
