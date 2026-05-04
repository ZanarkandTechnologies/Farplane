# Workflows

## Single Source

1. Extract source content with [summarize](../../summarize/SKILL.md).
2. Classify source visibility and apply the untrusted-input boundary.
3. Redact private or sensitive extracts before writing tracked files.
4. Create a run folder under `experiments/harness-scout/runs/`.
5. Extract concrete feature candidates.
6. Search `docs/features/registry.jsonl` and nearby local docs/skills.
7. Score each candidate.
8. Write `decision-matrix.md`.
9. Create `handoff.md` only for strong `adopt` or `adapt` candidates.

## Multi-Source Theme

1. Create one run folder per source.
2. Normalize duplicate feature candidates.
3. Build a project comparison matrix when feature support differs by source.
4. Use [best-of-worlds](../../best-of-worlds/SKILL.md) for synthesis.
5. Update the registry only for durable local knowledge.
6. Ticket only the chosen now-scope.

## Benchmark Scorecard

1. Pick one small task.
2. Compare `current-codexter`, `source-proposed`, and
   [best-of-worlds](../../best-of-worlds/SKILL.md).
3. Score each `1-10` across completion, evidence, trust, resume quality,
   overhead, and maintainability.
4. Record confidence and anti-metrics.
5. Treat the scorecard as a judgment aid, not a scientific benchmark.
